# Metrics and module specifications

## 1. Definitions

| Term | Definition |
|---|---|
| Contract value | Total billed/contract amount in reporting currency |
| Collected | Cash received, by actual receipt date |
| Outstanding | Open balance, from the ledger's outstanding column |
| Collection rate | Collected / Contract |
| Due date | Contractual payment due date |
| Aging date | Start point configured: invoice, due, or order date |
| Aging days | As-of date − aging date, for outstanding rows |
| Overdue days | As-of date − due date, only when > 0 |
| Overdue amount | Outstanding where due date < as-of date |
| Expected receipt | Outstanding rows grouped by expected receipt date |

Aging and overdue are different views of the same balance. Both must reconcile
to the outstanding total.

## 2. Reconciliations

```
Σ outstanding (all rows) = outstanding total
Σ outstanding by dimension = outstanding total
Σ outstanding by category = outstanding total
Σ outstanding by aging bucket = outstanding total
Σ overdue + Σ not overdue + Σ no due date = outstanding total
Σ expected by month = outstanding rows with an expected date
```

If contract − collected ≠ outstanding, report the gap as a definition issue;
do not force it to zero.

## 3. KPI formulas

- Contract: Σ contract amount.
- Collected: Σ collected amount.
- Outstanding: Σ outstanding amount.
- Collection rate: collected / contract.
- Overdue: Σ outstanding where due date < as-of.
- Overdue share: overdue / outstanding.

Variants worth adding when the user asks: weighted average days outstanding,
top-10 concentration, collected this period vs target.

## 4. Module specs

### Collections by dimension

Stacked horizontal bar: collected and outstanding per dimension, sorted by
outstanding. Label the collection rate at the bar end.

### Outstanding share

Donut: outstanding per dimension. Label `name amount (share)`. Group slices
below the configured share into "Other"; list them in a table below.

### Category by delivery status

Rows = balance category; columns = delivered / not delivered. Two options:

- Stacked bar per category, split by delivery status.
- Grouped bars when the category count is small.

State which categories are "not delivered" and why.

### Aging

Bars by bucket (`0–30`, `31–60`, `61–90`, `91–180`, `180+`). Show amount and
row count. Use a single colour family; do not colour by severity here.

### Overdue

Same buckets, computed from the due date. Use a warning colour family. Show
amount and count. Add "no due date" as a separate note, not a bucket.

### Top debtors

Table: debtor, dimension, outstanding, share, document count, longest overdue,
earliest due date, owner. Include a total row. Never truncate names; wrap or
use a tooltip.

### Expected collections

Monthly bars from the current period to the horizon (e.g. year end). Label
amounts. Add a line for the period target if one exists.

### Period collections

Grouped bars or a table: dimension, expected, actual, attainment, gap. Define
the period (week/month/quarter) in the subtitle.

## 5. Layout

```
header (title, as-of, source)
KPI row (6)
two-column zone: exposure modules
full-width zone: category / aging / overdue
two-column zone: top debtors + expected collections
full-width: period collections
footer (definitions, reconciliation notes)
```

Responsive: one column below 900 px. Tables scroll, charts keep 16:9.

## 6. Chart rules

- Label values directly; hover is supplementary.
- Sort categories by the measure the module is about.
- One measure per axis; no dual axes.
- Pie/donut: max 6 slices; group the rest.
- Use currency units consistently across the page.
- Provide `title` and `aria-label` for every chart.

## 7. Data-quality checks before rendering

- Outstanding < 0: label as credit/overpayment; do not hide.
- Due date missing: report count; exclude from overdue.
- Expected date in the past but still outstanding: flag as "past expected".
- Actual receipt date after as-of: exclude from collected.
- Duplicate rows: decide whether they are split payments or duplicates.
- Foreign currency rows: convert with a stated rate or filter.

## 8. Narrative skeleton

```
As of <date>, contract value is <A>, collected <B>, outstanding <C>,
collection rate <P>%. Of the outstanding, <D> is overdue (<Q>%).

Exposure is concentrated in <dimension> (<share>) and in <category>
(<share>), which indicates cash is stuck at <stage>.

Top three debtors are <names>, together <amount> (<share>); the longest
overdue is <days> days.

Expected collections this period are <E>, against a target of <T>;
<gap> remains with <days> left.

Actions: <who> to <what> by <when>; <who> to <what>; <who> to <what>.
```
