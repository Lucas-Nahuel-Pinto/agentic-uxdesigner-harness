# AGENTS.md — agentic-uxdesigner-harness

UX Designer console: heuristic design reviews and wireframes/mockups.

Scope: **UX/UI design only.** No pixel, audio or video generation in this
console. Local image and video generation (ComfyUI + models, ~30 GB under
`C:/AI`) was uninstalled on 2026-10-25 — never propose reinstalling a local
generator.

## Critical rules

1. **CREDENTIALS**: ALWAYS read from `.env` (see `.env.example`). NEVER hardcode or guess secrets.
2. **MCP / AUTH FAILURE = STOP IMMEDIATELY**: if an MCP fails auth or an env var is missing (`opencode.jsonc` uses `{env:VAR}` — OpenCode substitutes empty silently, so a 401/403 is the signal), do NOT work around it. STOP, name the exact env variable, point at `.env` / `.env.example`, and ask the user to fix `.env` + restart the agent session (env is cached at MCP spawn time).
3. **NO PRODUCT-CODE EDITS**: design reviews are critique-only and wireframes are artifacts of THIS repo. Changing product code belongs to the product repo, never here.
4. **GIT / PR WORK**: follow `.opencode/skills/git-flow-master/` — semantic commit prefixes, no AI attribution in commits, confirm before push, never rewrite pushed history. Never commit generated media (`outputs/`, `*.wav`, `*.mp3`, `*.png` are gitignored).
5. **DEFAULT VOICE**: caveman mode is the default conversational register (`.opencode/skills/caveman/`). Code, commits, reports, and wireframe files are ALWAYS written in normal English (or Spanish when the user asks) — that boundary is built into the skill.

## Skills

| Skill | Purpose |
|---|---|
| `.opencode/skills/ux-design-review/` | Heuristic UX audit: ranked findings + fixes (read-only) |
| `.opencode/skills/ux-wireframe/` | Standalone HTML wireframes and clickable mockups |
| `.opencode/skills/git-flow-master/` | End-to-end git operator (branch, commit, PR, conflicts) |
| `.opencode/skills/caveman/` | Terse conversational voice (vendored, Apache-2.0) |
| `.agents/skills/threejs-*` (7) | Verified three.js r186 reference: fundamentals, interaction, animation, shaders, lighting, postprocessing, performance |
| `.agents/skills/playwright-cli/` | Browser automation: navigation, clicks, screenshots — verifies the rendered 3D scene |
| `.opencode/skills/impeccable/` | Frontend design operator: `/impeccable init\|critique\|audit\|polish\|animate\|...`. Telemetry off, no hooks (OpenCode has no hook surface) |
| `.opencode/skills/img2threejs/` | Reference photo → quality-gated procedural Three.js model. Manual vendor (no nested `.git`); forge scripts need Python 3.10+ |

Skills stack for 3D web work: `threejs-*` builds the scene, `img2threejs` fabricates
models from photos, `impeccable` polishes the surrounding UI.

## MCPs

| MCP | Use |
|---|---|
| `engram` | Persistent memory across sessions |
| `tavily` | Web search (design patterns, accessibility rules, community fixes) |
