# Use these projects with Claude

## Build and learn

Every project folder contains a `PROMPT.md` with its exact input format, acceptance criteria, source links and next feature. Paste it into Claude with the code files available. If you use Claude Code in the repository, point it to the chosen project and read `CLAUDE.md` first.

A useful first request is: “Explain this project's input, calculation and output. Walk me through one sample row, then help me implement the suggested extension.” Keep a change you understand and rerun the tests.

## Analyze a report through chat

Run a project, then paste its generated prompt into Claude:

```bash
python run.py inventory
```

Open `output/inventory.prompt.md`. It includes the actual calculated report and a request to explain the suggested orders. No model call happens while generating this file. Redact personal, client or confidential data before pasting your own reports into a hosted model.

## Optional Claude API

The optional client uses Anthropic's [Messages API](https://platform.claude.com/docs/en/api/messages/create), with the documented [authentication and version headers](https://platform.claude.com/docs/en/api/overview). It requires an Anthropic API key and a model ID available to your account. Choose the model from your account's current model list; the code deliberately does not hard-code an aging model name.

PowerShell:

```powershell
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key" -MaskInput
$env:ANTHROPIC_MODEL = Read-Host "Available Claude model ID"
python run.py inventory --claude
```

`-MaskInput` requires PowerShell 7.1+. If your shell does not support it, set the environment variable through your normal secret manager or terminal environment settings rather than saving a key in a script.

macOS/Linux (bash):

```bash
read -s -p "Anthropic API key: " ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY
read -p "Available Claude model ID: " ANTHROPIC_MODEL
export ANTHROPIC_MODEL
python3 run.py inventory --claude
```

This writes `output/inventory.claude.md` alongside the original Markdown, JSON and prompt. Model responses are drafts and can be wrong. Exact amounts and dates are computed by Python before any model call. Truncated model responses are labeled.

`--claude` sends the generated report and analysis request to Anthropic. The report can contain client names, ticket subjects or resume evidence when you supply personal input. Without `--claude`, those reports stay local unless you share them yourself. API usage can incur charges; a Claude chat subscription does not configure this project's API access.

No `.env` loader or SDK is required. The program reads process environment variables only. A `.env.example` is a reference, not an automatically loaded file. Do not put keys in Git, prompts or sample data.

## Current limits

- Core calculations, offline demos and request/response handling are tested locally. The initial paid Anthropic call was not run because no key was supplied for this work.
- The model receives the report, not the full original files or the contents of linked sources. It should not claim to have inspected missing context.
- The client performs a single request with a timeout and reports HTTP errors. It does not retry paid requests automatically or provide streaming.
- Generated drafts do not send emails, modify tickets, create calendar entries, place orders or update repositories.
