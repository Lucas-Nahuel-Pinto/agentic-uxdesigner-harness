# agentic-uxdesigner-harness

Agent console for **UX Designer workflows**: a full design pipeline (brief →
discovery → IA/flows → wireframes → UI direction → usability test → audit →
handoff), heuristic design reviews and fast wireframes/mockups.

## The workflow

`/ux` runs `.opencode/skills/ux-design-workflow/`: seven stages, one artifact and
one user gate each. Artifacts land in `outputs/ux/<project>/` (gitignored);
deliverables the user keeps go to `reports/`. Stage routing:

| Stage | Agent |
|---|---|
| 0 Brief | main agent, with the user |
| 1 Discovery | `ux-research` |
| 2 IA & flows | `ux-architect` |
| 3 Wireframes | `ux-wireframe` |
| 4 UI direction | main agent (`impeccable`, `ui-ux-pro-max`) |
| 5 Usability test | main agent + `ux-review` |
| 6 Audit | `ux-review` (`ux-design-review` rubric) |
| 7 Handoff | `ux-handoff` |

## What's inside

```
.opencode/skills/
  ux-design-workflow/       End-to-end UX pipeline: brief → discovery → IA/flows →
                            wireframes → UI direction → usability test → audit → handoff
  ux-design-review/         Heuristic UX audit (Nielsen + WCAG baseline), ranked findings
  ux-wireframe/             Standalone HTML wireframes and clickable mockups
  caveman/                  Terse voice skill (vendored from github.com/JuliusBrussee/caveman, Apache-2.0)
  git-flow-master/          Git operator skill
.opencode/agents/
  ux-research.md            Discovery synthesis (stage 1)
  ux-architect.md           IA, flows, screen inventory (stage 2)
  ux-wireframe.md           Wireframe builder (stage 3)
  ux-review.md              Heuristic + WCAG findings (stages 5-6)
  ux-vision.md              Image/render inspection (verification)
  ux-handoff.md             Buildable spec (stage 7)
.opencode/commands/
  ux.md                     /ux — enter the workflow
opencode.jsonc              OpenCode MCP config (engram + tavily)
.env.example                Credential template
AGENTS.md                   Agent operating rules
reports/                    Saved design reviews (only when requested)
```

## Setup

1. `cp .env.example .env` and fill in (`TAVILY_API_KEY`).
2. `engram` must be on your PATH; MCP env vars are read at session start.
3. Open the repo in your agent and invoke skills by name
   (`/ux-design-workflow`, `/ux-design-review`, `/ux-wireframe`), or run the
   whole pipeline with `/ux`.

## Quick start

```bash
# Full UX workflow (stops at every gate)
/ux design the checkout flow for a B2B portal

# One stage
/ux run discovery for the onboarding redesign

# UX review of a live screen
# (tell the agent: "review https://example.com checkout UX")

# Wireframe
# (tell the agent: "wireframe a settings screen with profile, notifications, billing")
```

## Rules of the road

- Credentials always from `.env`; never hardcoded.
- MCP or auth failure = STOP and name the missing env var; no workarounds.
- Design reviews and wireframes never modify product code — artifacts live in
  this repo (`reports/`, wireframe HTML files).
- No AI attribution in commits; confirm before push.
- Caveman voice is the default for conversation; code/commits/artifacts stay
  normal English or Spanish — that boundary is built into the skill.

## Upstream attribution

- `caveman` skill — © 2026 Julius Brussee, Apache-2.0. See
  `.opencode/skills/caveman/LICENSE-APACHE-2.0` and `NOTICE` in this directory.
- `git-flow-master` — copied from the project QA boilerplate.
