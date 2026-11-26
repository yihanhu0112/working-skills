---
name: rule-based-data-audit
description: Execute a written rule book against exported datasets, separating genuinely detectable defects from rules that are unverifiable or mis-specified, and produce a traceable findings register. Use when the user supplies audit rules and data exports and asks to scan for anomalies, exceptions, or data-quality issues.
---

# Rule-based data audit

The method is: **make every rule falsifiable, then refuse to over-claim.**

A rule book is a hypothesis about what "wrong" looks like. Data either supports
it, contradicts it, or cannot test it. The output must say which.

## 1. Read the rule book first

Extract for each rule: id, domain, entity, condition, required fields,
threshold, severity, owner role.

Then build a coverage matrix:

| Rule | Required fields | Available? | Executability |
|---|---|---|---|
| … | … | all / partial / none | executable / partial / unverifiable / suspect |

Four outcomes only:

- **Executable**: fields and definitions are clear.
- **Partial**: a sub-test is possible (e.g. check missing values but not format).
- **Unverifiable**: a required field or reference table is absent, or the
  document type was not exported.
- **Rule suspect**: the data contradicts the rule's premise (e.g. it flags most
  normal records, or the assumed format does not exist).

Report the last two to the user **before** producing a findings file.

## 2. Profile the datasets

For each export record: rows, distinct document IDs, date range, status
distribution, fill rate of every rule-referenced field, duplicate rows, total
rows, identifier types.

This profile is the evidence for "unverifiable" and for coverage limits.

## 3. Execute at the right grain

- Decide per rule whether the unit is a document, a line, or a value pair.
- Aggregate to that grain before evaluating; otherwise one-to-many joins inflate
  counts.
- Compare only within overlapping date windows.
- Use the configured status (e.g. approved) for validity; keep excluded records
  counted but out of the conclusion.
- For time rules, state which date is used (approval vs business date).

## 4. Suppress false positives

Before writing a finding, ask in order:

1. **Normal process?** Returns, samples, direct transfers, free-of-charge items,
   exempt materials, reverse flows.
2. **Field convention?** A field left empty by design, a different field carrying
   the same meaning, a code format that changed.
3. **Window?** The referenced document predates the export range.
4. **Grain?** Multi-line documents compared as whole documents.
5. **Rule premise?** The rule assumes a format or workflow that does not exist.

Each suppressed pattern goes into the report's "definitions and coverage"
section, with counts. Do not silently drop it.

## 5. Findings register

One row per finding, at the rule's grain. Core fields:

`id | domain | entity | rule_id | finding_type | key | date | object | quantity |
amount | description | evidence | probable_cause | owner_role | recommendation |
due_date | status | notes`

Rules:

- `evidence` is mandatory: file + row number or document ID.
- `description` states the comparison ("A is X, B is Y, difference Z").
- `probable_cause` is a hypothesis, labelled as such.
- `owner_role` is a role, not a person, unless the source provides one.
- `status` starts at `open`.
- No amount => leave blank; do not write 0.

## 6. Summary sheet

1. Scope: files, rows, documents, date ranges, status filter.
2. Rule execution table: rule, entity, finding type, count, verdict.
3. Findings by rule and severity.
4. Definitions and coverage: excluded normal flows, missing fields, window
   overlap, aggregation choices, unresolved identifiers.
5. Comparison with the previous run, if any: new, resolved, unchanged.

## 7. Report to the user

Fixed order:

1. Output path and counts.
2. Scope table.
3. Rule verdicts — including "normal, 0 findings".
4. 3–6 material findings, with key, count, and value.
5. 2–4 definition issues the user must decide before the next run.
6. Coverage limits.

Never lead with the raw number of findings; lead with which rules produced
material results and which did not.

## 8. Quality gates

- [ ] Every rule has a verdict, including "not verifiable".
- [ ] Every finding has evidence.
- [ ] Register counts reconcile with the summary.
- [ ] Normal flows are excluded and listed.
- [ ] Window-outs are labelled, not counted as defects.
- [ ] No fabricated values or placeholder rows.
- [ ] Each rule's grain matches its finding count.

## 9. Red lines

- Do not run a rule whose premise the data contradicts; report it instead.
- Do not turn a missing field into a zero.
- Do not report "no issues" when coverage is partial.
- Do not mix units or currencies in a total.
- Do not infer a person's name from a role.

Execution checklist: [references/execution-checklist.md](references/execution-checklist.md).
