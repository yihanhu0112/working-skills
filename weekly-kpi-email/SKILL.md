---
name: weekly-kpi-email
description: Generate a weekly KPI report email (Word/docx) from a transaction table and a target table, covering week-over-week change, period-to-date attainment, dimension and owner rankings, driver analysis, and data caveats. Use when the user asks for a weekly report, weekly KPI email, business update, or says to follow last week's email.
---

# Weekly KPI report email

Turn one week of transactions into a report a manager can send without editing.
The value is in the **definitions and the caveats**, not the layout.

## 0. Configure once

Copy `assets/config.example.yaml` to the working directory as `config.yaml` and
fill it in. Every column name, target, calendar rule and label comes from there;
nothing below is hard-coded to a company, currency or region.

If no config exists, ask the user for:

1. Data file and sheet.
2. Date column (and whether to use approval date or business date).
3. Amount column and currency.
4. Document ID column.
5. Dimension columns to report on (e.g. region, team, owner, customer).
6. Target source (file/sheet or a literal table) and its grain.
7. Week start day and fiscal year start.
8. Report title, greeting, sign-off.

## 1. Locate inputs

- **Data**: the transaction workbook. Prefer the newest file; confirm with the
  user if several versions exist.
- **Targets**: a separate table or a sheet in the same workbook. Target grain
  must match the report grain (period × dimension).
- **Template**: the previous week's email (`.docx`) or a written outline. If it
  exists, mirror its headings, table columns and sign-off; this file is the
  fallback.

Run `python -I ${CLAUDE_SKILL_DIR}/scripts/profile_excel.py "<file>"` first.

## 2. Validation gate

Report these before computing; do not silently "fix" data:

| Check | Action |
|---|---|
| Header row position | Detect; do not assume row 1 |
| Sheet name exactness | Trailing spaces are common |
| Duplicate document IDs | Deduplicate for counts; keep rows for amounts |
| Multi-row documents | Amount may be on the first row only |
| Negative rows | Keep, label as credit/return |
| Missing dates | Exclude from period metrics, report count |
| Missing amounts | Exclude from sums, report count |
| Mixed currencies | Convert with a stated rate or filter to one |
| Total rows | Remove before aggregating |

State the resulting row/document counts in the email's data-notes section.

## 3. Compute

Compute, at minimum:

- **Current week**: sum amount, distinct documents, valid documents
  (amount > 0), average per document.
- **Prior week and 4–5 week trend**: totals, average, high/low weeks.
- **Period to date** (month/quarter/year): actual, target, attainment, gap.
- **Time progress**: elapsed days / period days; compare with attainment.
- **Run rate**: remaining gap / remaining weeks.
- **Dimension ranking**: amount, share, change vs prior week.
- **Owner ranking**: period-to-date target, actual, attainment.
- **Concentration**: top 3 entities by amount and their share.
- **Drivers**: for each dimension, the top owners/customers and the amounts
  behind the change.

Formulas and edge cases: [references/metric-formulas.md](references/metric-formulas.md).

## 4. Write the email

Default structure (adapt to the template):

1. **Greeting** and one-paragraph summary: amount, change, documents, average.
2. **Week ranking by dimension** — one paragraph on the total and drivers, one
   on concentration, then a table.
3. **Recent-week trend** — narrative, bar chart with target line, then one
   bullet per dimension value.
4. **Period-to-date attainment** — narrative, target vs actual table, chart.
5. **Cumulative and annual target** — narrative, attainment table, gap and run
   rate, then owner ranking.
6. **Data notes** — definitions, exclusions, known source issues, action ask,
   sign-off and date.

Detailed skeleton and phrasing: [references/report-structure.md](references/report-structure.md).

Rules:

- Amounts in one unit with two decimals; percentages two decimals.
- Every claim carries a number; name the owner/customer only if the source does.
- Explain week-over-week change as "who + which account + how much".
- Manager view: size of gap, weeks left, weekly run rate required, who acts.
- No unquantified intensifiers.

## 5. Output

- File: `<report title>_<YYYYMMDD>.docx` next to the source or in the working
  directory; never overwrite the previous week.
- A4, 2 cm margins, East Asian font from config (default Microsoft YaHei
  10.5 pt), 1.45 line spacing, heading colour `1F3864`.
- Tables: header fill `1F4E79` white bold, total row `DDEBF7`, `Table Grid`.
- Charts: matplotlib, East Asian font configured, data labels, no top/right
  spines, 16 cm wide in the document.
- Reopen the document and check for overflowing tables, clipped charts and
  orphan headings.

## 6. Self-check

- [ ] Week boundaries match the configured calendar.
- [ ] Document count uses distinct IDs; amounts do not double-count split rows.
- [ ] Dimension sums equal the total (rounding tolerance stated).
- [ ] Month/quarter totals reconcile with the weekly series.
- [ ] Targets come from the configured source, not a previous email.
- [ ] Excluded rows and cross-period items are listed in data notes.
- [ ] Every percentage can be recomputed from the tables.
- [ ] Sign-off and date updated.

## 7. Pitfalls

- Grouping by a raw region column that has more values than the official
  reporting structure — use the configured mapping.
- Using business date when only the approval date is reliable for new records.
- Reading a sheet name with a trailing space and silently getting another sheet.
- Forgetting the total row and doubling the total.
- Counting zero-value samples in the average.
- Copying last week's targets or labels into this week's file.
