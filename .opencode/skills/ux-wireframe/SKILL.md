---
name: ux-wireframe
description: >
  Build fast HTML/CSS wireframes and interactive mockups of UI screens from a
  written description or requirements: structure first, low-fidelity by
  default, clickable flows between screens. Use for "wireframe", "mockup",
  "hazme un mockup de", "pantalla de", "prototipo navegable", "layout para",
  "design this screen". Output is a standalone HTML file — never touches
  product code.
---

# ux-wireframe

Turn a screen description into a standalone HTML wireframe the user can open
and click. Structure and flow over pixels.

## Inputs

| Input | Source |
| --- | --- |
| What to design | User description: screen(s), primary task, audience |
| Fidelity | Default LOW (grays, boxes, real-ish copy); medium fidelity only on request (closer to brand) |
| Flow | Which screens connect and how (primary CTA of each screen) — ask only if >1 screen and the flow is ambiguous |

## Steps

1. **List the screens** and the primary task per screen. If the user described
   a flow, map screen → screen via the primary CTA before coding anything.
2. **Wireframe each screen.** Single HTML file per flow, sections in order:
   header → primary task content → supporting → footer. Real labels (never
   "Lorem ipsum" — plausible domain copy makes the layout judgeable).
3. **Wire the flow.** Anchor links or tiny JS between screens; back links
   everywhere. `file://` openable with zero build step, zero dependencies.
4. **Hand off.** Repo-relative file path + a one-line map of the flow. Offer
   a screenshot pass (`/playwright-cli`) if the user wants to see it rendered.

## Rules

- One file per flow unless the user asks otherwise; keep it under ~500 lines —
  wireframes that grow past that should become real code in the product repo.
- Low-fidelity by default: monochrome grays, no brand assets, no gradients —
  color invites premature visual debate before structure is right.
- Accessibility even in wireframes: label inputs, focus styles, semantic
  headings — a wireframe teaches the pattern the build will copy.
- Inline CSS, no frameworks, no CDN links (must work offline).
- File language: match the user's copy language; code/comments in English.
