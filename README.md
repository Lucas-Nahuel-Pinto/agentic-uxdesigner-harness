# agentic-uxdesigner-harness

Agent console for **UX Designer workflows**: heuristic design reviews,
fast wireframes/mockups, and original music generation with the local
ACE-Step 1.5 install.

## What's inside

```
.opencode/skills/
  ux-design-review/         Heuristic UX audit (Nielsen + WCAG baseline), ranked findings
  ux-wireframe/             Standalone HTML wireframes and clickable mockups
  acestep-music/            Song/jingle generation via the local ACE-Step install
  caveman/                  Terse voice skill (vendored from github.com/JuliusBrussee/caveman, Apache-2.0)
  git-flow-master/          Git operator skill
acestep/
  generate.py               ACE-Step 1.5 generation CLI (plain, cover mode, any vocal language)
  README.md                 Proven recipes + gotchas (caption control, language forcing, cover strengths)
opencode.jsonc              OpenCode MCP config (engram + tavily)
.env.example                Credential template
AGENTS.md                   Agent operating rules
reports/                    Saved design reviews (only when requested)
```

## Setup

1. `cp .env.example .env` and fill in (`TAVILY_API_KEY`; `ACESTEP_HOME` if
   your ACE-Step install is not at the default local path).
2. `engram` must be on your PATH; MCP env vars are read at session start.
3. Open the repo in your agent and invoke skills by name
   (`/ux-design-review`, `/ux-wireframe`, `/acestep-music`).

## Quick start

```bash
# UX review of a live screen
# (tell the agent: "review https://example.com checkout UX")

# Wireframe
# (tell the agent: "wireframe a settings screen with profile, notifications, billing")

# Song generation (needs the local ACE-Step install)
"$ACESTEP_HOME/.venv/Scripts/python.exe" acestep/generate.py \
  --caption "punk rock, energetic, 178 bpm" --lyrics-file song.txt --bpm 178
```

## ACE-Step: what lives where

Only the **portable capability** lives here: the CLI + the recipe knowledge in
`acestep/README.md`. The model install (checkpoints, venv, several GB) is
local content kept OUTSIDE this repo — set `ACESTEP_HOME` to it. Songs are
generated in ~5–8 min per take on an 8 GB RTX-class GPU.

## Rules of the road

- Credentials always from `.env`; never hardcoded.
- MCP or auth failure = STOP and name the missing env var; no workarounds.
- Design reviews and wireframes never modify product code — artifacts live in
  this repo (`reports/`, wireframe HTML files).
- Music: respect artist-imitation and cover-strength legal caveats
  (personal/local use OK; publishing risks takedowns + publicity claims).
- No AI attribution in commits; confirm before push.
- Caveman voice is the default for conversation; code/commits/artifacts stay
  normal English or Spanish — that boundary is built into the skill.

## Upstream attribution

- `caveman` skill — © 2026 Julius Brussee, Apache-2.0. See
  `.opencode/skills/caveman/LICENSE-APACHE-2.0` and `NOTICE` in this directory.
- `git-flow-master` — copied from the project QA boilerplate.
