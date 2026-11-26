# Deck blueprints

## 1. Arc A: performance review

| Slide | Claim pattern | Content |
|---|---|---|
| Cover | — | Title, period, presenter, date |
| Agenda | — | 3–5 sections, matching slide titles |
| Headline | "Result is X, attainment Y%, Z points behind plan" | 3–4 KPI tiles + one sentence + one trend |
| Decomposition | "Unit A explains N% of the gap" | Ranked bars or waterfall by unit |
| Structure | "Top 3 accounts are N% of the period" | Concentration / mix / cohort |
| Cash or operations | "Outstanding is X, overdue Y%" | One KPI row + one chart |
| Risk | "Three risks could move the result by X" | Risk, impact, mitigation, owner |
| Asks | "We need A from B by C" | Role, action, date |
| Next | "Priorities for next period are X, Y, Z" | 3 priorities with owner |
| Closing | — | Thank you / contact |

## 2. Arc B: initiative review

| Slide | Claim pattern | Content |
|---|---|---|
| Cover | — | Initiative, milestone, date |
| Agenda | — | 3–5 sections |
| Headline | "Overall status is X; next milestone on track/at risk" | Status, milestone, confidence |
| Workstreams | "3 of 5 workstreams are on track" | Workstream, status, blocker |
| Timeline | "Milestone M2 slipped by N days" | Gantt or milestone line |
| Risks | "Two risks need a decision this week" | Risk, impact, mitigation, owner |
| Dependencies | "We need A from B to start C" | Team, dependency, date |
| Decisions | "Decision required on X by Y" | Option, recommendation, consequence |
| Next | "Next milestones are A, B, C" | Dates and owners |
| Closing | — | Thank you |

## 3. Slide construction rules

- Title = claim, 6–12 words, with a number where possible.
- Max 3 bullets, max 1 chart, max 8 table rows.
- A footnote carries the source and definition.
- Leave 10% white space; do not fill the page.
- Use the same colour per category across slides.
- Put detailed tables in an appendix and reference them, not on the main slide.

## 4. Gantt specification

- X axis: time. Near term by week/day, long term by month.
- Y axis: workstream or milestone.
- Bar states: done (dark), in progress (mid), not started (light), late (warning).
- Milestone: diamond with date.
- Show today's line only if the audience needs it.
- Label bars outside the bar (bars are often too narrow for text).
- Roll up to monthly granularity beyond the current quarter.

## 5. Speaker notes

Per slide:

```
This slide shows <claim>.
The key number is <number>, which <comparison>.
It matters because <impact>.
Next, <action / decision / owner>.
```

- 150–300 words.
- Say the number, not the chart legend.
- One idea per paragraph.
- Do not read bullets verbatim.

## 6. Build checklist

- [ ] Opened from the template, not a blank file.
- [ ] Master, fonts, logo, footer preserved.
- [ ] Agenda matches section titles.
- [ ] Every title is a claim.
- [ ] Every claim has a number and a source.
- [ ] Charts are native or >=200 dpi.
- [ ] No text overflow; chart titles not clipped.
- [ ] Tables do not split across pages.
- [ ] Closing slide present.
- [ ] Saved as a new file; original untouched.

## 7. Review pass

Before delivering, re-open the deck and inspect:

1. The three densest slides — read them at 100% zoom.
2. The chart with the most series — check labels and legend.
3. The table with the most rows — check row height and wrapping.
4. The smallest font — is it still legible in a meeting room?
5. Page count — can any slide be cut without losing the argument?

## 8. Common failure modes

| Failure | Fix |
|---|---|
| Topic titles ("Revenue") | Rewrite as claims ("Revenue is 8% below plan, driven by two accounts") |
| Too many points | Split or move to appendix |
| Chart without conclusion | Add a one-sentence takeaway above it |
| Plan before diagnosis | Move the plan after the gap explanation |
| Inconsistent units | One unit per slide, stated in the axis title |
| Hidden bad news | Surface it with context and a mitigation |
| Overwritten user edits | Always start from the latest file and change only named pages |
