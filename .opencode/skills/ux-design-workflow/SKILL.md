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

Seven design stages, plus the handoff that hands implementation to another
agent. Each design stage produces an artifact, and each one ends at a gate: the
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
| 8 | Dev handoff | `ux-handoff` + main agent | `08-dev-handoff.md` | Package complete and ratified; the task is launched in the dev agent (`agentic-dev-boilerplate`) and **nothing is implemented here** |

Details, step-by-step instructions and templates per stage:
`references/stages.md`. Artifact skeletons: `references/artifacts.md`.

## Handoff to the dev agent (stage 8)

This console designs. Implementation — code, config, tests, build, deploy —
belongs to the dev agent configured in
`C:\Agentic-Quality-Engineer\Projects\agentic-dev-boilerplate`. When a design is
approved, stage 8 produces a package the dev agent can execute without a
meeting:

```
outputs/ux/<slug>/
  07-handoff.md          components, tokens, a11y, acceptance criteria
  08-dev-handoff.md      the task brief for the dev agent (see artifacts.md)
  03-wireframes/*.html   ratified screens — the dev agent treats these as the mockups
```

The dev agent's own rules make this the only viable path: it never invents UI,
it treats mockups as human-ratified artifacts, and it builds against a
`DESIGN.md` (Google Labs spec) at the product root. So stage 4 tokens and stage
7 components must be complete enough to become that `DESIGN.md`; if the user
wants the design system authored by the dev side, hand over the token table and
say so explicitly.

Launch it in the dev agent's repo with the package path as the only input:

> Read `outputs/ux/&lt;slug&gt;/08-dev-handoff.md` plus the files it lists, then
> implement screen by screen. Do not redesign; if something is missing, stop and
> ask.

Never re-implement inside this repo, not even "just this small fix" — a design
console that ships code stops being a design console.

## Narrative handoff (script + storyboard)

When the design depends on a story — a comic, a scroll narrative, a campaign
film, a character-led journey — the writing and the boarding belong to the
filmmaker console:

`C:\Agentic-Quality-Engineer\Projects\agentic-filmmaker-harness`
(`.opencode/skills/filmmaker/`, stages 0–2: treatment → screenplay → shot list +
storyboard + bible).

This console keeps the **narrative brief**: audience, chapters, what each
chapter must prove, the funnel, copy constraints, languages, and the panel
budget. It does not write the screenplay or draw the board.

```
outputs/ux/<slug>/
  08-filmmaker-handoff.md    narrative brief + beats + constraints (this repo)
```

The filmmaker agent writes into its own project folder
(`outputs/film/<slug>/01-screenplay.md`, `02-shotlist.md`, `02-storyboard/`,
`bible.md`). Adapt its shot vocabulary to the medium: for a web comic a "shot"
is a panel, the "camera" is the parallax layer stack, and the storyboard carries
layer breakdown and scroll position instead of lens and duration.

No pixels are generated from either side without a gate, and cloud generation
is the filmmaker console's call — never this one.



## Non-negotiables

- **Artifacts over edits.** Nothing here touches product code in another repo.
  Output is files in this repo (`outputs/ux/…`, `reports/`).
- **Design only, implementation is a handoff.** The moment a task means
  production code, config, tests, build or deploy, it goes to the dev agent
  (`agentic-dev-boilerplate`) with the stage-8 package. "Just this small fix"
  is how a design console turns into a bad code editor.
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
| "implement it" / "build it" / "code it" / "programá esto" | Stage 8 — package + hand over to the dev agent; never code here |
| "write the story" / "guion" / "storyboard" / "comic script" | Narrative handoff → filmmaker console (below) |
| "review the live page" | `ux-design-review` + `/playwright-cli` capture, then `ux-vision` |

## Fast paths

Small ask, single screen: compress to **0 → 3 → 6** (brief, wireframe, audit)
and say so. Never skip 0: a wireframe without a stated primary task is a
drawing.

Redesign of an existing product: **1 → 2 → 6 → 4 → 3**, because the audit tells
you what to fix and the wireframe proves the fix before visual work.
