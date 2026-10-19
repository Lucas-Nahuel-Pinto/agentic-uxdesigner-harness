---
name: acestep-music
description: >
  Generate original music/audio locally with ACE-Step 1.5 (RTX-class GPU, no
  cloud). Use for "generate a song", "hazme una canción", "theme song",
  "jingle", "background music", "generar música", "cover de esta canción",
  "versión en español de la canción", audio beds for UX prototypes or
  presentations. Reads acestep/README.md for proven recipes before running.
---

# acestep-music

Compose songs/jingles with the local ACE-Step install. This skill owns the
recipe knowledge; `acestep/generate.py` is the only entry point (never
hand-write a per-song generation script — parameterize instead).

## Inputs

| Input | Source |
| --- | --- |
| Style caption | User request → English genre description <512 chars (caption quality drives the result more than any other knob) |
| Lyrics | User-provided or written by the agent in the target singer's phrasing style |
| Model install | `ACESTEP_HOME` env or the default path in `acestep/README.md` — local content, never committed |
| Optional reference | Existing track for cover mode (`--cover`) |

## Steps

1. **Read `acestep/README.md`** — recipes and gotchas (caption control,
   language forcing, cover strengths, WAV-only output).
2. **Write/validate the lyric.** Match phrasing to the intended style (rap
   cadence for hip-hop, chant chorus for novelty songs, etc.), not to a
   template. Language: English sings best; Spanish works via `--lang es`.
3. **Choose the recipe** (plain / cover / non-English) and build the command.
4. **Run in background** (~5–8 min per song) and continue other work; report
   the WAV path when notified. One take per run — iterate by changing caption
   adjectives or seed, not by stacking params.
5. **Deliver + caveat.** Give the file path and, if the result imitates a
   living artist or a copyrighted recording, the one-line legal caveat
   (publishing risk; personal/local listening is fine).

## Rules

- One generation = one song = one background run; never block the session on
  a foreground run.
- Respect the hard gotchas: `use_cot_caption=False`, `use_cot_language=False`
  (both already forced in the CLI), WAV output only.
- For voice impersonation of real artists or high-similarity covers, state the
  risk BEFORE generating; proceed only for personal/local use.
- Never commit generated audio or the model install to this repo.
