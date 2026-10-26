# agentic-uxdesigner-harness

Agent console for **UX Designer workflows**: heuristic design reviews and
fast wireframes/mockups.

> Audio, video and film generation live in
> `../agentic-filmmaker-harness` (ACE-Step music, VoiceStudio, cloud video).

## What's inside

```
.opencode/skills/
  ux-design-review/         Heuristic UX audit (Nielsen + WCAG baseline), ranked findings
  ux-wireframe/             Standalone HTML wireframes and clickable mockups
  caveman/                  Terse voice skill (vendored from github.com/JuliusBrussee/caveman, Apache-2.0)
  git-flow-master/          Git operator skill
opencode.jsonc              OpenCode MCP config (engram + tavily)
.env.example                Credential template
AGENTS.md                   Agent operating rules
reports/                    Saved design reviews (only when requested)
```

## Setup

1. `cp .env.example .env` and fill in (`TAVILY_API_KEY`).
2. `engram` must be on your PATH; MCP env vars are read at session start.
3. Open the repo in your agent and invoke skills by name
   (`/ux-design-review`, `/ux-wireframe`).

## Quick start

```bash
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
