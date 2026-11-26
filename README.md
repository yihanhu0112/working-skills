# Reusable data & reporting skills

Six Claude Code skills that distil methods, not company data. Every skill is
configuration-driven: column names, targets, categories, calendars and output
labels come from a `config.yaml` you supply. There are no customer names, no
company names, no hard-coded targets and no historical figures in this repo.

## Skills

| Skill | What it does | Core method |
|---|---|---|
| `weekly-kpi-email` | Weekly report email from a transaction table + targets | Validate → compute week/period metrics → rank and attribute → state caveats |
| `document-flow-audit` | Audit a chain of documents against a base ledger | Match by key → detect stage presence → classify 2^N states → cross-check quantities |
| `rule-based-data-audit` | Execute a rule book and produce a traceable findings register | Translate rules → test executability → suppress false positives → evidence register |
| `receivables-dashboard` | Single-file AR dashboard | Separate aging from overdue → reconcile totals → exposure modules → narrative |
| `sales-performance-analysis` | Period analysis against targets and prior period | Model order lines → dual-basis attainment → decompose variance → cohort/one-off |
| `business-review-deck` | Review deck + speaker notes | Claim-led storyline → one message per slide → template reuse → QA pass |

## Design principles

1. **Config over constants.** No company, currency, region or target is assumed.
2. **Method over template.** Output structures are examples; the decision rules
   are the reusable part.
3. **Evidence over assertion.** Every finding cites a source or is labelled
   `not verifiable`.
4. **Read-only.** Skills never overwrite the source workbook or the user's deck.
5. **Ask when ambiguous.** Two plausible definitions → present both.

## Quick start

```powershell
# 1. Install skills (personal scope)
.\install.ps1

# 2. For each skill, copy its example config into your working folder
Copy-Item .\weekly-kpi-email\assets\config.example.yaml .\config.yaml
# edit config.yaml: file paths, sheet names, column names, targets

# 3. Inspect your workbook before running the method
python -I .\weekly-kpi-email\scripts\profile_excel.py "workbook.xlsx"
```

In Claude Code, run `/skills` to confirm loading, then ask for the task in
natural language (e.g. "write this week's KPI email using config.yaml").

## Repository layout

```
<skill>/
├─ SKILL.md                 method, steps, quality gates, pitfalls
├─ references/              detail loaded only when needed
├─ assets/config.example.yaml
└─ scripts/profile_excel.py  read-only workbook profiler
_shared/
├─ data-conventions.md      cross-skill reading/validation/delivery rules
└─ scripts/profile_excel.py
```

## What these skills deliberately do not contain

- Company or product names
- Customer, supplier or employee names
- Historical revenue, targets or margins
- Specific document numbers, part codes or account IDs
- Region lists, org structures or approval chains
- Vendor-specific ERP terminology

If you need a company-specific instantiation, keep it in your own private
`config.yaml` or a separate private repository.
