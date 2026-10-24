# Pi & Planck website runbook

Live site: https://piandplanck.github.io  (repo piandplanck/piandplanck.github.io, branch main, Pages source: GitHub Actions)

## Layout
- `_src/data/pieces.json`: one entry per piece (id, slug, date, topic, title, title_fa, caption, caption_fa, alt, alt_fa, sources)
- `_src/img/<id>_en.jpg`, `<id>_fa.jpg` (1600x900) and `_t.jpg` thumbnails (640x360)
- `_src/assets/`: logo, favicon, og image, headline font
- `_src/build.py`: standard-library builder -> `_site/`
- `.github/workflows/site.yml`: build and deploy on push, every Sunday 18:00 UTC, and manually

## Weekly publishing rule
The build shows only pieces dated on or before the most recent Saturday (Pacific). New pieces can be pushed any time; they stay hidden until the next Sunday build.

## Add a piece
1. Add an entry to `_src/data/pieces.json` (captions without the @handle) and the four images.
2. `python3 _src/build.py --out _site --through YYYY-MM-DD` to check locally.
3. `git add -A && git commit -m "Add piece <id>" && git push origin HEAD:main`.

## Rules
Nothing secret in this public repo. No dates printed on graphics. Sources listed on each piece page.
