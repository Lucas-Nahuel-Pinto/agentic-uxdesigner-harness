# UX heuristics (Nielsen-derived) + accessibility baseline

## The 10 heuristics

| # | Heuristic | Ask |
| --- | --- | --- |
| 1 | **Visibility of system status** | Does the user know what's happening within 100ms of every action? (spinners, progress, selected state) |
| 2 | **Match between system and real world** | Language the user knows, not the system's jargon? Logical information order? |
| 3 | **User control and freedom** | Undo, cancel, back — can the user leave an unwanted state without a cascade of clicks? |
| 4 | **Consistency and standards** | Same thing, same look, same words, everywhere? Platform conventions respected? |
| 5 | **Error prevention** | Are dangerous/destructive actions constrained or confirmed before they can go wrong? |
| 6 | **Recognition over recall** | Options visible? Context carried between screens? No memorizing IDs/codes across steps. |
| 7 | **Flexibility and efficiency of use** | Shortcuts for experts, defaults for novices? |
| 8 | **Aesthetic and minimalist design** | Every pixel earning its place? No info competing with the primary task? |
| 9 | **Help users recognize, diagnose, recover from errors** | Error messages say what happened + what to do, in plain language, near the error? |
| 10 | **Help and documentation** | Is help findable at the moment of need (not a manual dump)? |

## Accessibility baseline (WCAG 2.2 AA — the non-negotiables)

| Check | Threshold |
| --- | --- |
| Text contrast | 4.5:1 normal text, 3:1 large text (18.66px bold / 24px) |
| UI component contrast | 3:1 against adjacent colors (borders, icons, focus rings) |
| Keyboard | Everything reachable and operable by keyboard; visible focus ring on every interactive element |
| Focus order | Follows visual/logical order; focus not trapped |
| Labels | Every input has an associated label; icon-only buttons have accessible names |
| Targets | Clickable area ≥ 24×24 px (WCAG 2.2); ≥ 44×44 recommended on touch |
| Motion | Respects `prefers-reduced-motion` for non-essential animation |
| Language | Page declares its language (`lang` attr) — affects screen-reader pronunciation |

## Severity scale

| Severity | Definition |
| --- | --- |
| **Blocker** | Prevents completing the primary task; no workaround |
| **Major** | Slows or heavily confuses the task; workaround exists but users will fail or bail |
| **Minor** | Real friction or accessibility gap, but the task completes |
| **Polish** | Consistency/nicety; fix when touching that area anyway |

Accessibility failures default to at least **minor**; keyboard traps and
missing labels on essential flows are **major** or **blocker**.
