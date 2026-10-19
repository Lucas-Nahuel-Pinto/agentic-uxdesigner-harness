# ACE-Step — local music generation (portable part)

This repo carries only the **portable capability**: the CLI (`generate.py`) and
the recipe knowledge. The model install (checkpoints, venv, several GB) is
**local content that lives outside this repo**:

```
<ACESTEP_HOME>/            default: C:\Agentic-Quality-Engineer\Projects\bunkai\acestep-local\ACE-Step-1.5
  checkpoints/             acestep-v15-turbo + acestep-5Hz-lm-0.6B + vae + Qwen3 embedding
  .venv/Scripts/python.exe the python that runs generate.py
  docs/en/Tutorial.md      upstream docs (cover mode recipe ~lines 740-775)
```

Hardware assumption: NVIDIA GPU ~8 GB VRAM (RTX 3070 class). The CLI enables
int8 quantization + CPU offload automatically for that tier.

## Run

```bash
export ACESTEP_HOME=/path/to/ACE-Step-1.5   # only if not at the default path
"$ACESTEP_HOME/.venv/Scripts/python.exe" acestep/generate.py \
  --caption "punk rock, energetic, distorted guitars, 178 bpm" \
  --lyrics-file song.txt --lang en --bpm 178 --duration 180
```

Output: WAV 48 kHz under `outputs/` (gitignored). Full run ≈ 5–8 min (model
load included). Run it in the background and let the agent notify on completion.

## Proven recipes (tuned on this install)

| Recipe | Flags |
| --- | --- |
| Plain text2music | (defaults) `--caption ... --lyrics-file ...` |
| Cover of an existing track | `--cover ref.wav --cover-strength 1.0 --cover-noise 0.5` (max similarity; 0.6/0.15 is "inspired by") |
| Non-English vocals | `--lang es` — works (ISO 639-1); English is the model's strongest language, Spanish good, long words occasionally mispronounced |
| Denser/faster generation | `--steps 8` (turbo sweet spot), `--no-thinking` for quick drafts |

## Gotchas (learned the hard way)

- **Caption is king, and the LM must not touch it.** The CLI forces
  `use_cot_caption=False` — otherwise the LM rewrites your genre caption with
  hallucinated styles (observed: a drum&bass caption over a punk prompt).
- **Language**: `use_cot_language=False` forces `--lang`; with LM detection on,
  it returns "unknown" and overrides your choice.
- **Cover strength 1.0 clones the original recording** (vocals included) —
  legal derivative-work territory. Keep ≤0.8 for "in the style of", and treat
  any celebrity-voice result as publish-at-your-own-risk (right of publicity).
- **No ffmpeg on this machine** — MP3 export fails; WAV via soundfile is the
  working path. m4a references decode via `pyav` (`uv pip install av` in the
  install venv); the CLI handles that automatically for `--cover x.m4a`.
- **Tempo detection**: librosa lives in the *old* `ACE-Step/.venv` (v0.2), not
  in the 1.5 venv. `librosa.beat.beat_track` returns half-time (e.g. 89 for a
  178 BPM punk track) — double it when matching a reference.
- Lyrics tags `[verse]` / `[chorus]` / `[bridge]` / `[end]` structure the
  song; ad-libs in parens `(woo!)` render as backing shouts.
- A `Found N audio code tokens outside valid range` warning in the logs is
  benign — it appears on healthy runs too.

## Legal (personal/local use)

AI output is not copyright-free when it imitates a living artist's voice or
derives from a copyrighted recording at high cover strength. Publishing risks
takedowns + right-of-publicity claims. Personal local listening: low risk.
