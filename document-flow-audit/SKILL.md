---
name: document-flow-audit
description: Audit a chain of business documents (request, approval, issue, execution, receipt, settlement) against a base ledger, compute per-line stage coverage, classify each line into a completeness state, and output a summary plus line-level evidence workbook. Use when the user provides several document exports and asks whether each record was issued, consumed, reported, received, reconciled or closed.
---

# Document-flow audit

Given a base ledger (orders, work orders, projects, tickets) and a set of
follow-on documents, answer three questions per line:

1. **How far did this line get?**
2. **Which stage has no valid document?**
3. **Is the gap a real process break, a missing export, or a definition issue?**

## 0. Configure once

Copy `assets/config.example.yaml` to the working directory as `config.yaml`.
It defines the base ledger, each stage, the join keys and the valid statuses.
No entity name, stage name or quantity column is hard-coded.

If no config exists, ask for:

1. Base ledger file/sheet and its key columns.
2. Which statuses count as valid (e.g. approved, posted).
3. Stage list, in order, each with its files, join keys, quantity field and
   document-ID field.
4. Business key to match on when line numbers are unusable.
5. Quantity units and whether they can be summed across lines.
6. Output language, labels and file name.

## 1. Inspect and validate

Run `python -I ${CLAUDE_SKILL_DIR}/scripts/profile_excel.py` on every file.

Record for each file: row count, distinct document count, date range, status
distribution, key column fill rate, total rows, duplicate keys.

Gate:

- Only **valid statuses** count. List the excluded statuses and their counts.
- Normalize identifiers: strip whitespace; detect identifiers corrupted into
  dates or numbers; restore only when unambiguous.
- If the base ledger has multiple rows per document, every document-level
  comparison must aggregate to document + line item first.
- If exports start on different dates, compute the overlap window and restrict
  conclusions to it; mark the rest `not verifiable`.

## 2. Build the line ledger

One row = base key (e.g. document + line/item). Left-join every stage.

Matching rules, in priority order:

1. Exact key match on the configured keys.
2. If the stage has no line number, match on document + item key.
3. If one item is split across several base lines, allocate the stage quantity
   evenly and mark `allocation = even`; do not use allocated quantities for
   monetary conclusions.
4. Unmatched stage documents go to an `unmatched` sheet, not into the base.

Record a `match_method` column per line: `key`, `item`, `allocated`, `none`.

## 3. Classify each line

For each stage, define a boolean: does a valid document exist for this line?

With N stages you get 2^N states. For 3 stages the matrix is:

| State | Stage 1 | Stage 2 | Stage 3 | Meaning |
|---|---|---|---|---|
| 0 | no | no | no | not started |
| 1 | yes | no | no | stage 1 only |
| 2 | no | yes | no | out of order |
| 3 | yes | yes | no | waiting for stage 3 |
| 4 | no | no | yes | stage 3 without stage 1 |
| 5 | yes | no | yes | stage 2 skipped |
| 6 | no | yes | yes | stage 1 skipped |
| 7 | yes | yes | yes | complete |

Use the configured stage labels in the output, not numbers alone.
If N > 4, group rare combinations and report only combinations with counts > 0.

## 4. Anomaly tags

Tag each line (multiple tags allowed):

| Tag | Rule |
|---|---|
| `empty_closure` | Record closed but no valid document at any stage |
| `closed_incomplete` | Closed, but quantity completed < quantity ordered |
| `completed_not_closed` | Full quantity completed, record still open |
| `closed_incomplete_task` | Task/execution not finished but record closed |
| `status_not_written_back` | Base status says "not started" while valid documents exist |
| `missing_upstream` | A later stage exists without the earlier stage |
| `over_quantity` | Stage quantity > ordered quantity, after key aggregation |
| `zero_effort` | Valid execution document with zero hours/quantity |
| `out_of_order` | Stage timestamps precede the upstream document |
| `unmatched_document` | Stage document cannot be matched to the base |
| `identifier_corrupt` | Identifier stored as a date/number |

Rules:

- Apply mutually exclusive closure tags in order: `empty_closure` →
  `closed_incomplete` → `completed_not_closed`.
- Aggregate to key before quantity comparisons; otherwise split lines produce
  false over-quantity flags.

## 5. Cross-checks (must pass or be explained)

1. Σ state counts = base line count.
2. Match rate per stage.
3. Σ completed quantity = base ledger's written-back completed quantity.
4. Σ execution effort (hours/quantity) = written-back effort.
5. Σ issued quantity vs required quantity (over/under issue).
6. Status written back vs existence of valid documents.
7. Closure flag vs completion condition.
8. Unmatched documents count and value.
9. Unit consistency (do not add pieces to kilograms).

## 6. Output workbook

File: `<flow-audit>_<YYYYMMDD>.xlsx`.

| Sheet | Content |
|---|---|
| `00_readme` | Scope, file list, row/document counts, date ranges, key and match method, state definitions, caveats |
| `01_summary` | State matrix with counts/share/closed/quantity; cross-check results |
| `02..` | One sheet per state with rows present, same columns as summary detail |

Detail columns (adapt names via config): base keys, entity, ordered quantity,
completed quantity, base status, per-stage document count / line count /
quantity / effort, state, tags, evidence, notes.

Format: frozen header, filters, colour by state, column widths fitted.

## 7. Report

1. One-line conclusion: how many lines/documents/quantity audited, where the
   main gap is.
2. State table with counts and share.
3. 3–5 findings, each with key, line count, quantity, and the missing stage.
4. Data issues: identifier corruption, unusable line numbers, allocation,
   window mismatch.
5. File path and sheet structure.

No stage-by-stage narration; lead with the largest gap and who should act.

## 8. Red lines

- Only valid statuses count; excluded statuses are reported, not ignored.
- Never treat a valid later-stage document as evidence of an earlier stage.
- If a stage has an alternative path (e.g. backflush, auto-consumption), define
  it in config and check the alternative source instead of flagging missing.
- Window-outs are `not verifiable`, never `missing`.
- Never fabricate a document or a zero value to make a line look complete.
- Aggregate before comparing quantities.

Method details: [references/audit-method.md](references/audit-method.md).
