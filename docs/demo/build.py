#!/usr/bin/env python3
"""Render docs/demo.gif: HTML frames -> headless Chrome (2x) -> ffmpeg palette GIF.

Synthetic, rendered demo only. It never touches WeChat or /Applications.
Rebuild:  python3 docs/demo/build.py   (needs Google Chrome + ffmpeg)
"""
import html, pathlib, subprocess, tempfile, shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
ICON = ROOT / "skills/wechat-multifix/icons/previews/black.png"
OUT = ROOT / "docs/demo.gif"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 960, 540

# (kind, text) terminal script. kind: u=user prompt, c=command, o=output
LINES = [
    ("u", "Install WeChat multi-open with the black icon."),
    ("o", "Reading skills/wechat-multifix/SKILL.md ..."),
    ("c", "cp -R /Applications/WeChat.app /Applications/WeChat2.app"),
    ("c", "PlistBuddy -c \"Set :CFBundleIdentifier com.tencent.xinWeChat2\" …/Info.plist"),
    ("c", "xattr -cr /Applications/WeChat2.app"),
    ("c", "codesign --force --deep --sign - /Applications/WeChat2.app"),
    ("c", "cp icons/AppIcon-black.icns …/WeChat2.app/Contents/Resources/AppIcon.icns"),
    ("c", "codesign --force --deep --sign - /Applications/WeChat2.app"),
    ("o", "Done. WeChat = com.tencent.xinWeChat, WeChat2 = com.tencent.xinWeChat2 (differ)."),
]

def term(n, typed=None):
    rows = []
    for i, (k, t) in enumerate(LINES[:n]):
        if i == n - 1 and typed is not None:
            t = t[:typed]
        t = html.escape(t)
        if k == "u":
            rows.append(f'<div class="u">{t}</div>')
        elif k == "c":
            rows.append(f'<div class="c"><b>$</b> {t}</div>')
        else:
            rows.append(f'<div class="o">{t}</div>')
    return "\n".join(rows)

def dock(stage):
    # stage 0: one WeChat; 1: copy appears (green); 2: black icon swapped; 3: bounce
    green = '<div class="ic green"><img src="{i}"/></div>'.format(i=ICON.as_uri())
    black = '<div class="ic"><img src="{i}"/></div>'.format(i=ICON.as_uri())
    second = ""
    label2 = ""
    if stage == 1:
        second = green.replace('class="ic green"', 'class="ic green ghost"')
        label2 = "WeChat2"
    elif stage == 2:
        second = black
        label2 = "WeChat2"
    elif stage >= 3:
        second = black.replace('class="ic"', 'class="ic pop"')
        label2 = "WeChat2"
    others = "".join(f'<div class="ic g{j}"></div>' for j in range(3))
    return f'''<div class="dock">{others}
<div class="slot">{green}<span>WeChat</span></div>
<div class="slot">{second}<span>{label2}</span></div></div>'''

