find . -name "*.webp" -print0 | parallel -0 dwebp {} -o {.}.png
find . -name "*.webp" -type f -delete