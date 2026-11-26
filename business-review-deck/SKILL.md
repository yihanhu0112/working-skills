---
name: business-review-deck
description: Turn period results, targets and project status into a review meeting deck — a message-led storyline, KPI and trend slides, gap analysis, risks and asks, roadmap or Gantt, and per-slide speaker notes. Use when the user asks for a monthly or quarterly review deck, a business review presentation, or talking points for each slide.
---

# Business review deck

A review deck is an argument, not a report. Every slide makes one claim and
supplies the evidence for it. If a slide cannot be summarised in a sentence, it
is two slides or none.

## 1. Configure

Copy `assets/config.example.yaml` to `config.yaml`: template file, review type,
period, audience, section list, tone, and output name.

Ask for: the template (or last period's deck), the data source, the period, the
audience's decision, and any page the user has already edited.

## 2. Pick the arc

**Arc A — performance review** (results + operations):

1. Cover
2. Agenda
3. Headline: period result, attainment, time progress, one-sentence judgement
4. Where the result came from: dimension decomposition
5. What is structurally true: mix, concentration, cohort
6. Cash / working-capital or operational view
7. Risks and dependencies
8. Asks: who provides what, by when
9. Next-period priorities
10. Closing

**Arc B — initiative review** (project or transformation):

1. Cover
2. Agenda
3. Headline: overall status, milestone, confidence
4. Workstream status: done / in progress / blocked
5. Timeline or Gantt
6. Key risks and mitigations
7. Cross-team dependencies and asks
8. Decisions required
9. Next milestones
10. Closing

Cut sections the audience does not need. Ten slides with a clear argument beats
twenty with a complete outline.

## 3. Write the storyline before the slides

For each slide, write one sentence: **the claim**, plus the evidence and the
implication.

```
Claim: <one sentence with a number>
Evidence: <chart/table/source>
Implication: <what the audience should do or decide>
```

If the claim needs two sentences, split the slide.

Order by argument, not by org chart:

- headline → cause → structure → risk → ask → next.
- Put the gap before the explanation, the explanation before the plan.

## 4. Slide patterns

| Pattern | Use | Content |
|---|---|---|
| Headline KPI | Open a section | 3–4 large numbers + one sentence |
| Waterfall / bridge | Explain a change | Start, drivers, end |
| Ranked bar | Compare units | Sorted, labelled |
| Trend line | Show direction | 4–8 periods, target line |
| Stacked bar | Show mix | 3–5 categories |
| Matrix / heatmap | Show two dimensions | Sparse labels |
| Table | Names and amounts | <= 8 rows |
| Gantt | Plan vs actual | Workstreams, milestones, status colour |
| Risk | Decision support | Risk, impact, mitigation, owner |

Rules: one chart per slide; title is the claim; no dual axes; no 3-D; label
values; put definitions in a footnote.

## 5. Template reuse

- Open the supplied template; do not create a new presentation.
- Reuse its master, fonts, colours, logo and footer.
- Keep the agenda after the cover and the closing slide last.
- Prefer native editable charts; use high-resolution images only when necessary.
- Do not edit the original file; save a new version.

## 6. Speaker notes

Write notes separately (not in the file unless asked):

- 150–300 words per slide, 1–2 minutes.
- Structure: what this slide says → key number → why it matters → what happens next.
- Spoken language, not written prose; do not read the slide.
- If the deck is long, get agreement on tone with the first three slides before
  writing the rest.

## 7. Iteration rules

- Read the latest version before editing; the user may have changed pages.
- Change only the pages the user names.
- When the user says "follow my version", their file wins over any earlier draft.
- Save as a new version; never overwrite the file the user edited.

## 8. Quality gates

- [ ] Every slide title is a claim, not a topic.
- [ ] Every claim has a number and a source.
- [ ] Text fits; no overflow, no clipped chart titles.
- [ ] Fonts did not fall back.
- [ ] Agenda matches section titles.
- [ ] Page numbers are continuous.
- [ ] Source and definitions are footnoted.
- [ ] The asks name a role, an action and a date.
- [ ] The original file is unchanged.

## 9. Pitfalls

- Starting from a blank deck and losing the corporate template.
- Cramming five points and two charts onto one slide.
- Showing data without a claim.
- Writing the plan before explaining the gap.
- Reading the slide in the notes.
- Reverting pages the user already edited.
- Calling a chart "editable" when it is a screenshot.
- Hiding a bad number in an appendix.

Slide blueprints and Gantt spec: [references/deck-blueprints.md](references/deck-blueprints.md).
