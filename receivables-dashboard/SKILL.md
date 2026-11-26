---
name: receivables-dashboard
description: Build a single-file HTML accounts-receivable dashboard from an AR ledger — contract, collected and outstanding amounts, collection rate, aging and overdue distribution, top debtors, balance categories, expected collections and period collections. Use when the user asks for an AR dashboard, collections panel, aging view, or receivable visualization.
---

# Receivables dashboard

The dashboard answers four questions: **how much is outstanding, how old is it,
who owes it, and when will it come back.** Everything else is decoration.

## 1. Configure

Copy `assets/config.example.yaml` to `config.yaml`. It defines the ledger file,
the amount/date/category columns, the aging buckets and the module order.

Ask for: amount columns (contract / collected / outstanding), due-date column,
expected-date column, actual-date column, category column, customer/region/
owner columns, currency, aging start point, buckets, and the reporting period.

## 2. Define before aggregating

- **Contract** = contract value in one currency.
- **Collected** = cash actually received.
- **Outstanding** = the ledger's outstanding amount; do not derive it as
  contract − collected unless the user confirms that identity holds.
- **Aging start** is configurable (invoice date, due date, order date). State it.
- **Overdue** is separate from aging: overdue uses the due date; aging uses the
  aging start. Never merge the two into one chart.
- One invoice/order may have several payment rows. Sum rows for amounts; count
  distinct IDs for document counts.
- Exclude write-offs, notes and internal transfers unless explicitly included.

Reconcile first: Σ outstanding by dimension = total outstanding, and
Σ collected + Σ outstanding = contract value (or the difference has a stated
reason). If it does not reconcile, fix the definition before building the page.

## 3. KPI row

Six tiles, each with value, share or comparison, and a one-line definition:

1. Contract value
2. Collected
3. Outstanding
4. Collection rate (collected / contract)
5. Overdue amount
6. Overdue share (overdue / outstanding)

Add "as of" date and source file in the header.

## 4. Modules

Keep modules that answer a decision; drop the rest:

| Module | Question | Chart |
|---|---|---|
| Collections by dimension | Where is cash coming from? | Stacked bar (collected vs outstanding) |
| Outstanding share by dimension | Where is the exposure concentrated? | Pie/donut with amount + share labels |
| Balance category by delivery status | Which stage is cash stuck at? | Stacked bar or grouped bars |
| Aging distribution | How old is the debt? | Bars by bucket |
| Overdue distribution | How late is it? | Bars by overdue bucket |
| Top debtors | Who to call first? | Table, not a chart |
| Expected collections by period | What should arrive next? | Monthly bars |
| Period collections by dimension | Who performed this period? | Grouped bars or table |

Order is configurable. Two principles:

- Exposure modules go above detail modules.
- A table is better than a chart when the user needs names and amounts.

## 5. Build

- One HTML file, data embedded as JSON, works from `file://`.
- No CDN or network dependency; build charts with inline SVG or inline a small
  renderer. A blank page almost always means a chart library failed to load.
- Responsive: single column below 900 px; tables scroll horizontally.
- Label every pie/bar with amount and share; do not require hover to read a
  key number.
- Use a colour-blind-safe palette; do not encode the only distinction by colour.
- Format money in one unit (thousands or millions) with two decimals.

## 6. Narrative

Separate 3–5 paragraphs:

1. Total and rate; one-sentence judgement.
2. Structural concentration (dimension, stage).
3. Risk (overdue amount, top debtors, longest delay).
4. Expected collections vs the period target.
5. Two or three actions naming a dimension or debtor group.

No adjectives without a number.

## 7. Quality gates

- [ ] KPI values recomputable from the ledger.
- [ ] Dimension totals equal the grand total.
- [ ] Category totals equal outstanding (or difference explained).
- [ ] Overdue + not overdue = outstanding (no-due-date rows listed separately).
- [ ] Aging buckets sum to outstanding.
- [ ] Expected collections sum to the dated outstanding balance.
- [ ] No `NaN`, `undefined`, blank charts or clipped labels.
- [ ] Page readable at phone width.

## 8. Pitfalls

- Using expected date as actual receipt date (or vice versa).
- Deriving outstanding by subtraction when the ledger has its own column.
- Counting payment rows as documents.
- Treating write-offs or notes as cash.
- Mixing currencies without a stated rate.
- One customer with several spellings splitting the top-10.
- Pie labels overlapping because small slices were not grouped.

Formulas and module specs: [references/metrics-and-modules.md](references/metrics-and-modules.md).
