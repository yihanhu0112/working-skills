# Analysis blueprint

## 1. Formulas

| Metric | Formula |
|---|---|
| Actual | Σ amount over the filtered period |
| Target | From the configured target table, same grain |
| Attainment | Actual / Target |
| Gap | Target − Actual |
| Share of gap | Unit gap / total gap |
| Time progress | Elapsed days / period days |
| Run rate | Actual / elapsed days × period days |
| Orders | nunique(order_id) |
| Average order | Actual / Orders |
| Customers | nunique(customer after normalization) |
| Revenue per customer | Actual / Customers |
| Quantity | Σ quantity (only if unit-consistent) |
| Average price | Actual / Quantity (single-product lines only) |
| Concentration | Top N amount / total |
| Cohort change | Current amount − prior amount, by customer |

State the date basis and currency once, at the top of the workbook.

## 2. Sheet blueprints

### 2.1 Attainment

Rows: dimension value. Columns: target, actual, attainment, gap, share of gap,
time progress, run-rate attainment. Add a total row.

Commentary: which unit is on track, which is behind, how much of the gap it
explains.

### 2.2 Decomposition

Two levels: dimension → owner/customer/product. Sort by absolute gap.

Commentary: the top two contributors to the gap, with amounts.

### 2.3 Mix

Rows: product/category. Columns: quantity, quantity share, amount (if reliable),
amount share, average price, prior-period change.

If amount is order-level, use quantity for mix and label it clearly.

### 2.4 Concentration

Rows: top N customers or products. Columns: amount, share, cumulative share,
orders, average order. Add a second block excluding one-offs.

Commentary: dependency risk; what happens to the trend without the top entity.

### 2.5 Cohort movement

Build a customer matrix: prior amount, current amount, change, status
(new / lost / reduced / flat / increased). Aggregate counts and amounts by
status and by dimension.

Commentary: how much growth came from new vs existing; how much was lost.

### 2.6 Price / volume

Decompose change: volume effect = Δqty × prior price; price effect = Δprice ×
current qty; mix effect = residual. Only valid when price and quantity are
reliable at the same grain.

Commentary: whether the change is volume-led or price-led.

### 2.7 Distribution

Buckets of order value (configurable). Columns: orders, order share, amount,
amount share, average order. Compare with prior period.

Commentary: shift toward small or large orders; what it implies for cost to
serve.

### 2.8 One-off adjustment

Table of excluded records: id, date, customer, amount, reason. Then reported vs
underlying trend, side by side.

Commentary: how much of the headline change is one-off; what the underlying
growth is.

### 2.9 Prior-period comparison

Same period length, same date basis, same customer normalization. Show absolute
and percentage change by dimension.

Commentary: what is structurally different, not just numerically different.

## 3. Commentary templates

### View-level

```
What the data says
- <metric> is <value> (<share/attainment>), <comparison>.
- <driver> contributes <amount> (<share of gap>).
- <risk> is <value>, <trend>.

Why
- Fact: <data-supported statement>.
- Hypothesis (to verify): <plausible cause>.

What to do
- <owner> to <action> by <date>.
```

### Unit-level

```
<Unit>: <actual> against <target> (<attainment>), ranked <N>.
Strength: <one data point>.
Weakness: <one data point and likely cause>.
```

Keep it to 2–3 sentences. Do not write a paragraph per KPI.

## 4. Data-model checks

- [ ] Amount placement decided (first line vs split).
- [ ] Order count deduplicated.
- [ ] Customer names normalized; aliases listed.
- [ ] Currency converted with a stated rule.
- [ ] Zero/negative rows classified.
- [ ] Product mix uses a reliable measure.
- [ ] Partial period flagged.
- [ ] One-off list explicit.

## 5. Visual rules

- Rank charts by the measure being discussed.
- Use one chart per question; no dual axes.
- Label values; do not rely on hover.
- A table beats a chart when names and amounts matter.
- Keep the same colour per dimension across the workbook.
