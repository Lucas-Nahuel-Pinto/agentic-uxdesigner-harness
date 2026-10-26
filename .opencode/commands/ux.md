---
description: "Run the UX design workflow: brief → discovery → IA and flows → wireframes → UI direction → usability test → audit → handoff, one user gate per stage."
agent: build
subtask: true
---
Call skill({ name: "ux-design-workflow" }) and follow it for $ARGUMENTS.

Start at stage 0 unless the user names a stage. Present each stage artifact at
its gate and stop for approval — do not run the whole pipeline silently.
