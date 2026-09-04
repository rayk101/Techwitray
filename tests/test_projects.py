"""Behavioral tests: business edge cases, API failures and offline end-to-end runs."""
import contextlib
import hashlib
import io
import json
import os
import tempfile
import unittest
import urllib.error
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlsplit

import run
import start
import toolkit

CATALOG = toolkit.read_json(toolkit.ROOT / "catalog.json")


def app(project_id):
    project = next(item for item in CATALOG if item["id"] == project_id)
    return run.load_project(project)


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def input(self, content, name="input.csv"):
        target = self.path / name
        target.write_text(content, encoding="utf-8")
        return target

    def test_expenses_refunds_transfers_and_month_boundary(self):
        data = "id,date,description,category,amount\n1,2026-08-01,Pay,Income,100.00\n2,2026-08-02,Food,Food,-0.10\n3,2026-08-02,Food,Food,-0.20\n4,2026-08-03,Refund,Food,0.05\n5,2026-08-03,Saving,Transfer,-30.00\n6,2026-09-01,Other,Food,-10.00\n"
        result = app("expenses").run(SimpleNamespace(input=self.input(data), month="2026-08"))
        self.assertEqual(result["summary"]["Net spending (USD)"], "0.25")
        self.assertEqual(result["summary"]["Cash remaining (USD)"], "99.75")

    def test_duplicate_transaction_ids_are_rejected(self):
        data = "id,date,description,category,amount\n1,2026-08-01,Food,Food,-1\n1,2026-08-02,Food,Food,-2\n"
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            app("expenses").run(SimpleNamespace(input=self.input(data), month="2026-08"))

    def test_empty_csv_produces_zero_report(self):
        result = app("expenses").run(SimpleNamespace(input=self.input("id,date,description,category,amount\n"), month="2026-08"))
        self.assertEqual(result["summary"]["Net spending (USD)"], "0.00")
        self.assertEqual(result["rows"], [])

    def test_invalid_and_short_csv_rows_are_rejected(self):
        for text in ("id,amount\n1,2\n", "id,amount\n1\n", "id,amount\n1,2,3\n", "id,amount\n,2\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                toolkit.read_csv(self.input(text), ["id", "amount", "category"] if text == "id,amount\n1,2\n" else ["id", "amount"])

    def test_money_rejects_nonfinite_subcent_and_huge_values(self):
        for value in ("NaN", "Infinity", "0.001", "abc", "1e99"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                toolkit.money(value)

    def test_dates_require_real_iso_calendar_dates(self):
        self.assertEqual(toolkit.iso_date("2024-02-29"), date(2024, 2, 29))
        for value in ("2026-02-29", "2026-13-01", "20260904"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                toolkit.iso_date(value)

    def test_invoice_aging_boundaries_and_partial_payments(self):
        reference = date(2026, 9, 4)
        lines = ["invoice_id,client,due_date,amount,paid"]
        for days in (0, 1, 30, 31, 60, 61, 90, 91):
            lines.append(f"I{days},Demo,{reference - timedelta(days=days)},100,25")
        result = app("invoices").run(SimpleNamespace(input=self.input("\n".join(lines)), as_of=reference))
        buckets = {row["Days overdue"]: row["Aging bucket"] for row in result["rows"]}
        self.assertEqual(buckets, {0: "Current", 1: "1-30", 30: "1-30", 31: "31-60", 60: "31-60", 61: "61-90", 90: "61-90", 91: "90+"})
        self.assertEqual(result["summary"]["Outstanding (USD)"], "600.00")
        self.assertEqual(result["summary"]["Overdue (USD)"], "525.00")

    def test_invoice_overpayment_rejected(self):
        data = "invoice_id,client,due_date,amount,paid\nI1,Demo,2026-09-04,100,101\n"
        with self.assertRaisesRegex(ValueError, "paid"):
            app("invoices").run(SimpleNamespace(input=self.input(data), as_of=date(2026, 9, 4)))

    def test_invoice_paid_is_omitted_and_future_is_current(self):
        data = "invoice_id,client,due_date,amount,paid\nI1,Demo,2026-01-01,100,100\nI2,Demo,2026-10-01,80,0\n"
        result = app("invoices").run(SimpleNamespace(input=self.input(data), as_of=date(2026, 9, 4)))
        self.assertEqual(len(result["rows"]), 1)
        self.assertEqual(result["rows"][0]["Aging bucket"], "Current")

    def test_inventory_rounding_incoming_stock_and_zero_demand(self):
        data = "sku,name,on_hand,on_order,daily_sales,lead_days,safety_stock\nA,Test,3,0,1.5,2,1\nB,Test,3,10,1.5,2,1\nC,Test,2,0,0,2,1\n"
        result = app("inventory").run(SimpleNamespace(input=self.input(data), review_days=1))
        by_sku = {row["SKU"]: row for row in result["rows"]}
        self.assertEqual(by_sku["A"]["Order units"], 3)
        self.assertEqual(by_sku["B"]["Order units"], 0)
        self.assertEqual(by_sku["C"]["Days on hand"], "No demand")

    def test_inventory_negative_stock_rejected(self):
        data = "sku,name,on_hand,on_order,daily_sales,lead_days,safety_stock\nA,Test,-1,0,2,3,1\n"
        with self.assertRaises(ValueError):
            app("inventory").run(SimpleNamespace(input=self.input(data), review_days=7))

    def test_support_security_precedence_and_multi_match_flag(self):
        queue, priority, reason, review = app("support").classify("Unauthorized login and a duplicate invoice")
        self.assertEqual((queue, priority, review), ("Security", "P1", True))
        self.assertIn("Billing", reason)

    def test_support_no_substring_matches(self):
        self.assertEqual(app("support").classify("I discharged a battery")[0], "General")

    def test_meeting_parser_preserves_missing_dates_and_source_line(self):
        text = "Discussion only\n- [ ] Maya | 2026-09-03 | Ship draft\n- [x] Alex | 2026-09-01 | Done\n- [ ] Unassigned | TBD | Review\n- [ ] malformed task\n"
        result = app("meetings").run(SimpleNamespace(input=self.input(text, "notes.md"), as_of=date(2026, 9, 4)))
        self.assertEqual(result["summary"]["Parsing warnings"], 1)
        self.assertEqual(result["summary"]["Open actions"], 2)
        self.assertEqual(result["rows"][0]["Line"], 2)
        self.assertEqual({row["Status"] for row in result["rows"]}, {"Overdue", "Done", "Needs date"})

    def test_campaign_encoding_replacement_and_fragment_preservation(self):
        url = app("campaigns").build_url("https://example.com/a?x=1&x=2&utm_source=old#signup", "Instagram", "Organic Social", "A&B", "Reel 1")
        parts = urlsplit(url)
        query = parse_qs(parts.query)
        self.assertEqual(query["x"], ["1", "2"])
        self.assertEqual(query["utm_source"], ["instagram"])
        self.assertEqual(query["utm_campaign"], ["a&b"])
        self.assertEqual(query["utm_medium"], ["organic social"])
        self.assertEqual(parts.fragment, "signup")

    def test_campaign_rejects_invalid_destinations(self):
        for url in ("javascript:alert(1)", "https://", "/relative", "https://user:pass@example.com", "https://example.com/a b"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                app("campaigns").build_url(url, "a", "b", "c")

    def test_job_match_word_boundaries_and_evidence(self):
        data = {"resume": "Used C++ and Python.\nStudied SQLite.", "job_description": "Need C++, SQL and Python", "skills": ["C++", "SQL", "Python", "python"]}
        result = app("jobmatch").run(SimpleNamespace(input=self.input(json.dumps(data), "job.json")))
        self.assertEqual(result["summary"]["Skills identified in posting"], 3)
        self.assertEqual(result["summary"]["Skills mentioned in resume"], 2)
        self.assertEqual(result["rows"][1]["Match"], "Missing")

    def test_no_job_skills_is_not_zero_employability(self):
        data = {"resume": "Python developer", "job_description": "Kitchen role", "skills": ["Python"]}
        result = app("jobmatch").run(SimpleNamespace(input=self.input(json.dumps(data), "job.json")))
        self.assertTrue(result["summary"]["Keyword coverage"].startswith("N/A"))

    def test_books_handles_missing_bibliography(self):
        path = self.input(json.dumps({"docs": [{"title": "Uncatalogued", "key": "/works/OL1W"}]}), "books.json")
        result = app("books").run(SimpleNamespace(input=path, live=False, query="ignored", limit=5))
        self.assertEqual(result["rows"][0]["Authors"], "Unknown")
        self.assertEqual(result["rows"][0]["First publication"], "Unknown")

    def test_books_live_query_uses_one_encoded_request(self):
        module = app("books")
        with patch.object(module, "fetch_json", return_value={"docs": []}) as fetch:
            module.run(SimpleNamespace(input=None, live=True, query="data & science", limit=3))
        self.assertEqual(fetch.call_count, 1)
        self.assertEqual(parse_qs(urlsplit(fetch.call_args.args[0]).query)["q"], ["data & science"])

    def weather_args(self, data):
        return SimpleNamespace(input=self.input(json.dumps(data), "weather.json"), live=False,
                               latitude=40.7128, longitude=-74.0060, max_rain=30, max_wind=25)

    def test_weather_nulls_are_unknown_and_threshold_is_inclusive(self):
        data = {"daily_units": {"temperature_2m_max": "°C", "precipitation_probability_max": "%", "wind_speed_10m_max": "km/h"},
                "daily": {"time": ["2026-09-04", "2026-09-05"], "temperature_2m_max": [20, None], "precipitation_probability_max": [30, None], "wind_speed_10m_max": [25, 10]}}
        result = app("weather").run(self.weather_args(data))
        self.assertEqual([row["Filming preference"] for row in result["rows"]], ["Fits", "Unknown"])

    def test_weather_rejects_mismatched_arrays(self):
        data = {"daily": {"time": ["2026-09-04"], "temperature_2m_max": [], "precipitation_probability_max": [], "wind_speed_10m_max": []}}
        with self.assertRaisesRegex(ValueError, "mismatched"):
            app("weather").run(self.weather_args(data))

    def test_weather_rejects_wrong_units(self):
        data = {"daily_units": {}, "daily": {"time": [], "temperature_2m_max": [], "precipitation_probability_max": [], "wind_speed_10m_max": []}}
        with self.assertRaisesRegex(ValueError, "units"):
            app("weather").run(self.weather_args(data))

    def test_different_location_never_silently_uses_nyc_sample(self):
        args = self.weather_args({})
        args.input, args.latitude = None, 51.5
        with self.assertRaisesRegex(ValueError, "require --live"):
            app("weather").run(args)

    def test_repo_missing_metadata_is_reviewed(self):
        data = {"full_name": "demo/repo", "html_url": "https://github.com/demo/repo", "license": None, "archived": True, "pushed_at": None}
        result = app("repocheck").run(SimpleNamespace(input=self.input(json.dumps(data), "repo.json"), live=False, repo="demo/repo", as_of=date(2026, 9, 4)))
        checks = {row["Check"]: row["Status"] for row in result["rows"]}
        self.assertEqual(checks["Detected license"], "Review")
        self.assertEqual(checks["Push recency"], "Unknown")
        self.assertEqual(checks["Archived"], "Review")

    def test_repo_path_cannot_add_api_segments(self):
        with self.assertRaisesRegex(ValueError, "owner/repository"):
            app("repocheck").run(SimpleNamespace(repo="owner/repo/issues", live=True))

    def test_snapshots_match_recorded_checksums(self):
        for project in CATALOG[-3:]:
            folder = toolkit.ROOT / "projects" / project["folder"]
            provenance = toolkit.read_json(folder / "provenance.json")
            self.assertEqual(hashlib.sha256((folder / "sample.json").read_bytes()).hexdigest(), provenance["sha256"])
            self.assertTrue(provenance["source_url"].startswith("https://"))

    def test_all_ten_demos_are_offline_and_write_complete_outputs(self):
        with patch("urllib.request.urlopen", side_effect=AssertionError("Unexpected network request")), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run.main(["demo", "--output-dir", str(self.path)]), 0)
        self.assertEqual(len(list(self.path.glob("*.json"))), 10)
        for project in CATALOG:
            data = toolkit.read_json(self.path / (project["id"] + ".json"))
            self.assertTrue(data["sources"])
            self.assertTrue((self.path / (project["id"] + ".prompt.md")).is_file())
            self.assertEqual((self.path / (project["id"] + ".md")).read_text(encoding="utf-8"), toolkit.markdown(data))

    def test_beginner_menu_runs_all_projects_and_recovers_from_bad_choices(self):
        choices = ["hello", "11", "0"]
        for number in range(1, 11):
            choices.extend([str(number), ""])
        choices.append("q")
        with patch("builtins.input", side_effect=choices), patch("urllib.request.urlopen", side_effect=AssertionError("Unexpected network request")), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(start.main(self.path), 0)
        self.assertIn("Please type a number from 1 to 10", output.getvalue())
        self.assertEqual(len(list(self.path.glob("*.json"))), 10)
        for project in CATALOG:
            self.assertIn(project["simple_title"].upper(), output.getvalue())

    def test_cli_invalid_json_returns_readable_error(self):
        path = self.input("not json", "invalid.json")
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(run.main(["jobmatch", "--input", str(path)]), 1)
        self.assertIn("Error:", errors.getvalue())
        self.assertNotIn("Traceback", errors.getvalue())

    def test_markdown_does_not_render_input_html_or_break_tables(self):
        text = toolkit.markdown(toolkit.report("Demo", {}, ["Text"], [{"Text": "<script>x</script>|next\nline"}]))
        self.assertNotIn("<script>", text)
        self.assertIn("&#124;", text)


class ClaudeAndNetworkTests(unittest.TestCase):
    def test_claude_requires_explicit_configuration(self):
        with patch.dict(os.environ, {}, clear=True), patch("urllib.request.urlopen") as fetch:
            with self.assertRaisesRegex(ValueError, "ANTHROPIC_API_KEY"):
                toolkit.ask_claude("sample")
            fetch.assert_not_called()

    def test_claude_request_contract_and_separate_text_response(self):
        response = MagicMock()
        response.read.return_value = json.dumps({"content": [{"type": "text", "text": "Review SKU A."}], "stop_reason": "end_turn"}).encode()
        opener = MagicMock()
        opener.__enter__.return_value = response
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake-test-key", "ANTHROPIC_MODEL": "test-model"}), patch("urllib.request.urlopen", return_value=opener) as fetch:
            result = toolkit.ask_claude("report facts")
        request = fetch.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.anthropic.com/v1/messages")
        self.assertEqual(request.get_header("X-api-key"), "fake-test-key")
        self.assertEqual(request.get_header("Anthropic-version"), "2023-06-01")
        body = json.loads(request.data)
        self.assertEqual(body["model"], "test-model")
        self.assertEqual(body["messages"][0]["content"], "report facts")
        self.assertIn("Review SKU A.", result)

    def test_claude_truncation_is_labeled(self):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake", "ANTHROPIC_MODEL": "fake"}), patch.object(toolkit, "fetch_json", return_value={"content": [{"type": "text", "text": "Partial"}], "stop_reason": "max_tokens"}):
            self.assertIn("truncated", toolkit.ask_claude("sample"))

    def test_http_errors_do_not_dump_secrets_or_response_body(self):
        error = urllib.error.HTTPError("https://example.com", 429, "rate limited", {}, io.BytesIO(b"sensitive response"))
        with patch("urllib.request.urlopen", side_effect=error), self.assertRaisesRegex(ValueError, "429") as raised:
            toolkit.fetch_json("https://example.com")
        self.assertNotIn("sensitive response", str(raised.exception))

    def test_network_timeout_explains_offline_fallback(self):
        with patch("urllib.request.urlopen", side_effect=TimeoutError()), self.assertRaisesRegex(ValueError, "offline sample"):
            toolkit.fetch_json("https://example.com")


if __name__ == "__main__":
    unittest.main()
