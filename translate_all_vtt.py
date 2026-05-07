import re
from pathlib import Path
from deep_translator import GoogleTranslator

ROOT = Path(".")

LANGUAGES = ["ar", "fr"]


# ✅ Better chunking (by characters, not lines)
def chunk_text(text_list, max_chars=3000):
    chunk = []
    size = 0

    for line in text_list:
        if size + len(line) > max_chars:
            yield chunk
            chunk = []
            size = 0

        chunk.append(line)
        size += len(line)

    if chunk:
        yield chunk


def translate_vtt(input_file, lang):
    output_file = input_file.with_suffix(f".{lang}.vtt")

    if output_file.exists():
        print(f"✅ Skip exists: {output_file.name}")
        return

    print(f"🌍 Translating: {input_file.name} -> {lang}")

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    text_lines = []
    structure = []

    # 🔹 Separate metadata vs text
    for line in lines:
        stripped = line.strip()

        if (
            stripped == ""
            or stripped == "WEBVTT"
            or "-->" in stripped
            or re.match(r"^\d+$", stripped)
        ):
            structure.append(("meta", line))
        else:
            structure.append(("text", len(text_lines)))
            text_lines.append(stripped)

    translator = GoogleTranslator(source="auto", target=lang)

    translated_parts = []

    try:
        # 🔹 Translate chunks safely
        for chunk in chunk_text(text_lines, 3000):
            big_text = "\n".join(chunk)
            translated_chunk = translator.translate(big_text)

            translated_parts.append(translated_chunk)

    except Exception as e:
        print(f"❌ Translation error in {input_file.name}: {e}")
        return

    # 🔹 Rebuild VTT
    final_lines = []
    text_index = 0

    for item_type, _ in structure:
        if item_type == "meta":
            final_lines.append(_)
        else:
            if text_index < len(translated_parts):
                final_lines.append(translated_parts[text_index] + "\n")
                text_index += 1
            else:
                final_lines.append("\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    print(f"✅ Created: {output_file.name}")


# 🚀 Run for all playlists
for playlist in sorted(ROOT.glob("playlist_*")):

    if not playlist.is_dir():
        continue

    print(f"\n📁 Processing {playlist.name}")

    for vtt in sorted(playlist.glob("*.vtt")):

        if vtt.name.endswith(".ar.vtt") or vtt.name.endswith(".fr.vtt"):
            continue

        print(f"🔍 Checking: {vtt.name}")

        for lang in LANGUAGES:
            translate_vtt(vtt, lang)

print("\n✅ All translations completed.")