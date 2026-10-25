# Social preview kit

Source for `docs/social-preview.jpg` (1280x640, GitHub social preview; the lockup stays inside the centered square so chat-app thumbnails don't crop it).

## Rebuild

Needs Python 3, Google Chrome/Chromium and ffmpeg.

```bash
python3 docs/social-preview/render.py
```

Defaults use the files in this folder. Override with `--background`, `--icon`, `--name "Line1|Line2"`, `--tagline`, `--out`.
Then upload `docs/social-preview.jpg` in Settings > General > Social preview (GitHub requires < 1 MB).

## Background prompt

`background.jpg` was generated with Codex image generation:

> Abstract expressive oil painting filling the whole frame, wide 16:9: thick visible brushstrokes, canvas texture, soft painterly blending, diagonal sweeping strokes, editorial OpenAI-blog-cover aesthetic. ABSOLUTELY NO text, letters, logos, symbols, faces or objects. Keep the center calmer and mid-tone so white text stays readable. Palette: fresh bright green and lime family with accents of coral, pink, turquoise and golden yellow.

## Credits

- Icon: `wechat` from [Simple Icons](https://simpleicons.org) (CC0). WeChat is a trademark of Tencent; this project is unofficial and not affiliated with Tencent.
- Background: AI-generated, no third-party artwork.
