# Audit method

## 1. Keys and matching

- Preferred key: the most granular pair that exists in the base ledger
  (document + line/item). If a stage export has no line number, fall back to
  document + item.
- Line numbers in exports are often unreliable: out of range, or valid but with
  a different item. Treat them as a hint, not as the key.
- Normalize before joining:
  - strip whitespace and zero-width characters;
  - unify full-width/half-width digits and parentheses;
  - keep internal separators (dots, dashes);
  - do not uppercase identifiers unless the source does.
- Report match rate per stage. Below 90% means the key is wrong or the export
  window is too narrow.

## 2. Aggregation

- Base ledger: one row per line. Multiple lines per document are normal.
- Stage documents may have several rows per key (split batches). Aggregate to
  key before comparing quantities.
- Monetary comparisons: sum only if the amount is repeated per row; if it is a
  document total repeated on every row, take the first value per document.
- Quantity comparisons: sum, but only within the same unit. Different units
  cannot be added; group by item/unit.

## 3. State matrix

For N stages, the state is the binary vector of "valid document exists".

- N=3 → 8 states, N=4 → 16.
- Name states by the stages present, not by number.
- Keep a configurable label map; the same vector may be "good" in one process
  (skipping a non-mandatory step) and "bad" in another.
- If a stage is optional, exclude it from the vector and record its presence as
  an attribute instead.
- Combinations with zero count are omitted from the detail sheets but listed in
  the summary.

## 4. Alternative paths

Some stages legitimately have no document:

- backflush / auto-consumption;
- direct transfer instead of a standard issue;
- free samples / zero-value orders;
- returns with a different upstream document;
- outsourced processing where material is supplied by the vendor.

Put these in `alternative_paths` and check the alternative source (e.g.
consumption quantity on the bill of materials). If the alternative source is not
exported, mark the line `not verifiable`, not `missing`.

## 5. Windows

- Record min/max date per file.
- Overlap = [max(min dates), min(max dates)].
- Lines outside the overlap cannot be judged for "missing later stage"; they may
  simply not have happened yet.
- Split conclusions into "within window" and "outside window" counts.
- Never write "no exceptions in the full population" when coverage is partial.

## 6. Closure

Closure is a separate dimension from document presence:

| Situation | Tag |
|---|---|
| Closed, no documents at all | `empty_closure` |
| Closed, completed quantity < ordered | `closed_incomplete` |
| Not closed, completed quantity >= ordered | `completed_not_closed` |
| Closed, execution status still open | `closed_incomplete_task` |
| Base status says not started, documents exist | `status_not_written_back` |

Apply in that order; do not attach both `empty_closure` and `closed_incomplete`.

## 7. Identifier corruption

Symptoms:

- A code column contains values like `2012-03-04`, `2012-03-05`.
- A text column became numeric and lost leading zeros.
- A long numeric ID shows scientific notation.

Recovery:

1. Collect all plausible original values from a reference column (item master,
   another export, the same table in an earlier period).
2. Generate candidates by interpreting the corrupted value (e.g. month.day).
3. Restore only when exactly one candidate matches.
4. List all unresolved values for the user; do not bulk-rewrite.

## 8. Cross-check implementation

```python
# state counts
assert len(detail) == len(base_lines)
assert detail["state"].notna().all()

# match rate
for stage in stages:
    rate = (detail[f"{stage}_docs"] > 0).mean()
    print(stage, f"{rate:.1%}")

# quantity reconciliation
assert abs(detail["completed_qty"].sum() - base["completed_qty"].sum()) < 0.01

# status write-back
mismatch = detail[(detail["base_status"] == "Not started") & (detail["issued_docs"] > 0)]
```

## 9. False positives to suppress

| Pattern | Why it is not a defect |
|---|---|
| Every line of one document shares the same stage document | Normal header-level linkage |
| A stage has zero quantity but a valid document | Zero-value / sample / correction |
| Completed quantity exceeds ordered by a tiny amount | Rounding or unit conversion |
| No later stage for an open, in-progress line | Not yet due |
| Missing upstream for a return/credit line | Reverse flow |
| Split lines look over-issued individually | Aggregate first |
| Old documents unmatched | Outside export window |

## 10. Output notes

Every output must state:

- base line count, document count, quantity;
- per-stage valid/invalid/excluded counts;
- matching keys and match rate;
- allocation count;
- window overlap;
- unresolved identifiers;
- which cross-checks passed and which did not.
