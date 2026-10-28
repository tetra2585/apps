# tetra2585 Apps

個人開発の iPhone アプリの一覧ページ。各 SNS のプロフィールのリンクに使う（LOVOW・Miveliq で共通）。
このフォルダがそのまま GitHub Pages で公開されている: https://tetra2585.github.io/apps/ （リポジトリ `tetra2585/apps`、`main` のルート）

## SNS のプロフィールに置くリンク

`?src=` が App Store のキャンペーンの印（`ct=`）になり、App Store Connect → アナリティクス → キャンペーンで SNS ごとのダウンロード数がわかる（`?src=` なしは `ct=lp`）。

| SNS | リンク |
|---|---|
| TikTok | https://tetra2585.github.io/apps/?src=tiktok |
| Instagram | https://tetra2585.github.io/apps/?src=instagram |
| YouTube（チャンネルのリンク） | https://tetra2585.github.io/apps/?src=youtube |
| X | https://tetra2585.github.io/apps/?src=x |

ほかのパラメータ: `?app=miveliq` でそのアプリを先頭に出し「動画で見たのは…」を表示、`?lang=ja|en` で言語を固定（なければ端末の言語。画面右上で切り替えも可）。

## ファイル

- `index.html` — ページ本体（夜空・オーロラ、アプリごとの紹介、立体的に傾く iPhone）。外部のライブラリは使わない（フォントだけ Google Fonts）
- `apps.json` — アプリの一覧。文章（ja / en）、App Store の ID、画面、キャラクター、色（`theme`）
- `icons/` `assets/` — アイコン、画面（540px 幅の JPEG）、キャラクター（透過 PNG）
- `scripts/add-app.py` — アプリを足す・画像を入れ直す
- `scripts/publish.sh` — コミットして公開

## 手元で見る

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

http://localhost:8765/?src=tiktok&app=miveliq を開く（`file://` で開くと apps.json が読めない）。Claude Code では `.claude/launch.json` の `tetra2585-apps` で起動できる。

## アプリを足す

```bash
python3 scripts/add-app.py --id toviqu --store-id <App Store の ID> --name TOVIQU \
  --screens-ja <日本語のスクリーンショットのフォルダ> --screens-en <英語のフォルダ> \
  --shots 01_home:home,02_x:x,03_y:y --mascot <キャラの透過 PNG>
```

`apps.json` に入った `TODO` の文章と `theme` の色を書き換え、手元で見てから公開する。並び順は `apps.json` の順（`?app=` で来た人にはそのアプリが先頭）。

## 公開

```bash
sh scripts/publish.sh "Add TOVIQU"
```

`apps.json` に `TODO` が残っていると止まる。
