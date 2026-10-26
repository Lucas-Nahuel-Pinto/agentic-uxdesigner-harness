---
name: ux-design-workflow
description: >
  End-to-end UX design workflow for a product or feature: discovery and
  research synthesis, information architecture and user flows, wireframes,
  UI direction and tokens, usability testing, UX/accessibility audit, and
  design handoff. Use for "diseñar la UX de", "armá el workflow de diseño",
  "plan de UX", "research plan", "arquitectura de información", "user flow",
  "usability test", "test de usabilidad", "design handoff", "spec de diseño",
  "design system", "tokens", or when a design request needs more than a
  single screen mocked. Orchestrates the repo's skills and subagents; each
  stage ends at a gate the user approves.
---

# ux-design-workflow

Seven stages. Each one produces an artifact, and each one ends at a gate: the
next stage does not start until the artifact satisfies its exit criteria and
the user approves. Cheap to change at stage 1, expensive at stage 7 — that is
why the order is not negotiable.

## Artifact home

```
outputs/ux/<project-slug>/        working artifacts (gitignored — never committed)
  00-brief.md
  01-discovery.md
  02-ia-flows.md
  03-wireframes/                  *.html + manifest
  04-ui-direction.md
  05-usability-test.md
  06-audit.md
  07-handoff.md
reports/                          only the deliverables the user asks to keep
```

`outputs/` is gitignored by repo rule: artifacts are per-project work, not repo
content. When the user wants something preserved as a deliverable, copy that
single file into `reports/`.

## Stages

| # | Stage | Owner | Artifact | Exit gate |
|---|---|---|---|---|
| 0 | Brief | main agent, with the user | `00-brief.md` | Problem, users, constraints and the success signal in one page; every unknown listed as an open question |
| 1 | Discovery | `ux-research` subagent | `01-discovery.md` | JTBD, personas/segments, journey with pain points, assumptions ranked by risk; every claim tagged evidence / assumption / unknown |
| 2 | IA & flows | `ux-architect` subagent | `02-ia-flows.md` | Sitemap + primary flow (diagram) + screen inventory with states; each screen has one primary task and a defined entry/exit |
| 3 | Wireframes | `ux-wireframe` subagent | `03-wireframes/` | Every inventory screen exists as a clickable screen, default + empty/loading/error states, flow navigable end to end |
| 4 | UI direction | main agent (`impeccable`, `ui-ux-pro-max`) | `04-ui-direction.md` | Visual language chosen against the brief, tokens defined (color, type scale, spacing, radius, motion), contrast pairs pass |
| 5 | Usability test | main agent + `ux-review` | `05-usability-test.md` | Task list, script, environments, scoring rubric; findings synthesized with severity and a fix each |
| 6 | Audit | `ux-review` / `ux-design-review` | `06-audit.md` | Ranked findings (blocker → polish), every one cited to a heuristic or WCAG rule, blocking vs polish separated |
| 7 | Handoff | `ux-handoff` subagent | `07-handoff.md` | Components with states, tokens, a11y requirements, acceptance criteria, open decisions — enough for a developer to build without asking |

Details, step-by-step instructions and templates per stage:
`references/stages.md`. Artifact skeletons: `references/artifacts.md`.

## Non-negotiables

- **Artifacts over edits.** Nothing here touches product code in another repo.
  Output is files in this repo (`outputs/ux/…`, `reports/`).
- **No stage ships on vibes.** Every statement is evidence, assumption or
  unknown — labelled. Stage artifacts carry a short `## Evidence` section.
- **Accessibility is a stage input, not a final pass.** WCAG checks start at
  wireframe time (labels, focus order, contrast pairs, target sizes).
- **The gate is the user's.** Present the artifact, name what is weak, ask.
  A skipped gate is only valid if the user explicitly says so; record it in
  the artifact header as `Gate: skipped by user`.
- **One artifact per stage.** No shadow docs; if something changes, edit the
  stage artifact so history stays readable through git-less filenames
  (`00-`, `01-`, …).
- **Language:** talk to the user in their language (caveman register by
  default in this repo); write artifacts in normal English unless the user
  asks for Spanish.

## Routing cheatsheet

| The user says | Do |
|---|---|
| "design the UX for X" / "diseñá la UX de X" | Stage 0 → 1, ask for the brief inputs first |
| "who is this for" / "research this market" | `ux-research` |
| "how should this flow" / "map the screens" | `ux-architect` |
| "wireframe it" / "mockup rápido" | Stage 3 only, after a minimal brief |
| "make it look good" / "redesign the visuals" | Stage 4 (`impeccable`), requires 1–3 |
| "test it with users" | Stage 5 |
| "is this usable" / "revisá el diseño" | Stage 6 (`ux-design-review`) |
| "spec it for dev" / "handoff" | Stage 7 (`ux-handoff`) |
| "review the live page" | `ux-design-review` + `/playwright-cli` capture, then `ux-vision` |

## Fast paths

Small ask, single screen: compress to **0 → 3 → 6** (brief, wireframe, audit)
and say so. Never skip 0: a wireframe without a stated primary task is a
drawing.

Redesign of an existing product: **1 → 2 → 6 → 4 → 3**, because the audit tells
you what to fix and the wireframe proves the fix before visual work.
