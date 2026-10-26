# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The agent operator running an OpenCode session on this console. The operator invokes
skills by name and consumes the artifacts the agent produces (UX review reports,
standalone HTML wireframes). Downstream human designers or clients
may read the outputs, but the operator is the primary user.

## Product Purpose

A console that equips one agent with a repeatable UX-designer workflow: discovery
synthesis, information architecture and flows, wireframes, UI direction and tokens,
usability testing, heuristic/accessibility audits, and design handoff. Success means
each stage can be requested on demand, produces a reviewable artifact, and is
delivered without ever touching product code.

## Positioning

A curated, opinionated console — not a generic coding agent with design plugins.
Its differentiator is the packaged workflow itself: a Nielsen + WCAG review rubric
and wireframe recipes, so results are reproducible. Audio, video and film
generation are out of scope (moved out on 2026-10-25).

## Operating Context

- OpenCode agent console; skills invoked by name (`/ux-design-workflow`,
  `/ux-design-review`, `/ux-wireframe`, plus vendored caveman, git-flow-master,
  img2threejs, impeccable); `/ux` enters the pipeline.
- MCPs: `engram` (persistent memory, env read at session start; `engram` must be on
  PATH) and `tavily` (web search).
- Saved design reviews go in `reports/` only when requested; wireframes are
  standalone HTML files in this repo.

## Capabilities and Constraints

- Skills: `ux-design-workflow` (7-stage pipeline with a user gate per stage,
  artifacts in `outputs/ux/<project>/`), heuristic UX audit (Nielsen + WCAG
  baseline, ranked findings, read-only), standalone HTML wireframes/clickable
  mockups, plus git operator and terse-voice vendored skills.
- Subagents: `ux-research` (1), `ux-architect` (2), `ux-wireframe` (3),
  `ux-review` (5-6), `ux-vision` (render inspection), `ux-handoff` (7).
- Operating rules that future work must preserve:
  - Credentials ALWAYS from `.env` (template `.env.example`); never hardcoded.
  - MCP or auth failure = STOP, name the missing env var, no workarounds
    (`opencode.jsonc` substitutes `{env:VAR}` silently — a 401/403 is the signal).
  - Design reviews and wireframes NEVER modify product code.
  - Git/PR work follows git-flow-master: semantic commit prefixes, no AI
    attribution, confirm before push, never rewrite pushed history; generated
    files (`outputs/`, `*.wav`, `*.png`) are never committed.

## Brand Commitments

- Repo identity: `agentic-uxdesigner-harness`, MIT, described as the "Agent console
  for UX Designer workflows".
- Voice boundary (binding): caveman terse voice is the default conversational
  register; code, commits, reports, and wireframe files are ALWAYS normal English
  (or Spanish when the user asks).
- Upstream attributions must be preserved: `caveman` (© 2026 Julius Brussee,
  Apache-2.0, LICENSE + NOTICE in skill dir), `git-flow-master` (QA boilerplate copy).
- No product name, logo, or visual identity beyond the repo name was confirmed;
  no visual commitments exist to preserve.

## Evidence on Hand

- `reports/qa-park-comic-pages.md`, `reports/qa-factory-image-prompt.md` — example
  saved reports.
- `skills-lock.json` — vendored skill manifest; `.opencode/skills/` — seven
  vendored skills.
- `.env.example` — credential template (`TAVILY_API_KEY`).
- Absent, and future work must not fabricate: product website/landing copy,
  testimonials, customers, pricing, benchmarks, or press.

## Product Principles

1. Artifacts over edits — the harness produces reports and HTML files; it
   never modifies product code in other repos.
2. Reproducible workflows over one-offs — recipes, gotchas, and rubrics live
   in-repo so any session can repeat a result.
3. Loud failure over silent workarounds — missing credentials or auth problems
   stop the run and name the exact env var.
4. Narrow scope — audio, video and film generation are out of scope; work
   outside UX/UI is refused, not absorbed here.

## Accessibility & Inclusion

Every UX review is scored against a WCAG baseline alongside the Nielsen heuristics
(`ux-design-review` skill); accessibility findings are part of the standard ranked
output, not an optional extra.
