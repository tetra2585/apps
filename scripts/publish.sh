#!/bin/sh
# 変更をコミットして GitHub に送る。GitHub Pages が数分で https://tetra2585.github.io/apps/ に反映する。
#   sh scripts/publish.sh "Add TOVIQU"
set -eu
cd "$(dirname "$0")/.."
msg="${1:-Update the app list}"
# apps.json が壊れていると、ページにアプリが何も出なくなるので先に確かめる
python3 -c "import json; d=json.load(open('apps.json')); assert d['apps'], 'apps.json にアプリがありません'"
if grep -q '"TODO"' apps.json; then
  echo "apps.json に TODO が残っています。文章を書いてから公開してください" >&2
  exit 1
fi
git add -A
if git diff --cached --quiet; then
  echo "変更はありません"
  exit 0
fi
git commit -q -m "$msg"
git push -q origin main
echo "公開しました: https://tetra2585.github.io/apps/ (反映まで数分かかることがあります)"