def page(n, typed, stage, caption):
    return f'''<!doctype html><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0}}
body{{width:{W}px;height:{H}px;background:linear-gradient(135deg,#2b3a67,#6b5b95 55%,#c06c84);font-family:-apple-system,"SF Pro Text","Helvetica Neue",sans-serif;overflow:hidden;position:relative}}
.win{{position:absolute;left:28px;top:28px;width:560px;height:484px;border-radius:12px;background:#1c1d22;box-shadow:0 18px 40px rgba(0,0,0,.45);overflow:hidden}}
.bar{{height:34px;background:#2a2b31;display:flex;align-items:center;padding:0 12px;gap:7px;color:#9a9ca5;font-size:12px}}
.bar i{{width:11px;height:11px;border-radius:50%;display:inline-block}}
.body{{padding:16px 18px;font:13px/1.5 Menlo,monospace;color:#d6d8de}}
.u{{background:#34364a;border-radius:10px;padding:9px 12px;margin:0 0 12px 60px;font-family:-apple-system,sans-serif;font-size:14px;color:#fff}}
.c{{color:#e9ecf5;margin:3px 0;word-break:break-all}} .c b{{color:#7ee0a0}}
.o{{color:#8f93a1;margin:6px 0;font-family:-apple-system,sans-serif;font-size:13px}}
.right{{position:absolute;left:608px;top:28px;width:324px;height:484px}}
.cap{{color:#fff;font-size:18px;font-weight:600;text-align:center;margin-top:30px;text-shadow:0 2px 8px rgba(0,0,0,.4);height:52px;line-height:1.3}}
.stagebox{{position:absolute;bottom:0;left:0;right:0;height:300px}}
.dock{{position:absolute;bottom:0;left:-8px;right:-8px;height:92px;border-radius:24px;background:rgba(255,255,255,.22);border:1px solid rgba(255,255,255,.35);backdrop-filter:blur(8px);display:flex;align-items:flex-end;justify-content:center;gap:10px;padding:10px 10px 14px}}
.slot{{display:flex;flex-direction:column;align-items:center;gap:4px;width:64px;position:relative}}
.slot span{{position:absolute;top:-42px;font-size:12px;color:#fff;background:rgba(0,0,0,.55);padding:2px 7px;border-radius:6px;white-space:nowrap}}
.slot span:empty{{display:none}}
.ic{{width:60px;height:60px;border-radius:14px;overflow:hidden;position:relative;background:#000;flex:none}}
.ic img{{width:100%;height:100%;display:block}}
.ic.green{{background:#07c160}} .ic.green img{{mix-blend-mode:screen}}
.ghost{{opacity:.45}} .pop{{transform:translateY(-6px) scale(1.08);box-shadow:0 10px 18px rgba(0,0,0,.4)}}
.g0{{background:#5ac8fa}}.g1{{background:#ffcc00}}.g2{{background:#af52de}}
.g0,.g1,.g2{{width:52px;height:52px;opacity:.85;margin-bottom:4px}}
</style>
<div class="win"><div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i>&nbsp; agent session (illustrative)</div>
<div class="body">{term(n, typed)}</div></div>
<div class="right"><div class="cap">{caption}</div><div class="stagebox">{dock(stage)}</div></div>'''

def frames():
    f = []  # (html, seconds)
    f.append((page(0, None, 0, "Your Dock: one WeChat"), 1.2))
    f.append((page(1, None, 0, "One sentence to your agent"), 1.6))
    f.append((page(2, None, 0, "Following SKILL.md…"), 0.8))
    f.append((page(3, None, 1, "Copy WeChat → WeChat2"), 1.4))
    f.append((page(4, None, 1, "New Bundle ID"), 1.2))
    f.append((page(5, None, 1, "Strip attributes"), 0.9))
    f.append((page(6, None, 1, "Ad-hoc re-sign"), 1.2))
    f.append((page(7, None, 2, "Swap in the black icon"), 1.3))
    f.append((page(8, None, 2, "Re-sign again"), 1.1))
    f.append((page(9, None, 3, "Two WeChats, told apart at a glance"), 3.2))
    return f

def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="demo-frames-"))
    try:
        lst = []
        for i, (doc, sec) in enumerate(frames()):
            h = tmp / f"f{i:02d}.html"; h.write_text(doc)
            p = tmp / f"f{i:02d}.png"
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=2", f"--window-size={W},{H}",
                            "--allow-file-access-from-files", "--virtual-time-budget=500",
                            f"--screenshot={p}", h.as_uri()],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            lst += [f"file '{p}'", f"duration {sec}"]
        lst.append(lst[-2])
        (tmp / "list.txt").write_text("\n".join(lst))
        pal = tmp / "pal.png"
        vf = f"fps=10,scale={W}:-1:flags=lanczos"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
                        "-vf", vf + ",palettegen=max_colors=96", str(pal)], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
                        "-i", str(pal), "-lavfi", vf + "[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4",
                        "-loop", "0", str(OUT)], check=True)
        if shutil.which("gifsicle"):
            subprocess.run(["gifsicle", "-O3", "--lossy=40", "-b", str(OUT)], check=False)
        if __import__("os").environ.get("KEEP_FRAMES"):
            shutil.copytree(tmp, ROOT / "docs/demo/_frames", dirs_exist_ok=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
