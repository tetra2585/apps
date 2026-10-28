#!/usr/bin/env python3
"""
新しいアプリを一覧に足す (または画像を入れ直す)。

  python3 scripts/add-app.py --id toviqu --store-id 1234567890 --name TOVIQU \
      --screens-ja path/to/ja --screens-en path/to/en --shots 01_home:home,03_done:done,04_list:list \
      --mascot path/to/mascot.png

- アイコンは App Store から取得する (iTunes Search API)。まだ App Store に無いアプリは --icon で画像を渡す
- 画面は 1206×2622 などの縦長のスクリーンショット (枠なし) を 540px 幅の JPEG にして assets/ に入れる
- 文章 (ja / en の tagline・desc・feats・price) は apps.json に「TODO」で入るので、書き換える
- 同じ --id がすでにあれば、画像だけ入れ直して文章はそのまま残す
"""
import argparse
import json
import pathlib
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent


def save_shot(src: pathlib.Path, dst: pathlib.Path) -> None:
    im = Image.open(src).convert("RGB")
    w = 540
    im.resize((w, round(w * im.height / im.width)), Image.LANCZOS).save(dst, quality=82, optimize=True, progressive=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, help="小文字の英数字 (ページ内のリンク #<id> にもなる)")
    p.add_argument("--store-id", required=True, help="App Store の数字の ID")
    p.add_argument("--name", required=True)
    p.add_argument("--screens-ja", required=True)
    p.add_argument("--screens-en", required=True)
    p.add_argument("--shots", required=True, help="ファイル名(拡張子なし):表示名 をカンマ区切りで 3 つ。例 01_home:home,03_done:done")
    p.add_argument("--mascot", help="背景が透明な PNG (キャラクター)")
    p.add_argument("--icon", help="App Store に無いときのアイコン画像")
    p.add_argument("--support", default="")
    a = p.parse_args()

    (ROOT / "icons").mkdir(exist_ok=True)
    (ROOT / "assets").mkdir(exist_ok=True)

    icon_path = ROOT / "icons" / f"{a.id}.jpg"
    if a.icon:
        Image.open(a.icon).convert("RGB").resize((512, 512), Image.LANCZOS).save(icon_path, quality=88)
    else:
        with urllib.request.urlopen(f"https://itunes.apple.com/lookup?id={a.store_id}&country=jp") as r:
            results = json.load(r)["results"]
        if not results:
            raise SystemExit("App Store にアプリが見つかりません。--icon で画像を渡してください")
        urllib.request.urlretrieve(results[0]["artworkUrl512"], icon_path)

    names = []
    for pair in a.shots.split(","):
        file_stem, name = pair.split(":")
        names.append(name)
        for lang, folder in (("ja", a.screens_ja), ("en", a.screens_en)):
            src = next(pathlib.Path(folder).glob(f"{file_stem}.*"))
            save_shot(src, ROOT / "assets" / f"{a.id}-{name}-{lang}.jpg")

    mascot = ""
    if a.mascot:
        im = Image.open(a.mascot).convert("RGBA")
        im = im.crop(im.getbbox())
        im.thumbnail((520, 520), Image.LANCZOS)
        mascot = f"assets/{a.id}-mascot.png"
        im.save(ROOT / mascot, optimize=True)

    data_path = ROOT / "apps.json"
    data = json.loads(data_path.read_text())
    existing = next((x for x in data["apps"] if x["id"] == a.id), None)
    todo = {"tagline": "TODO", "desc": "TODO", "feats": [["✨", "TODO"], ["✨", "TODO"], ["✨", "TODO"]], "price": "TODO", "mascotAlt": "TODO"}
    entry = existing or {
        "id": a.id,
        "name": a.name,
        "storeId": a.store_id,
        "ja": dict(todo),
        "en": dict(todo),
        "theme": {"glow": "rgba(139,116,255,.40)", "tint": "rgba(139,116,255,.25)", "accent": "#8B74FF", "accent2": "#FF8FB3"},
    }
    entry.update({"icon": f"icons/{a.id}.jpg", "screens": names, "support": a.support or entry.get("support", "")})
    if mascot:
        entry["mascot"] = mascot
    if not existing:
        data["apps"].append(entry)
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"{'更新' if existing else '追加'}しました: {a.id}。apps.json の文章 (TODO) と theme の色を確認してください")


if __name__ == "__main__":
    main()
