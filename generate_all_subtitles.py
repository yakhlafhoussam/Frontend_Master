import os
import subprocess
from pathlib import Path

ROOT = Path(".")
MODEL = "small"
LANGUAGE = "English"

video_extensions = [".mp4", ".mkv", ".mov", ".webm"]

for playlist in sorted(ROOT.glob("playlist_*")):
    if not playlist.is_dir():
        continue

    print(f"\n📁 Playlist: {playlist}")

    videos = sorted([
        f for f in playlist.iterdir()
        if f.suffix.lower() in video_extensions
    ])

    for video in videos:
        subtitle_file = video.with_suffix(".vtt")

        if subtitle_file.exists():
            print(f"✅ Skip already exists: {subtitle_file.name}")
            continue

        print(f"🎬 Generating subtitle for: {video.name}")

        command = [
            "whisper",
            str(video),
            "--model", MODEL,
            "--language", LANGUAGE,
            "--task", "transcribe",
            "--output_format", "vtt",
            "--output_dir", str(playlist)
        ]

        subprocess.run(command)

print("\n✅ All subtitles done.")
