#!/usr/bin/env python3
"""テトラニコの画像を作り直す (assets/niko/)。

レンダー済みの透過 PNG 連番 (Vmodel/tetra_teto/renders) から、ページで使うコマだけを切り出して WebP にする。
blend ファイルには触らない。Pillow だけで動く。

    python3 scripts/build-niko.py
    python3 scripts/build-niko.py --renders /path/to/tetra_teto/renders

コマ番号や切り出し範囲を変えたら、index.html の NIKO (コマ数・列数・大きさ) も合わせる。最後に表示される値を写す。
"""
import argparse
import pathlib
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "niko"
DEFAULT_RENDERS = pathlib.Path.home() / "project/Vmodel/tetra_teto/renders"
INTRO = "tetraniko_intro_v037"  # 1〜551 トーク、552〜659 チャールストン

# 顔 (会話の窓に出す)。値は INTRO のコマ番号
FACES = {"idle": 1, "smile": 60, "talk": 127, "talk2": 449, "happy": 211, "hmph": 29, "wink": 533, "soft": 239}
FACE_BOX = (290, 370, 790, 930)
FACE_SIZE = (300, 336)

# 手を振る (ヒーロー)
WAVE_FRAMES = list(range(1, 86, 2))
WAVE_BOX = (40, 370, 1060, 1500)
WAVE_SIZE = (400, 443)
WAVE_COLS = 8

# 開幕で大きく出す (手を上げて振るところまで)。大きく映るので、ヒーロー用より細かく作る。3 コマおき = 10fps
OPEN_FRAMES = list(range(1, 68, 3))
OPEN_SIZE = (560, 620)
OPEN_COLS = 6

# チャールストン (隠しステージ)
DANCE_FRAMES = list(range(552, 660, 2))
DANCE_BOX = (165, 445, 908, 1915)
DANCE_SIZE = (230, 455)
DANCE_COLS = 9

# 自己紹介で話す (音声に合わせてコマを送る)。30fps の連番を 3 コマおき = 10fps
TALK_FRAMES = list(range(1, 552, 3))
TALK_BOX = (240, 370, 960, 1130)
TALK_SIZE = (256, 270)
TALK_COLS = 16
VOICE = "audio/tetraniko_intro.wav"  # renders の隣。口パクは音声より 0.6 秒遅れて始まる (index.html の NIKO.talk.lead)


def frame(renders: pathlib.Path, n: int) -> Image.Image:
    return Image.open(renders / INTRO / f"frame_{n:04d}.png").convert("RGBA")


def cut(renders, n, box, size):
    return frame(renders, n).crop(box).resize(size, Image.LANCZOS)


def sheet(renders, frames, box, size, cols, name, quality):
    rows = (len(frames) + cols - 1) // cols
    im = Image.new("RGBA", (cols * size[0], rows * size[1]), (0, 0, 0, 0))
    for i, n in enumerate(frames):
        im.paste(cut(renders, n, box, size), ((i % cols) * size[0], (i // cols) * size[1]))
    im.save(OUT / name, "WEBP", quality=quality, method=6)
    print(f"{name}: frames={len(frames)} cols={cols} w={size[0]} h={size[1]} ({(OUT / name).stat().st_size // 1024} KB)")


def voice(renders):
    """自己紹介の声 (wav → m4a)。afconvert は macOS に入っている"""
    src = renders.parent / VOICE
    if not src.exists() or not shutil.which("afconvert"):
        print(f"voice.m4a: 作れない ({src} か afconvert が無い)。前のものを残す")
        return
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", str(src), str(OUT / "voice.m4a")], check=True)
    print(f"voice.m4a ({(OUT / 'voice.m4a').stat().st_size // 1024} KB)")


def font(size, bold=True):
    for path, index in (("/System/Library/Fonts/Avenir Next.ttc", 0 if bold else 7), ("/System/Library/Fonts/Helvetica.ttc", 1 if bold else 0)):
        try:
            return ImageFont.truetype(path, size, index=index)
        except OSError:
            continue
    return ImageFont.load_default()


def og(renders):
    """SNS にリンクを貼ったときの画像 (1200x630)"""
    w, h = 1200, 630
    im = Image.new("RGB", (w, h), "#070C1C")
    glow = Image.new("RGB", (w, h), "#070C1C")
    d = ImageDraw.Draw(glow)
    for x, y, r, c in ((180, 40, 460, "#1B3C9C"), (1000, 140, 420, "#1F6FC4"), (560, 640, 380, "#1B5E88"), (1150, 620, 300, "#2A4A8A")):
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(140)), 0.9)
    niko = frame(renders, 60).crop((40, 370, 1060, 1500))
    niko = niko.resize((int(niko.width * 700 / niko.height), 700), Image.LANCZOS)
    im.paste(niko, (w - niko.width - 10, 20), niko)
    d = ImageDraw.Draw(im)
    d.text((72, 190), "tetra2585", font=font(96), fill="#FFFFFF")
    d.text((72, 300), "Apps", font=font(96), fill="#4FB3FF")
    d.text((76, 430), "guided by Tetra Niko", font=font(34, bold=False), fill="#C9D6F5")
    im.save(OUT / "og.jpg", "JPEG", quality=86, optimize=True)
    print(f"og.jpg ({(OUT / 'og.jpg').stat().st_size // 1024} KB)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--renders", type=pathlib.Path, default=DEFAULT_RENDERS)
    renders = p.parse_args().renders
    OUT.mkdir(parents=True, exist_ok=True)

    for name, n in FACES.items():
        cut(renders, n, FACE_BOX, FACE_SIZE).save(OUT / f"face-{name}.webp", "WEBP", quality=82, method=6)
    print(f"faces: {', '.join(FACES)} ({sum((OUT / f'face-{k}.webp').stat().st_size for k in FACES) // 1024} KB)")

    # 最初に出す 1 枚 (シートが届くまで) と、診断カード用の大きい 1 枚
    cut(renders, WAVE_FRAMES[0], WAVE_BOX, (WAVE_SIZE[0] * 2, WAVE_SIZE[1] * 2)).save(OUT / "hero.webp", "WEBP", quality=80, method=6)
    cut(renders, FACES["wink"], WAVE_BOX, (900, 997)).save(OUT / "card.webp", "WEBP", quality=84, method=6)
    cut(renders, TALK_FRAMES[0], TALK_BOX, (TALK_SIZE[0] * 2, TALK_SIZE[1] * 2)).save(OUT / "about.webp", "WEBP", quality=80, method=6)
    print(f"hero.webp ({(OUT / 'hero.webp').stat().st_size // 1024} KB), card.webp ({(OUT / 'card.webp').stat().st_size // 1024} KB), about.webp ({(OUT / 'about.webp').stat().st_size // 1024} KB)")

    sheet(renders, WAVE_FRAMES, WAVE_BOX, WAVE_SIZE, WAVE_COLS, "wave.webp", 62)
    sheet(renders, OPEN_FRAMES, WAVE_BOX, OPEN_SIZE, OPEN_COLS, "open.webp", 60)
    sheet(renders, DANCE_FRAMES, DANCE_BOX, DANCE_SIZE, DANCE_COLS, "dance.webp", 62)
    sheet(renders, TALK_FRAMES, TALK_BOX, TALK_SIZE, TALK_COLS, "talk.webp", 55)
    voice(renders)
    og(renders)


if __name__ == "__main__":
    main()
