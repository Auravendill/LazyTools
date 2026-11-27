#!/bin/bash

# === Einstellungen ===
INPUT_DIR="./vid"
OUTPUT_DIR="./converted"
CRF=30
PRESET=4

# === Ab hier nichts mehr ändern ===
mkdir -p "$OUTPUT_DIR"

# Dateien nach Größe sortieren (kleinste zuerst)
mapfile -t files < <(
  find "$INPUT_DIR" -maxdepth 1 -type f \( \
    -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.avi' -o \
    -iname '*.mov' -o -iname '*.webm' -o -iname '*.m4v' -o \
    -iname '*.flv' -o -iname '*.wmv' -o -iname '*.ts' -o \
    -iname '*.mts' \
  \) -printf '%s %p\n' | sort -n | cut -d' ' -f2-
)

if [ ${#files[@]} -eq 0 ]; then
  echo "Keine Videodateien gefunden."
  exit 0
fi

echo "Gefundene Dateien (kleinste zuerst): ${#files[@]}"
echo

for file in "${files[@]}"; do
  [ -f "$file" ] || continue

  filename=$(basename "$file")
  name="${filename%.*}"
  output="$OUTPUT_DIR/${name}.mkv"
  size=$(du -h "$file" | cut -f1)

  echo "→ Konvertiere ($size): $filename"

  tmp_output="${output}.tmp.mkv"

  if ffmpeg -n -i "$file" \
      -c:v libsvtav1 \
      -crf "$CRF" \
      -preset "$PRESET" \
      -pix_fmt yuv420p10le \
      -svtav1-params tune=0:enable-variance-boost=1 \
      -c:a libopus -b:a 96k \
      "$tmp_output"; then

    mv "$tmp_output" "$output"
    rm -f "$file"
    echo "✓ Fertig & Original gelöscht: $filename"
  else
    rm -f "$tmp_output"
    echo "✗ FEHLER bei: $filename (Original bleibt)"
  fi

  echo
done

echo "Alle Dateien verarbeitet."