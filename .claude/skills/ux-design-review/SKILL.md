---
name: ux-design-review
description: >
  Review UI designs, wireframes, mockups or live screens against UX
  heuristics: usability problems ranked by severity, accessibility gaps,
  and concrete fix suggestions. Use for "review this design", "revisa este
  diseño", "UX audit", "heuristic evaluation", "qué le falta a esta pantalla",
  "usability review", "revisa este mockup". Read-only critique — never edits
  the product code.
---

# ux-design-review

Heuristic UX evaluation of any interface artifact (HTML mockup, Figma export,
screenshot, live URL). Output: ranked findings with fixes, not a lecture.

## Inputs

| Input | Source |
| --- | --- |
| The design | Screenshot(s), HTML file, or live URL (use `/playwright-cli` to capture when live) |
| Context | Who uses it, for what task, on what device — ask ONLY if the review would materially differ without it |
| Standard | `references/heuristics.md` (Nielsen-derived 10 + accessibility baseline) |

## Steps

1. **Load the artifact.** For images, read them directly; for live pages,
   screenshot with `/playwright-cli` (load that skill first). Review what IS,
   not what the code intends.
2. **Walk the primary task.** Mentally execute the most likely user goal
   end-to-end. Every hesitation, dead-end, or missing affordance is a finding.
3. **Score against the heuristics.** `references/heuristics.md` — each finding
   cites the heuristic it violates.
4. **Rank by severity** (definitions in the reference): blocker → major →
   minor → polish. Accessibility failures (contrast, labels, focus) are never
   below minor.
5. **Deliver.** Findings table: severity · what · where · why it hurts the
   task · concrete fix (one line each). Then a 2-3 sentence overall verdict.
   Save to `reports/` only if asked; chat output is the default.

## Rules

- Critique the design, not the designer; every finding carries a fix.
- No finding without evidence ("the button reads OK on white" needs the
  contrast number or the visible pair).
- If the artifact is ambiguous (lo-fi wireframe), judge structure/flow only —
  do not invent visual-polish findings on a wireframe.
- Never edit product code from this skill; fixes are recommendations.
- User's language for the report; English for any artifact written to a file.
