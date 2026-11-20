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

広告の誘導先には広告用の印を付ける（普段の投稿と分けて測るため）: `?src=igads`（Instagram 広告）、`fbads`（Facebook 広告）、`tiktokads`、`ytads`。Meta の広告は App Store のリンクを直接使えない（「アプリのインストール」が目的の広告だけ）ので、このページを誘導先にする。例: `https://tetra2585.github.io/apps/?src=igads&app=miveliq&lang=en`

ほかのパラメータ: `?app=miveliq` でそのアプリを先頭に出し「動画で見たのは…」を表示、`?lang=ja|en` で言語を固定（なければ端末の言語。画面右上で切り替えも可）。

## 集計

数える場所は 2 つある。

- **App Store Connect**（ダウンロード）: 上の `?src=` の印で、SNS ごとのダウンロード数がわかる。
- **サイトの集計**（訪問と、ページの中で何をしたか）: `index.html` の `ANALYTICS` に ID を入れると送り始める。空のあいだは何も送らない。`umami` は Umami Cloud の Website ID、`ga4` は Google アナリティクスの測定 ID（`G-…`）。どちらか片方でよい。手元（localhost）では送らない。送るはずの中身は、ブラウザのコンソールで `__track` を見るとわかる。

今は Google アナリティクスのプロパティ「tetra2585 Apps」（測定 ID `G-DWNQFYECS1`）に送っている。Infipix 用のプロパティとは別。下の表の値のうち `src` `app` `from` `section` `kind` `sns` `key` は、レポートで使えるようにカスタム ディメンションとして登録済み（値を増やしたら、管理 → カスタム定義 で足す）。

送る内容。どれにも `src`（どの SNS から来たか）が付く。

| 名前 | いつ | 付く値 |
|---|---|---|
| `visit` | ページを開いた | `lang`, `app`（`?app=` の指定） |
| `reach` | 章が画面に入った（章ごとに 1 回） | `section` = about / apps / stage / finale |
| `demo` | アプリの体験をやり終えた（アプリごとに 1 回） | `app` |
| `store` | App Store へのボタンを押した | `app`, `from` = theater / dock / quiz / list |
| `quiz_open` / `quiz_result` | 診断を開いた / 結果が出た | `app`（結果のみ） |
| `camera` | 最後の章で撮り方を選んだ | `kind` = live（カメラ）/ file（端末のカメラ・写真）/ none（カメラなし）/ denied（カメラを使えなかった） |
| `photo` | 写真を開いた | `from` = pashlo / finale, `cast`（写ったキャラの数） |
| `share` | シェアのボタンを押した | `kind` = quiz / photo |
| `voice` | ニコの声を再生した | |
| `secret` | ひみつを見つけた | `key`, `n`（見つけた数） |
| `follow` | SNS へのボタンを押した | `sns` |

## ファイル

- `index.html` — ページ本体（夜空・オーロラ、アプリごとの紹介、立体的に傾く iPhone）。外部のライブラリは使わない（フォントだけ Google Fonts）
- `apps.json` — アプリの一覧。文章（ja / en）、App Store の ID、画面、キャラクター、色（`theme`）
- `icons/` `assets/` — アイコン、画面（540px 幅の JPEG）、キャラクター（透過 PNG）
- `assets/niko/` — テトラニコの画像と声（顔、開幕・手を振る・話す・ダンスの連番、シェアカード用、自己紹介の声 `voice.m4a`、SNS のリンク画像 `og.jpg`）
- `scripts/add-app.py` — アプリを足す・画像を入れ直す
- `scripts/build-niko.py` — テトラニコの画像を作り直す
- `scripts/publish.sh` — コミットして公開

## テトラニコ（案内役）

ページの案内役は V モデルのテトラニコ。モデルをブラウザで動かすのではなく、レンダー済みの透過 PNG から切り出した画像（`assets/niko/`）を使う。

- **開幕**: 初めて来た人にだけ、地味なページの下からニコが出てきて、画面を割る演出を見せる（`?intro=1` で必ず見せる、`?intro=0` で見せない。「動きを減らす」設定の端末では出ない）
- **会話の窓**: 画面下でニコが喋る。`?src=` の SNS 名、時間帯、見ている章に合わせてセリフが変わる。アプリごとのセリフは `apps.json` の `ja.niko` / `en.niko`（無ければキャッチコピーを読む）
- **触れる iPhone**: アプリ一覧は、画面に固定した 1 台の iPhone の中身がスクロールで入れ替わる形。アプリごとに、画面の上で動作を 1 つやらせる（Miveliq: 笑顔のつまみでロック解除／TOVIQU: 勤務開始で封印／LOVOW: 約束を宣言して「できた」／PASHLO: 何もしなくても勝手に撮る）。動作は `index.html` の `DEMOS[アプリの id]`、文言は `TEXT` の `demo`。`DEMOS` に無いアプリは、画面が切り替わるだけで並ぶ。動作を終えると、画面は指で左右にめくれる（左右の端のタップでも送れる）。「↻」で動作をやり直せる。「動きを減らす」設定の端末では、固定しない従来の並び（説明文と特徴つき）で出す
- **診断**: 3 問でアプリを 1 つ選び、シェア用の縦長カード（1080x1920）を作る。入口はヒーローのボタン。カードは PASHLO で撮れる写真と同じ形（白いふちの写真に、ニコと、触ったアプリのキャラが写る）。シェアされたリンクは `?src=share` になり、App Store のキャンペーンで数えられる。質問と配点は `index.html` の `TEXT.*.quiz`（アプリを足したら配点にも足す）
- **自己紹介**: ヒーローのすぐ下、アプリ一覧の前に「ニコって、誰？」の章。「声で聞く」を押すと、自己紹介動画の声（英語）に合わせてニコが話し、字幕が出る。文面は `index.html` の `aboutSay` / `aboutFacts` / `aboutSubs`
- **隠しステージ**: タップするほどニコが踊る。ひみつは 4 つ（ニコを何度もタップ／ページを離れて戻る／踊らせる／4 つのアプリを全部触る）
- **最後の章**: 「ニコと撮る」で、その時点で触ったアプリのキャラと写真を撮れる。カメラを起動すると、自分の隣にニコが写る（`camOpen`）。カメラを使えない端末では、端末のカメラか写真の選択に切り替わる。カメラなしでも撮れる。写真は端末の中で作り、どこにも送らない。その下に TikTok・YouTube・Instagram へのリンク（`index.html` の `#finale`）
- **見た目**: 色はニコに合わせて紺・水色・白（`:root` の変数）。アプリごとの色は、触れる iPhone の中だけで使う
- 画像の作り直し: `python3 scripts/build-niko.py`（元の連番は `~/project/Vmodel/tetra_teto/renders` の `tetraniko_intro_v037`、声は `audio/tetraniko_intro.wav`。声の変換は macOS の `afconvert`。コマ番号や大きさを変えたら `index.html` の `NIKO` も合わせる）

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
