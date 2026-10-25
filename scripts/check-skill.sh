#!/bin/bash
# Validate the bundled skill: frontmatter present and every referenced icon exists.
set -eu
cd "$(dirname "$0")/.."
SKILL=skills/wechat-multifix/SKILL.md
[ -f "$SKILL" ] || { echo "missing $SKILL"; exit 1; }
[ "$(sed -n 1p "$SKILL")" = "---" ] || { echo "frontmatter must start on line 1"; exit 1; }
FM=$(awk 'NR>1 && /^---$/ {exit} NR>1 {print}' "$SKILL")
echo "$FM" | grep -q '^name: wechat-multifix$' || { echo "frontmatter: name must be wechat-multifix"; exit 1; }
echo "$FM" | grep -q '^description:' || { echo "frontmatter: description missing"; exit 1; }
status=0
for icon in $(grep -oE 'AppIcon-[a-z]+\.icns' "$SKILL" "README.md" "README.zh-CN.md" | sed 's/.*://' | sort -u); do
  if [ ! -f "skills/wechat-multifix/icons/$icon" ]; then echo "missing icon: $icon"; status=1; fi
done
for img in $(grep -oE 'skills/wechat-multifix/icons/previews/[a-z-]+\.png' README.md README.zh-CN.md | sed 's/.*://' | sort -u); do
  [ -f "$img" ] || { echo "missing image: $img"; status=1; }
done
[ $status -eq 0 ] && echo "skill OK"
exit $status
