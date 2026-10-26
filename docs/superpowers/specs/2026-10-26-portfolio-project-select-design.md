# Design: direct project selection (cinematic scene dropped)

- **Date**: 2026-10-26
- **Repo**: `C:\Agentic-Quality-Engineer\Projects\Lucas-Nahuel-Pinto.github.io`
- **Supersedes (in part)**: `2026-10-22-portfolio-walkthrough-design.md` — Fase 3 (Blender
  cinematic + first-person scene) and the animatic that validated it are dropped.
- **Status**: approved by the user (2026-10-26)

---

## 1. Decision

The animated intro is gone. After **COMENZAR** the visitor lands directly on the three
projects, selectable. There is no cutscene, no first-person scene, no Blender render and
no intro voice track.

New flow:

```
MENU ──[COMENZAR]──▶ GRID (3 projects) ──[card click]──▶ DETAIL ──[Abrir caso completo]──▶ /{lang}/proyectos/{slug}
  ▲                        │                                  │
  └──── ◀ Volver al menú ──┘                                  └── ◀ Volver a proyectos
```

`Escape` moves one level up (detail → grid → menu). The traditional HTML page underneath
stays as the fallback / SEO layer, reachable through "Ver proyectos sin 3D" (classic mode).

## 2. Why

- The cinematic was the expensive part of the plan (Blender set, four rigged characters,
  audio-synced lights, seven shots, match-cut, video encoding) and it delayed the thing
  that actually sells the portfolio: the projects.
- A visitor who clicks COMENZAR wants the work, not a 40 s intro. Project selection is the
  shortest path from curiosity to evidence.
