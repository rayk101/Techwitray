# Inventory reorder planner

*Techwitray · practical projects to build with Claude*

- **Products:** 5
- **Products to reorder:** 2
- **Total suggested units:** 98
- **Review interval (days):** 7

| SKU | Product | Stock position | Reorder point | Order units | Days on hand | Status |
| --- | --- | --- | --- | --- | --- | --- |
| STK-03 | Sticker pack | 12 | 30 | 60 | 2.0 | Reorder |
| MUG-01 | Studio mug | 18 | 28 | 38 | 4.5 | Reorder |
| CAP-04 | Everyday cap | 25 | 15 | 0 | 5.0 | OK |
| PIN-05 | Enamel pin | 15 | 4 | 0 | No demand | OK |
| TEE-02 | Logo tee | 55 | 31 | 0 | 15.0 | OK |

## Notes

- Fictional shop inventory. Reorder point = daily sales x lead days + safety stock, rounded up.
- Stock position = on hand + on order. When position &lt;= reorder point, order up to lead time + review interval demand + safety stock.
- Assumes stable demand, no backorders and all on-order stock arriving in time. Orders are suggestions only; no purchasing integration.

## Sources

- [Shopify — Reorder point formula](https://www.shopify.com/blog/reorder-point)
