#!/usr/bin/env python3
"""ACE-Step 1.5 music generation CLI (portable part of the local ACE-Step install).

The model install, venv and checkpoints live OUTSIDE this repo (local content,
several GB). Point ACESTEP_HOME at that install before running:

    ACESTEP_HOME=C:/Agentic-Quality-Engineer/Projects/bunkai/acestep-local/ACE-Step-1.5

Run with the install's own venv python:

    "$ACESTEP_HOME/.venv/Scripts/python.exe" acestep/generate.py \
        --caption "punk rock, energetic, 178 bpm" \
        --lyrics-file song.txt \
        --lang en --bpm 178 --duration 180

Cover mode (reuse an existing recording's structure/vocals):

    "$ACESTEP_HOME/.venv/Scripts/python.exe" acestep/generate.py \
        --caption "punk rock cover" --lyrics-file song.txt \
        --cover reference.wav --cover-strength 1.0 --cover-noise 0.5
"""
import argparse
import os
import sys

os.environ.setdefault("ACESTEP_LM_BACKEND", "pt")

DEFAULT_HOME = r"C:\Agentic-Quality-Engineer\Projects\bunkai\acestep-local\ACE-Step-1.5"


def parse_args():
    parser = argparse.ArgumentParser(description="Generate music with local ACE-Step 1.5")
    parser.add_argument("--caption", required=True, help="Style caption, <512 chars, English")
    parser.add_argument("--lyrics", default=None, help="Inline lyrics (with [verse]/[chorus] tags)")
    parser.add_argument("--lyrics-file", default=None, help="Path to lyrics file (overrides --lyrics)")
    parser.add_argument("--lang", default="en", help="Vocal language, ISO 639-1 (en, es, ...)")
    parser.add_argument("--bpm", type=int, default=120)
    parser.add_argument("--timesignature", default="4/4")
    parser.add_argument("--duration", type=float, default=180.0)
    parser.add_argument("--steps", type=int, default=8, help="Inference steps (turbo model: 8)")
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--output-dir", default=None, help="Default: <this dir>/../outputs")
    parser.add_argument("--cover", default=None, help="Source audio for cover mode (wav/flac/m4a)")
    parser.add_argument("--cover-strength", type=float, default=0.6, help="Max similarity = 1.0 (1.0 clones the original)")
    parser.add_argument("--cover-noise", type=float, default=0.15)
    parser.add_argument("--no-thinking", action="store_true", help="Skip LM CoT phases (faster, lower quality)")
    return parser.parse_args()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()

    home = os.environ.get("ACESTEP_HOME", DEFAULT_HOME)
    if not os.path.isdir(home):
        sys.exit(f"ACESTEP_HOME not found: {home} — set it to your ACE-Step-1.5 install")
    sys.path.insert(0, home)

    if args.lyrics_file:
        with open(args.lyrics_file, encoding="utf-8") as handle:
            lyrics = handle.read()
    else:
        lyrics = args.lyrics or ""

    from acestep.gpu_config import get_gpu_config, set_global_gpu_config
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationConfig, GenerationParams, generate_music
    from acestep.llm_inference import LLMHandler
    from acestep.model_downloader import ensure_lm_model

    gpu_config = get_gpu_config()
    set_global_gpu_config(gpu_config)
    print(f"GPU tier: {gpu_config.tier}, VRAM: {gpu_config.gpu_memory_gb:.2f} GB")

    dit_handler = AceStepHandler()
    llm_handler = LLMHandler()
    use_flash = dit_handler.is_flash_attention_available("auto")
    quantization = "int8_weight_only" if gpu_config.quantization_default else None

    init_status, enable_generate = dit_handler.initialize_service(
        project_root=home,
        config_path="acestep-v15-turbo",
        device="auto",
        use_flash_attention=use_flash,
        compile_model=False,
        offload_to_cpu=True,
        offload_dit_to_cpu=getattr(gpu_config, "offload_dit_to_cpu_default", True),
        quantization=quantization,
        prefer_source=None,
    )
    if not enable_generate:
        sys.exit(f"DiT init failed: {init_status}")

    checkpoint_dir = os.path.join(home, "checkpoints")
    ok, msg = ensure_lm_model(
        model_name="acestep-5Hz-lm-0.6B",
        checkpoints_dir=checkpoint_dir,
        prefer_source=None,
    )
    if not ok:
        sys.exit(f"LM download failed: {msg}")

    lm_status, lm_ok = llm_handler.initialize(
        checkpoint_dir=checkpoint_dir,
        lm_model_path="acestep-5Hz-lm-0.6B",
        backend="pt",
        device="auto",
        offload_to_cpu=True,
        dtype=None,
    )
    if not lm_ok:
        sys.exit(f"LM init failed: {lm_status}")

    cover_path = None
    if args.cover:
        cover_path = args.cover
        if cover_path.lower().endswith(".m4a"):
            import av

            wav_path = os.path.splitext(cover_path)[0] + "_48k.wav"
            if not os.path.exists(wav_path):
                container = av.open(cover_path)
                resampler = av.audio.resampler.AudioResampler(format="fltp", layout="stereo", rate=48000)
                frames = []
                for frame in container.decode(audio=0):
                    frames.extend(resampler.resample(frame))
                frames.extend(resampler.resample(None))
                import soundfile

                import numpy as np

                array = np.concatenate([f.to_ndarray() for f in frames], axis=1)
                soundfile.write(wav_path, array.T, 48000)
            cover_path = wav_path

    params = GenerationParams(
        caption=args.caption,
        lyrics=lyrics,
        vocal_language=args.lang,
        bpm=args.bpm,
        timesignature=args.timesignature,
        duration=args.duration,
        inference_steps=args.steps,
        thinking=not args.no_thinking,
        use_cot_caption=False,  # keep OUR caption verbatim (LM otherwise hallucinates genres)
        use_cot_lyrics=False,
        use_cot_language=False,  # force --lang (LM auto-detect would override it)
        seed=args.seed,
        enable_normalization=True,
    )
    if cover_path:
        params.task_type = "cover"
        params.src_audio = cover_path
        params.audio_cover_strength = args.cover_strength
        params.cover_noise_strength = args.cover_noise

    config = GenerationConfig(
        batch_size=1,
        use_random_seed=False,
        seeds=[args.seed],
        audio_format="wav",  # MP3 needs ffmpeg; WAV is the dependency-free path
        mp3_bitrate="320k",
    )

    output_dir = args.output_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    result = generate_music(dit_handler, llm_handler, params, config, save_dir=output_dir)
    data = result.to_dict()
    print("STATUS:", data.get("status_message"), "| success:", data.get("success"), "| error:", data.get("error"))
    for audio in data.get("audios") or []:
        print("AUDIO PATH:", audio.get("path"))
    return 0 if data.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
