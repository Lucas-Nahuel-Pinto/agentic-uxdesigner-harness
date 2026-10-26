# Stages in detail

One section per stage. Each has: purpose, inputs, steps, what the artifact must
contain, the gate checklist, and the failure mode that costs the most.

---

## 0 · Brief

**Purpose:** turn a vague request into a testable problem. This is the only
stage where the user is the main source.

**Inputs:** the request, any existing product links or screenshots, business
constraint (if the user has one), deadline.

**Steps**

1. Restate the problem in one sentence: *who* is stuck, *doing what*, *why now*.
2. Name the primary task of the product (the one action that must work).
3. Capture constraints: platform, tech stack, existing brand, languages,
   regulatory or accessibility obligations, timeline.
4. Define the success signal: what observable change means this worked
   (task completion, time on task, drop-off, support tickets). No vanity metric.
5. List every unknown as an open question with an owner (user or agent).

**Artifact `00-brief.md`:** one page — problem, primary task, users (raw),
constraints, success signal, open questions, `Gate:` line.

**Gate**

- [ ] Problem sentence names a user and a task, not a feature.
- [ ] Success signal is observable, not a feeling.
- [ ] Open questions are listed; none of them silently assumed.
- [ ] Scope is bounded: what is explicitly out.

**Costliest failure:** designing a screen before the primary task is agreed.

---

## 1 · Discovery

**Purpose:** understand the people and the friction well enough that later
decisions can cite something.

**Owner:** `ux-research` subagent (judgment + synthesis). The main agent may
answer from provided material instead of running research.

**Inputs:** `00-brief.md`, any transcripts, analytics, support logs, competitor
or market material. If none exist, the artifact is built on assumptions and
must say so loudly.

**Steps**

1. **Jobs to be done** — 3–6 jobs phrased *when [situation], I want to
   [motivation], so I can [outcome]*.
2. **Segments / personas** — only as many as change a design decision (2–3
   normally). Each: context, goal, current workaround, one blocking friction.
3. **Journey** — stages of the current experience, what the user does, thinks,
   feels, and where it breaks. Mark the two or three moments that matter.
4. **Assumptions table** — assumption · impact if wrong · how to test · risk
   (high/med/low). Ranked. High-risk assumptions drive stage 5 tasks.
5. **Evidence labels** — every claim tagged `evidence` (source), `assumption`
   (reasoning) or `unknown`. No unlabelled claims.

**Artifact `01-discovery.md`:** the four blocks above + evidence section.

**Gate**

- [ ] Jobs are situational, not feature names.
- [ ] Every persona maps to a decision it changes.
- [ ] Journey shows at least one concrete break, with the moment named.
- [ ] The riskiest assumptions are testable in stage 5 (not "users like it").

**Costliest failure:** personas invented as decoration; if no research exists,
say "assumption" and keep the list short.

---

## 2 · IA & flows

**Purpose:** decide what screens exist and how the user moves between them,
before any pixels.

**Owner:** `ux-architect` subagent.

**Inputs:** `00-brief.md`, `01-discovery.md`.

**Steps**

1. **Sitemap** — every screen/page, one line of purpose each, grouped by
   navigation level. No orphan screens.
2. **Primary flow** — the happy path from entry to the primary task, as a
   diagram (Mermaid `flowchart` inline, or `/archify` for a richer one). One
   diagram per primary task; not one giant diagram.
3. **Secondary flows** — recovery, error, auth, empty state. Name the decision
   points where the user can leave.
4. **Screen inventory** — table: screen · primary task · entry points · exit
   points · required states (default, empty, loading, error, success, mobile,
   RTL/long copy if relevant).
5. **Content model** — what the screen must say (labels, hierarchy), not final
   copy. Flag the strings that carry the most risk.

**Artifact `02-ia-flows.md`:** sitemap, diagrams, inventory, content model,
decisions log (what was rejected and why).

**Gate**

- [ ] Every screen traces to a job from stage 1.
- [ ] Each screen has exactly one primary task.
- [ ] Every flow has an exit (back, cancel, escape) — no dead end.
- [ ] States are named per screen, not "TBD".
- [ ] Diagram is readable at a glance (≤ 12 nodes per flow).

**Costliest failure:** ten screens and no stated path; the wireframe stage then
invents navigation.

---

## 3 · Wireframes

**Purpose:** prove the flow with cheap, clickable screens.

**Owner:** `ux-wireframe` subagent (one artifact per flow).

**Inputs:** `02-ia-flows.md`. A minimal brief if the ask is a single screen.

**Steps**

1. Build one standalone HTML file per flow, low fidelity by default.
2. Cover every state named in the inventory; mark each state on screen.
3. Wire the flow with links or tiny JS; every screen reachable and escapable.
4. Check semantics even at low fidelity: headings, labels, focus order, target
   sizes ≥ 44 px.

**Artifact `03-wireframes/`:** the HTML file(s) + `manifest.md` (screen → state
→ file anchor).

**Gate**

- [ ] Every inventory screen exists and is reachable.
- [ ] Empty / loading / error states are visible, not implied.
- [ ] The primary task can be completed end to end by clicking.
- [ ] No brand styling that invites visual debate (`04` is for that).
- [ ] Opens from `file://` with no build step and no network.

