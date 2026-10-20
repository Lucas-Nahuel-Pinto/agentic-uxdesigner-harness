# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The agent operator running an OpenCode session on this console. The operator invokes
skills by name and consumes the artifacts the agent produces (UX review reports,
standalone HTML wireframes, generated audio). Downstream human designers or clients
may read the outputs, but the operator is the primary user.

## Product Purpose

A console that equips one agent with a repeatable UX-designer workflow: heuristic
design reviews, fast wireframes/mockups, and original music from the local ACE-Step
install. Success means each of those artifacts can be requested on demand and
delivered without ever touching product code.

## Positioning

A curated, opinionated console — not a generic coding agent with design plugins.
Its differentiator is the packaged workflow itself: a Nielsen + WCAG review rubric,
wireframe recipes, and local music generation with proven recipes/gotchas captured
in-repo, so results are reproducible and nothing computationally heavy leaves the
machine (external calls limited to the engram memory and tavily search MCPs).

## Operating Context

- OpenCode agent console; skills invoked by name (`/ux-design-review`,
  `/ux-wireframe`, `/acestep-music`, plus vendored caveman, git-flow-master,
  img2threejs, impeccable).
- ACE-Step 1.5 model install (multi-GB checkpoints + venv) lives OUTSIDE the repo at
  `ACESTEP_HOME`; the repo holds only the portable CLI (`acestep/generate.py`) and
  recipe knowledge (`acestep/README.md`). One take ≈ 5–8 min on an 8 GB RTX-class
  GPU; long runs are backgrounded.
- MCPs: `engram` (persistent memory, env read at session start; `engram` must be on
  PATH) and `tavily` (web search).
- Saved design reviews go in `reports/` only when requested; wireframes are
  standalone HTML files in this repo.

## Capabilities and Constraints

- Skills: heuristic UX audit (Nielsen + WCAG baseline, ranked findings, read-only),
  standalone HTML wireframes/clickable mockups, ACE-Step music (plain, cover mode,
  any vocal language), plus git operator and terse-voice vendored skills.
- Operating rules that future work must preserve:
  - Credentials ALWAYS from `.env` (template `.env.example`); never hardcoded.
  - MCP or auth failure = STOP, name the missing env var, no workarounds
    (`opencode.jsonc` substitutes `{env:VAR}` silently — a 401/403 is the signal).
  - Design reviews and wireframes NEVER modify product code.
  - Music: `acestep/generate.py` is the only entry point; artist-imitation /
    high-similarity cover legal risk stated BEFORE generating (personal/local use
    OK; publishing is the user's risk).
  - Git/PR work follows git-flow-master: semantic commit prefixes, no AI
    attribution, confirm before push, never rewrite pushed history; generated audio
    and model files (`outputs/`, `*.wav`, `*.mp3`) are never committed.
  - One take ≈ 5–8 min: always background music runs, never block the session.

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

- `acestep/README.md` — proven generation recipes and gotchas (caption control,
  language forcing, cover strengths).
- `reports/qa-park-comic-pages.md`, `reports/qa-factory-image-prompt.md` — example
  saved reports.
- `skills-lock.json` — vendored skill manifest; `.opencode/skills/` — seven
  vendored skills.
- `.env.example` — credential template (`TAVILY_API_KEY`, `ACESTEP_HOME`).
- Absent, and future work must not fabricate: product website/landing copy,
  testimonials, customers, pricing, benchmarks, or press.

## Product Principles

1. Local-first — heavy compute (music, model work) runs on the user's machine;
   only search/memory MCP calls leave it.
2. Artifacts over edits — the harness produces reports, HTML files, and audio; it
   never modifies product code in other repos.
3. Reproducible workflows over one-offs — recipes, gotchas, and rubrics live
   in-repo so any session can repeat a result.
4. Loud failure over silent workarounds — missing credentials or auth problems
   stop the run and name the exact env var.
5. Legal caution before generation — state imitation/cover risk before producing
   derivative-sounding audio.

## Accessibility & Inclusion

Every UX review is scored against a WCAG baseline alongside the Nielsen heuristics
(`ux-design-review` skill); accessibility findings are part of the standard ranked
output, not an optional extra.
