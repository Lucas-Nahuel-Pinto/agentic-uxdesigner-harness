# AGENTS.md — agentic-uxdesigner-harness

UX Designer console: heuristic design reviews, wireframes/mockups, and music
generation with the local ACE-Step 1.5 install.

## Critical rules

1. **CREDENTIALS**: ALWAYS read from `.env` (see `.env.example`). NEVER hardcode or guess secrets.
2. **MCP / AUTH FAILURE = STOP IMMEDIATELY**: if an MCP fails auth or an env var is missing (`.mcp.json` uses `${VAR}` for Claude Code; `opencode.jsonc` uses `{env:VAR}` for OpenCode — OpenCode substitutes empty silently, so a 401/403 is the signal), do NOT work around it. STOP, name the exact env variable, point at `.env` / `.env.example`, and ask the user to fix `.env` + restart the agent session (env is cached at MCP spawn time).
3. **NO PRODUCT-CODE EDITS**: design reviews are critique-only and wireframes are artifacts of THIS repo. Changing product code belongs to the product repo, never here.
4. **MUSIC = LOCAL, GENEROUSLY CAVEATED**: `acestep/generate.py` is the only music entry point. Read `acestep/README.md` before any run. Artist voice imitation or high-similarity covers: state the legal risk BEFORE generating (personal/local use OK; publishing is the user's risk).
5. **GIT / PR WORK**: follow `.claude/skills/git-flow-master/` — semantic commit prefixes, no AI attribution in commits, confirm before push, never rewrite pushed history. Never commit generated audio or model files (`outputs/`, `*.wav`, `*.mp3` are gitignored).
6. **DEFAULT VOICE**: caveman mode is the default conversational register (`.claude/skills/caveman/`). Code, commits, reports, and wireframe files are ALWAYS written in normal English (or Spanish when the user asks) — that boundary is built into the skill.

## Skills

| Skill | Purpose |
|---|---|
| `.claude/skills/ux-design-review/` | Heuristic UX audit: ranked findings + fixes (read-only) |
| `.claude/skills/ux-wireframe/` | Standalone HTML wireframes and clickable mockups |
| `.claude/skills/acestep-music/` | Song/jingle generation via `acestep/generate.py` |
| `.claude/skills/git-flow-master/` | End-to-end git operator (branch, commit, PR, conflicts) |
| `.claude/skills/caveman/` | Terse conversational voice (vendored, Apache-2.0) |

## MCPs

| MCP | Use |
|---|---|
| `engram` | Persistent memory across sessions |
| `tavily` | Web search (design patterns, accessibility rules, community fixes) |

## ACE-Step pointers

- CLI: `acestep/generate.py` — recipes + gotchas in `acestep/README.md`.
- Install location: `ACESTEP_HOME` env or the default local path (multi-GB
  local content, never committed). Run with the install's venv python.
- One take ≈ 5–8 min: always background the run, never block the session.
