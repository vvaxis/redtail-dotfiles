#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
CURRENT="$DIR/.palette.current"
TARGET="$DIR/palette.conf"

if [[ ! -f "$CURRENT" ]]; then
    echo "No .palette.current found. Run: cp palette.conf .palette.current"
    exit 1
fi

# Config files to recolor
FILES=(
    "$HOME/.config/foot/foot.ini"
    "$HOME/.config/dunst/dunstrc"
    "$HOME/.config/fuzzel/fuzzel.ini"
    "$HOME/.config/niri/config.kdl"
    "$HOME/.config/gtk-3.0/gtk.css"
    "$HOME/.config/gtk-4.0/gtk.css"
    "$HOME/.config/swaylock/config"
    "$HOME/.config/starship.toml"
    "$HOME/.config/yazi/theme.toml"
    "$HOME/.config/micro/colorschemes/redtail.micro"
    "$HOME/.config/btop/themes/redtail.theme"
    "$HOME/.zshrc.local"
    "$HOME/.config/ignis/style.css"
)

# Convert 6-char hex to "R, G, B" decimal string
hex_to_rgb() {
    printf "%d, %d, %d" "0x${1:0:2}" "0x${1:2:2}" "0x${1:4:2}"
}

# Read palettes into associative arrays
declare -A OLD NEW
while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" =~ ^# ]] && continue
    OLD[$key]="$value"
done < "$CURRENT"

while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" =~ ^# ]] && continue
    NEW[$key]="$value"
done < "$TARGET"

# Build sed args: two passes to avoid cascading replacements
# Pass 1: old value → temporary token
# Pass 2: temporary token → new value
SED_TOKENIZE=()
SED_RESOLVE=()
CHANGED=0

for key in "${!OLD[@]}"; do
    [[ -z "${NEW[$key]+x}" ]] && continue
    old_val="${OLD[$key]}"
    new_val="${NEW[$key]}"
    if [[ "$old_val" != "$new_val" ]]; then
        # Hex replacement (e.g., 150a04 → 0e0907)
        SED_TOKENIZE+=(-e "s/${old_val}/__P_${key}__/g")
        SED_RESOLVE+=(-e "s/__P_${key}__/${new_val}/g")

        # RGB decimal replacement for rgba()/rgb() contexts
        # Matches "(R, G, B" to avoid false positives on bare numbers
        old_rgb=$(hex_to_rgb "$old_val")
        new_rgb=$(hex_to_rgb "$new_val")
        if [[ "$old_rgb" != "$new_rgb" ]]; then
            SED_TOKENIZE+=(-e "s/(${old_rgb}/(PR_${key}_/g")
            SED_RESOLVE+=(-e "s/(PR_${key}_/(${new_rgb}/g")
        fi

        echo "  $key: $old_val → $new_val  (rgb: $old_rgb → $new_rgb)"
        CHANGED=$((CHANGED + 1))
    fi
done

if [[ $CHANGED -eq 0 ]]; then
    echo "No palette changes detected."
    exit 0
fi

echo "Recoloring $CHANGED value(s) across ${#FILES[@]} configs..."
for f in "${FILES[@]}"; do
    if [[ ! -f "$f" ]]; then
        echo "  SKIP $(basename "$f") (not found)"
        continue
    fi
    sed -i "${SED_TOKENIZE[@]}" "$f"
    sed -i "${SED_RESOLVE[@]}" "$f"
    echo "  $(basename "$f")"
done

# Update current palette
cp "$TARGET" "$CURRENT"
echo "Done."
