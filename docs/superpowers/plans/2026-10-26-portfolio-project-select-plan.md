# Implementation plan: direct project selection

- **Date**: 2026-10-26
- **Spec**: `2026-10-26-portfolio-project-select-design.md` (approved)
- **Repo**: `C:\Agentic-Quality-Engineer\Projects\Lucas-Nahuel-Pinto.github.io`
- **Rule**: every step ends runnable and verifiable; no step leaves the overlay in a dead state.

---

## Step 1 — Data module `src/walkthrough/panel.ts`

| # | Task |
|---|---|
| 1.1 | `ProjectCard` interface: `slug`, optional `live`/`repo`, `copy: Record<Lang, {title, pitch, tags, metric, skills}>` |
| 1.2 | `buildCards(PROJECTS)` maps `stripe.metric`, `caseStudy.title/pitch/tags`, `caseStudy.skills.cards` |
| 1.3 | `parseCards(raw: string): ProjectCard[] \| null` — safe `JSON.parse`, returns `null` on failure |

**Acceptance**: `bun run check` clean.

## Step 2 — `state.ts`

| # | Task |
|---|---|
| 2.1 | `STATES = ['menu','panel','case','classic']` |
| 2.2 | Transitions: menu→panel/classic, panel→case/menu/classic, case→panel/menu/classic, classic→menu |
| 2.3 | Update the header comment (flow diagram) |

**Acceptance**: no reference to `cutscene`/`fp` in `src/`.

## Step 3 — `audio.ts` slims down to SFX

| # | Task |
|---|---|
| 3.1 | Remove voice source, `preload`, `play`, `pause/resume/seek`, fade logic, `onEnded`, subtitle timings |
| 3.2 | Keep `blip`, selection tick, panel sound, `setMuted`, internal mute state |
| 3.3 | Constructor no longer takes `lang`; `setLang` removed |

**Acceptance**: no `intro-speech` string in `src/`; sounds still play on menu interactions.

## Step 4 — `strings.ts`

| # | Task |
|---|---|
| 4.1 | Remove `loading`, `skip`, `cutsceneSoon`, `fpSoon`, `panelSoon` |
| 4.2 | Add `projects`, `projectsIntro`, `backToProjects`, `openCase`, `viewCode`, `liveDemo`, `project` (eyebrow) |

**Acceptance**: both languages present, `Record<Lang, WalkthroughStrings>` type-checks.

## Step 5 — `Walkthrough.astro`: grid + detail

| # | Task |
|---|---|
| 5.1 | Frontmatter: `buildCards(PROJECTS)` → JSON payload → `<script type="application/json" id="wt-projects">` with `<` escaped |
| 5.2 | Delete cutscene + fp sections and their styles (`.subs`, `.skip`, `.placeholder`) |
| 5.3 | Grid section `data-screen="panel"`: header + 3 card buttons (server-rendered placeholders replaced client-side) + footer actions |
| 5.4 | Detail section `data-screen="case"`: dynamic body rendered client-side, back buttons |
| 5.5 | Client: parse payload → render grid → open detail → `Abrir caso completo` href from `pathFor` |
| 5.6 | COMENZAR → `sm.set('panel')` immediately; drop the voice gate, `readyPromise`, `voiceReady`, `loadingEl` |
| 5.7 | Escape handling: case→panel, panel→menu |
| 5.8 | Language switch re-renders grid/detail copy + card hrefs |
| 5.9 | Payload missing/unparsable → `classic` fallback |
| 5.10 | Styles: glass grid (3 → 1 column at 900 px), lift + red border on hover/focus, spotlight, detail two-column, reduced-motion coverage |

**Acceptance**: menu → grid → detail → case study works in ES and EN with no reload; no scrollbars at 588×478 and 375×667.

## Step 6 — Delete the cinematic leftovers

| # | Task |
|---|---|
| 6.1 | Delete `src/pages/animatic.astro`, `src/walkthrough/animatic.ts` |
| 6.2 | Delete `public/audio/intro-speech-es.mp3`, `public/audio/intro-speech-en.mp3` |
| 6.3 | `astro.config.mjs`: drop the `/animatic` sitemap exclusion |
| 6.4 | Grep the repo for `animatic` / `intro-speech` / `cutscene` / `fpSoon` → zero matches in `src/` |

**Acceptance**: `dist/` has no animatic route and no intro audio.

## Step 7 — Verification

| # | Task |
|---|---|
| 7.1 | `bun run check` → 0 errors |
| 7.2 | `bun run build` → clean, `dist/` inspected |
| 7.3 | Playwright: full flow ES and EN, language hot-switch, Escape ladder, back navigation, classic mode, console clean |
| 7.4 | Screenshot of grid + detail for the user |

**Acceptance**: all of the above pass; the user reviews the screenshots.

## Step 8 — Commit

Semantic commits, no AI attribution; push only with explicit confirmation (38 commits are
already pending).
