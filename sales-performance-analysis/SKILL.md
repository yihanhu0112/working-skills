---
name: sales-performance-analysis
description: Analyze a period of sales data against targets and a prior period — attainment on two bases, dimension and product mix, customer cohort movement, concentration, price/volume, one-off deal effects, and a written conclusion for each view. Use when the user asks for a period review, half-year or year-to-date analysis, variance versus last year, or a performance workbook.
---

# Sales performance analysis

The deliverable is not a pile of pivots. It is a small set of views that explain
**what changed, why, and what to do next**, with every claim traceable to data.

## 1. Configure

Copy `assets/config.example.yaml` to `config.yaml`: file, sheet, date and amount
columns, target source, dimensions, product/customer fields, prior-period
definition, and the exclusion list for one-off records.

If no config exists, ask for the reporting period, the target basis, the
dimensions to decompose, and which records are known one-offs.

## 2. Model the data first

Sales tables normally violate tidy-data rules. Establish:

- **Order line**: one row per product/category within an order.
- **Amount placement**: total order amount may sit only on the first line, or be
  split across lines when several owners share a deal.
- **Detection rule**: if several lines of one order carry amounts and they sum to
  the order total, treat them as a split; if only the first line carries it,
  treat the rest as zero.
- **Counts**: distinct order IDs for orders; distinct customer names for
  customers (after name normalization).
- **Dates**: one basis for the whole analysis (order or approval date).
- **Currency**: one reporting currency; state the conversion rule.

Never compute a product-mix amount by summing line amounts when the amount is
order-level; use quantity for mix, or allocate explicitly and label it.

## 3. Choose the views

Pick from this menu; each view must answer a question the user actually has:

| View | Question |
|---|---|
| Attainment | Did we hit the target? On which basis? |
| Dimension decomposition | Which unit drives the gap or the overachievement? |
| Mix | Which products/categories/segments explain the change? |
| Concentration | How dependent are we on the top entities? |
| Cohort movement | Are existing customers growing, shrinking, or lost? |
| New vs existing | Is growth coming from acquisition or penetration? |
| Price/volume | Is the change driven by quantity or price? |
| Distribution | Is the order-size profile shifting? |
| One-off adjustment | What does the underlying trend look like without exceptional deals? |
| Prior-period comparison | What is genuinely different from last period/year? |

## 4. Dual-basis attainment

If the target table has both a company-level target and a sum of unit targets,
compute both and explain the difference. A single number hides the most
important governance fact: whether targets are internally consistent.

## 5. Decompose the variance

For each dimension, report: target, actual, attainment, gap, share of total gap.
Sort by absolute gap, not by attainment — a small unit at 50% may matter less
than a large unit at 95%.

Then explain the gap with a second layer: owner, customer, product, or one-off
deal. Stop at the layer that yields an actionable name.

## 6. Cohort and concentration

- Existing customers = those with activity in the prior period; new = first
  activity in this period.
- Normalize names before matching (case, width, legal suffixes, group entities).
- Report lost, reduced, flat, increased, new: counts and amounts.
- Concentration: top 5/10 share, and the same share excluding one-offs.
- If a single customer or deal explains most of the change, say so explicitly.

## 7. One-off adjustment

Maintain an explicit exclusion list (order IDs or a rule). For each excluded
record, state the amount and why. Recompute the headline trend without them and
present both: reported and underlying.

Do not silently remove outliers. Do not call a legitimate large order an outlier
without business confirmation.

## 8. Commentary

Every view gets three blocks:

1. **What the data says** — 2–4 bullets, each with a number.
2. **Why** — separate fact from hypothesis; label hypotheses.
3. **What to do** — 1–3 actions naming a unit, customer group, or product.

Rules: conclusion first; one paragraph per dimension for qualitative reviews;
"strength + weakness" for unit-level comments; no unquantified intensifiers.

## 9. Output

- One workbook, one sheet per view, named by question (not Sheet1).
- Each sheet: title, data table, commentary block, source note.
- Consistent formats: money two decimals, percentages two decimals, totals.
- Optional chart per sheet; do not chart a table that is easier to read.
- Never modify the source workbook.

## 10. Quality gates

- [ ] Order counts use distinct IDs; line counts are labelled as lines.
- [ ] Amount sums reconcile to the source total.
- [ ] Dimension totals equal the grand total.
- [ ] Dual-basis attainment both shown, difference explained.
- [ ] One-off exclusions listed with amounts.
- [ ] Customer name normalization documented.
- [ ] Every commentary bullet has a number.
- [ ] Prior-period comparison uses the same period length and date basis.

## 11. Pitfalls

- Summing line amounts when the amount is order-level.
- Counting product mix by amount when only quantity is reliable.
- Comparing a partial period with a full prior period.
- Treating a renamed or restructured customer as both lost and new.
- Reporting attainment without the target basis.
- Explaining a gap with "market conditions" and no data.

View formulas and sheet layout: [references/analysis-blueprint.md](references/analysis-blueprint.md).