**Costliest failure:** polishing a wireframe; it converts structural feedback
into colour feedback.

---

## 4 · UI direction

**Purpose:** choose a visual language that serves the brief, then express it as
tokens — not as a pile of screens.

**Owner:** main agent, loading `impeccable` (execution/quality) and
`ui-ux-pro-max` (style, palette, type pairing references).

**Inputs:** `00-brief.md`, `03-wireframes/`.

**Steps**

1. Pick 2 candidate directions, each justified against the brief's tone,
   audience and density needs. Show the trade-off, not a mood board.
2. Define the system: colour roles (surface, text, muted, accent, semantic),
   type scale, spacing scale, radius, elevation, motion durations/easing.
3. Verify contrast pairs (text ≥ 4.5:1, large text ≥ 3:1, UI borders ≥ 3:1)
   and list the numbers.
4. Apply the direction to **one** representative screen to prove it, not all.

**Artifact `04-ui-direction.md`:** chosen direction + rejected one with reason,
token table, contrast table, one proof screen reference.

**Gate**

- [ ] Every token has a role, not just a value.
- [ ] Contrast numbers are stated, not asserted.
- [ ] Type scale works at 320 px and at 1440 px.
- [ ] Reduced-motion and dark/light (if in scope) defined.

**Costliest failure:** building a system nobody validated against the brief's
density; enterprise screens with marketing spacing is the classic version.

---

## 5 · Usability test

**Purpose:** find where the design fails *before* engineering pays for it.

**Owner:** main agent. `ux-review` scores findings; `ux-vision` reads captured
screenshots. Real participants are the user's call — the artifact must work
with 0 participants (expert walkthrough) and scale to 5.

**Inputs:** `03-wireframes/` (or stage 4 proof), riskiest assumptions from
stage 1.

**Steps**

1. Turn the two or three riskiest assumptions into tasks: *"You want to
   [goal]. Show me how you'd do it."* No leading wording.
2. Script per task: setup, prompt, success criteria, failure signals, time
   budget, follow-up questions. Neutral moderation notes (don't rescue early).
3. Run an expert walkthrough now: execute each task yourself with the
   heuristics open, record every hesitation with a timestamp.
4. Synthesize: observation → interpretation → severity → fix. Group repeated
   observations into one finding with a count.
5. State the confidence level: expert walkthrough vs N participants.

**Artifact `05-usability-test.md`:** tasks, script, environment matrix,
observations log, findings, confidence, what to re-test.

**Gate**

- [ ] Every task maps to an assumption from stage 1.
- [ ] Prompts are goal-worded, not UI-worded ("open settings" is a hint).
- [ ] Findings have severity and a fix; observations stay separate from opinion.
- [ ] Confidence is stated honestly.

**Costliest failure:** asking opinions ("do you like it?") instead of watching
tasks fail.

---

## 6 · Audit

**Purpose:** catch what the tasks missed — consistency, states, accessibility,
edge cases — with a ranked, cited list.

**Owner:** `ux-review` subagent following `ux-design-review`; optionally the
competitor/pattern sweep with `tavily`.

**Inputs:** the artifact under audit (HTML, screenshots, live URL), the brief.

**Steps**

1. Capture the current state: `/playwright-cli` for live pages, all breakpoints
   and key states.
2. Walk the primary task end to end, then the recovery paths.
3. Score against the heuristics + WCAG baseline in
   `ux-design-review/references/heuristics.md`.
4. Rank blocker → major → minor → polish. Accessibility is never below minor.
5. Separate "breaks the task" from "degrades the experience".

**Artifact `06-audit.md`:** ranked findings table (severity · what · where ·
impact · fix · rule cited), blocking list, verdict paragraph.

**Gate**

- [ ] No finding without evidence (number, screenshot region, DOM attribute).
- [ ] Every finding cites a heuristic or WCAG criterion.
- [ ] Blocking issues are short, explicit and reproducible.
- [ ] The list is actionable in one sprint.

---

## 7 · Handoff

**Purpose:** make the design buildable without a meeting.

**Owner:** `ux-handoff` subagent.

**Inputs:** stages 2–6.

**Steps**

1. Component inventory: name, purpose, anatomy, variants, states (default,
   hover, focus-visible, active, disabled, loading, error, empty).
2. Tokens as a table (or JSON) with the exact values used in stage 4.
3. Content and i18n notes: string keys, pluralization, character budgets, RTL
   or long-text behaviour.
4. Accessibility requirements per component: role, name, keyboard interaction,
   focus management, announcements, contrast minimums.
5. Acceptance criteria per screen, written testably (Given/When/Then).
6. Open decisions with owner and deadline — never silently resolved.

**Artifact `07-handoff.md`:** the six blocks above. This is the one artifact
worth copying to `reports/` when the user asks to keep it.

**Gate**

- [ ] A developer can build every screen without asking a design question.
- [ ] Every state has a defined visual.
- [ ] Every interactive element has keyboard and screen-reader behaviour.
- [ ] Acceptance criteria are testable, not aspirational.
- [ ] Open decisions are visible, not hidden in prose.
