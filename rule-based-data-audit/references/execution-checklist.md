# Execution checklist

## 1. Rule translation

For each rule write a sentence of the form:

> For every [entity] with [valid status] where [condition], flag it if
> [comparison] exceeds [threshold] using [field A] and [field B].

If you cannot fill every bracket, the rule is not executable yet.

Common missing pieces:

- Which date defines "age" or "delay".
- Whether the comparison is at document or line level.
- Whether zero/blank means "not applicable" or "missing".
- Whether the threshold is absolute or relative.
- Which status makes a record valid.

## 2. Grain

| Rule shape | Grain | Aggregation |
|---|---|---|
| "document has no upstream" | document | distinct upstream IDs per document |
| "line quantity differs" | document + item | sum by key before difference |
| "price differs" | document + item | compare unit prices, not totals |
| "time between stages" | document | first valid timestamp per stage |
| "count of X per Y" | Y | distinct X per Y |

If a rule mixes grains, split it into two rules; do not average them.

## 3. Joins

- Left join from the audited entity, not the other way round.
- Normalize keys before joining: trim, unify width, keep separators.
- One-to-many joins create duplicate rows; de-duplicate before counting.
- Report match rate. A low match rate is a data/window problem, not a finding.
- Unmatched reference records go to a separate sheet.

## 4. Time

- Choose one date basis and apply it to the whole run.
- Approval date is usually the right basis for "when did the record become
  effective"; business date is right for "when did the event happen".
- If business dates are backfilled, time-difference rules can go negative.
  Detect negative durations and report them as a data issue.
- "Overdue" needs an as-of date. Default to today; state it.

## 5. False-positive checklist

Run this list for every rule with a non-trivial hit count:

- [ ] Reverse flow (return, credit, reversal).
- [ ] Free / sample / zero-value.
- [ ] Exempt or alternative path.
- [ ] Field intentionally blank.
- [ ] Code/format changed over time.
- [ ] Reference record outside export window.
- [ ] Multi-line document compared as one line.
- [ ] Unit or currency mismatch.
- [ ] Duplicate export rows.
- [ ] Rule threshold set for a different process variant.

If two or more apply, the rule needs a qualifier before it can be used.

## 6. Evidence format

`file!row` is preferred. If row numbers shift, use a stable key plus the value:

```
orders.xlsx!R4821 | Order O-1042 | received 80 vs ordered 100
```

Never cite only "the system" or "the export". A reviewer must be able to reopen
the source and see the same value.

## 7. Severity

Use three levels, defined by consequence, not by count:

- **High**: affects money, compliance, or a downstream process.
- **Medium**: affects reporting accuracy or requires rework.
- **Low**: cosmetic, master-data hygiene, single-record typos.

Do not label everything high; a register where 90% is high is unusable.

## 8. Coverage statement

For every run, state:

```
Files: N; rows: R; documents: D; period: A..B
Status filter: approved only (excluded S rows)
Overlap window: C..D
Rules: total T, executable E, partial P, unverifiable U, suspect X
Findings: F rows / K documents
Limits: missing fields, unexported documents, unmatched keys
```

## 9. Reconciliation

- Findings by rule sum to total findings.
- Distinct keys in the register <= distinct keys in the audited data.
- Amount totals in findings <= audited amount (unless the same amount is
  intentionally counted under several rules; then say so).
- Every `unverifiable` rule appears in the summary, not in the register.
