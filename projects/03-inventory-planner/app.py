"""A simple reorder-point and order-up-to planner for a small shop."""
from decimal import ROUND_CEILING
from pathlib import Path

from toolkit import integer, number, read_csv, report, unique


def configure(parser):
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample.csv"))
    parser.add_argument("--review-days", type=int, default=7)


def run(args):
    if args.review_days < 0:
        raise ValueError("Review days cannot be negative")
    records = read_csv(args.input, ["sku", "name", "on_hand", "on_order", "daily_sales", "lead_days", "safety_stock"])
    unique(records, "sku")
    rows = []
    for record in records:
        on_hand, on_order, lead, safety = [integer(record[key], key) for key in ("on_hand", "on_order", "lead_days", "safety_stock")]
        daily = number(record["daily_sales"], "daily_sales", 0)
        point = int((daily * lead + safety).to_integral_value(rounding=ROUND_CEILING))
        target = int((daily * (lead + args.review_days) + safety).to_integral_value(rounding=ROUND_CEILING))
        position = on_hand + on_order
        reorder = position <= point
        quantity = max(0, target - position) if reorder else 0
        rows.append({"SKU": record["sku"], "Product": record["name"], "Stock position": position,
                     "Reorder point": point, "Order units": quantity,
                     "Days on hand": f"{on_hand / daily:.1f}" if daily else "No demand", "Status": "Reorder" if quantity else "OK"})
    rows.sort(key=lambda row: (-row["Order units"], row["SKU"]))
    return report("Inventory reorder planner", {"Products": len(rows), "Products to reorder": sum(row["Order units"] > 0 for row in rows),
        "Total suggested units": sum(row["Order units"] for row in rows), "Review interval (days)": args.review_days},
        ["SKU", "Product", "Stock position", "Reorder point", "Order units", "Days on hand", "Status"], rows,
        ["Fictional shop inventory. Reorder point = daily sales x lead days + safety stock, rounded up.",
         "Stock position = on hand + on order. When position <= reorder point, order up to lead time + review interval demand + safety stock.",
         "Assumes stable demand, no backorders and all on-order stock arriving in time. Orders are suggestions only; no purchasing integration."])