- The approved menu already carries the visual identity (light glass, steel-blue tower,
  Mirror's Edge red). The grid reuses it, so no new aesthetic has to be invented or
  validated.
- Removing the voice track removes the audio-buffering gate: COMENZAR can no longer be
  blocked or slow.

## 3. Approaches considered

| Approach | Description | Verdict |
|---|---|---|
| **A — Glass HUD grid** | Reuse the menu's glass stage, tilt and spotlight; COMENZAR swaps to a "mission select" screen with the three projects | **Chosen** — coherent with the approved identity, zero new visual language |
| B — Dark AR HUD | Dark translucent overlay, scanlines, AR brackets, monospace | Rejected: breaks the light glass the user already approved |
| C — Grid on the page | COMENZAR closes the overlay and scrolls to the existing projects section | Rejected: loses the app feel and the detail screen |

## 4. Architecture

### 4.1 States

`src/walkthrough/state.ts`:

```ts
STATES = ['menu', 'panel', 'case', 'classic']
```

| From | Allowed |
|---|---|
| `menu` | `panel`, `classic` |
| `panel` | `case`, `menu`, `classic` |
| `case` | `panel`, `menu`, `classic` |
| `classic` | `menu` |

`cutscene` and `fp` are removed. `StateMachine` keeps its API (`state`, `on`, `set`) and
its guard against invalid transitions.

### 4.2 Screens (`src/components/Walkthrough.astro`)

Both new screens live inside the same `#wt` overlay, share the glass stage, and follow the
existing screen contract (`[data-screen]`, `hidden`, `inert`, `display:flex` only when
visible).

**GRID (`data-screen="panel"`)**

- Header: eyebrow `PROYECTOS` / `PROJECTS`, counter `03`, one-line intro.
- Three cards in a row (`grid-template-columns: repeat(3, 1fr)`), one column below 900 px.
- Card content, per project: index (`01`), title, pitch clamped to two lines, big metric
  value + label, up to three tag chips, arrow affordance.
- Card is a `<button>`; hover/focus-visible: lift, red border, spotlight tracking the
  pointer (`--mx/--my`, same technique as the menu), arrow slides right.
- Keyboard: `Tab` across cards, `Enter`/`Space` opens; `Escape` returns to the menu.
- Footer row: `◀ Volver al menú` and the classic exit link.

**DETAIL (`data-screen="case"`)**

- Two columns (single column below 900 px): left = eyebrow with project index, title,
  pitch, tag chips, primary CTA `Abrir caso completo`, secondary links `Ver demo` (only
  when the project has `live`) and `Ver código` (only when it has `repo`); right = the big
  metric and the three "what it demonstrates" cards (`caseStudy.skills.cards`).
- `◀ Volver a proyectos` and `◀ Menú`.
- On open, focus moves to the detail `<h2>` (`tabindex="-1"`); the grid button that opened
  it is restored on return.
- The primary CTA is a real `<a href>` to `pathFor(lang, 'proyectos/<slug>')`, so it works
  without JS once rendered and is crawlable.

### 4.3 Data flow (single source of truth)

`src/lib/projects.ts` stays the only source. A new module
`src/walkthrough/panel.ts` exports:

```ts
export interface ProjectCard {
  slug: string;
  live?: { href: string; label: string };
  repo?: { url: string; label: string };
  copy: Record<Lang, {
    title: string;
    pitch: string;
    tags: string[];
    metric: Metric;
    skills: { name: string; desc: string }[];
  }>;
}
export function buildCards(projects: Project[]): ProjectCard[];
```

`Walkthrough.astro` builds the payload in the frontmatter and injects it once:

```astro
<script type="application/json" id="wt-projects" set:html={payload} />
```

`payload` is `JSON.stringify(buildCards(PROJECTS)).replace(/</g, '\\u003c')` so no project
text can close the script tag. The client parses it, renders the grid and rebuilds the
detail on demand, and re-renders both on a hot language switch — no reload, no duplicated
copy in `strings.ts`.

If the payload is missing or unparsable, the component falls back to classic mode instead
of showing an empty grid (no dead screens).

### 4.4 Audio

`src/walkthrough/audio.ts` keeps only the synthesized SFX (`blip`, selection tick, panel
sound, mute state). Removed: voice source, `preload`, `play`, `pause/resume/seek`,
`onEnded`, subtitle timings. `AudioManager` no longer needs a `lang` argument for any
asset, but keeps `setMuted`. The menu's sound toggle still persists in `localStorage`.

COMENZAR is loud-free of network work: it transitions immediately.

### 4.5 Deletions

- `src/pages/animatic.astro`
- `src/walkthrough/animatic.ts`
- `public/audio/intro-speech-es.mp3`, `public/audio/intro-speech-en.mp3`
- `astro.config.mjs`: the `/animatic` sitemap exclusion (nothing left to exclude)
- `strings.ts`: `loading`, `skip`, `cutsceneSoon`, `fpSoon`, `panelSoon`; new keys for the
  grid/detail screens
- `Walkthrough.astro`: cutscene/fp markup and styles, the voice preload gate, `.subs`,
  `.skip`, the `loadingEl` status line, `wakeGlass` is kept (still needed after the
  menu ⇄ grid round-trip)

### 4.6 What stays

- Menu: ES/EN hot switch, persisted language and sound, COMENZAR, classic exit link.
- Tilt + cursor spotlight on the menu stage.
- `classic` mode with the traditional page (`hero` + `Stripe` sections) that Astro renders
  under the overlay — SEO, no-JS and degraded-GPU story unchanged.
- `<noscript>` hides the overlay.
- Case-study routes `/{lang}/proyectos/{slug}` and their content.

## 5. Accessibility

- Cards and back buttons are native `<button>`s; focus ring uses the existing
  `:focus-visible` rule (red on glass, ≥ 3:1 against the pane).
- Each card's accessible name is the project title; the pitch and metric follow in the
  DOM so screen readers hear them inside the button.
- `inert` + `hidden` on inactive screens (already the pattern) keeps the tab order clean.
- `Escape` never traps: detail → grid → menu.
- Reduced motion: the tilt, lift and arrow transitions are disabled by the existing
  `prefers-reduced-motion` block, extended to the new elements.

## 6. Verification

1. `bun run check` → 0 errors.
2. `bun run build` → succeeds; `dist/` contains no `animatic`, no `audio/intro-speech-*`.
3. Playwright, both languages: menu → COMENZAR → grid shows three cards → open each one →
   detail renders the right copy → `Abrir caso completo` navigates to the case study →
   browser back returns to the grid → `◀ Volver al menú` restores the menu.
4. Hot language switch on grid and detail updates every string without a reload.
5. `Escape` from detail returns to the grid; from the grid returns to the menu.
6. No console errors; no layout scrollbar at 588×478 nor at 375×667.
7. Classic mode still scrolls to `#work` and the restore button returns to the menu.

## 7. Out of scope

- AR magazine / comic viewer (old Fase 5) — future work.
- Case-study gallery assets: `projects.ts` references `/images/jira-traceability/*.png`
  and that folder does not exist in the repo; the case-study gallery is broken today.
  Tracked separately, not fixed here.
- Pushing the 38 pending local commits (needs explicit user confirmation).
