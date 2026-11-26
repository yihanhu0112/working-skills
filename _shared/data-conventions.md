# Shared data conventions

These rules apply to every skill in this repository. They contain no business
constants; every column name, target and category comes from the user's config.

## 1. Inspect before reading

```powershell
python -I scripts\profile_excel.py "workbook.xlsx"
```

Confirm:

1. Exact sheet names (trailing spaces matter).
2. Which row holds the header (title/merged rows often come first).
3. Duplicate or near-duplicate column names (`Amount` vs `Amount (CNY)`).
4. Value types: identifiers stored as dates, numbers stored as text, currency
   symbols, Unicode minus signs, thousands separators.

## 2. Read-only by default

- Open with `data_only=True`; never save over the source workbook.
- Convert explicitly: `pd.to_numeric(..., errors="coerce")`,
  `pd.to_datetime(..., errors="coerce")`. Keep failed rows in a separate list.
- Strip identifiers; do not strip meaningful separators inside them.
- Detect total/subtotal rows (usually the last 1–3 rows) before aggregating.

## 3. Validation gate

Before computing anything, check and report:

| Check | What to do |
|---|---|
| Duplicate primary keys | Decide: same record, or legitimate split rows? Ask if unclear |
| Multi-row documents | Amounts may appear only on the first row; sum rows, count distinct IDs |
| Negative amounts | Keep; label as credit/return; never silently drop |
| Missing dates | Exclude from period metrics; report count |
| Mixed currencies | Convert with a stated rate, or restrict to one currency |
| Zero-value rows | Exclude from averages, keep in counts; state the rule |
| Total rows | Remove before aggregation |
| Identifier corruption | e.g. `12.34.567` stored as a date; restore only when unambiguous |

## 4. Aggregation rules

- Sum amounts at row level unless the source repeats them per group.
- Count documents by distinct ID; count customers/entities by distinct name.
- When one entity has several rows, aggregate to the entity before comparing
  with another table.
- Compare like windows only. If exports cover different date ranges, restrict
  conclusions to the overlap and mark the rest `not verifiable`.

## 5. Evidence and uncertainty

- Every finding must cite a source file and row number (or document ID).
- Missing fields => `not verifiable`; never fabricate a value or a record.
- When two interpretations are equally plausible, present both and ask.
- A rule that flags a large share of normal records is probably a rule
  definition problem; report it before producing the output.

## 6. Delivery

- Write new files; never overwrite the source. Use a dated suffix.
- Excel: header fill `1F4E79` white bold, total row `DDEBF7`, frozen header,
  filters on, sensible column widths, thousands separators.
- Word: A4, 2 cm margins, configurable East Asian font (default Microsoft YaHei
  10.5 pt), 1.45 line spacing, heading colour `1F3864`.
- PowerPoint: reuse the supplied template/master; do not edit the original deck.
- Charts: label data points, drop top/right spines, use a colour-blind-safe
  palette, export at >=160 dpi or use native editable charts.

## 7. Language

- Numbers first, conclusion first; every judgement has a number behind it.
- Avoid unquantified intensifiers ("significantly", "dramatically").
- Keep methodology language neutral: no company, customer, product or person
  names belong in a skill file.
