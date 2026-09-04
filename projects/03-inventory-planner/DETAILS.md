# 03 · Inventory reorder planner

**Medium · 3–5 hours to rebuild and customize** · [All projects](../../README.md)

Help a small shop spot products that need replenishment.

[Source code](app.py) · [Sample input](sample.csv) · [Example report](../../examples/inventory.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py inventory --review-days 7
```

Reports are written to output/inventory.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

## Use your own input

CSV: sku,name,on_hand,on_order,daily_sales,lead_days,safety_stock. Counts and days are nonnegative integers; daily_sales can be fractional. No backorders.

```bash
python run.py inventory --input path/to/your-file.csv
```

## What the code does

Computes ceil(daily_sales × lead_days + safety_stock). At or below that point, suggests enough units to cover lead_days + review_days plus safety stock. On-order units count toward stock position.

## Reel demo

Show Sticker pack: reorder point 30, stock position 12, suggested order 60 units.

## Claude analysis

Write a purchasing review note explaining the three largest suggested orders. Cite SKUs and exact quantities; distinguish demand assumptions from observed stock. Do not place orders or claim the quantities are optimal.

Copy output/inventory.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Calculate average demand from dated sales history and model incoming shipment dates. Add supplier minimum order quantities.

## Sources and scope

- [Shopify — Reorder point formula](https://www.shopify.com/blog/reorder-point): Reorder point = demand during lead time + safety stock. Our review-interval order-up-to policy is an explicit project design choice.

Review the notes in the [example report](../../examples/inventory.md) for assumptions and limitations.
