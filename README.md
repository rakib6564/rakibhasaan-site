# rakibhasaan.com

Source for the "Built Different" redesign of rakibhasaan.com.

## Layout

- `copy.md` — page copy (Phase 1 copy doc).
- `site/gen/` — Python generator. `build.py` writes the inner pages; `home_refresh.py` and `home_v3.py` update the home page.
- `site/project/` — the design pages (`*.dc.html`), as published to the design canvas.
- `site/export/` — `export.py` turns the design pages into a plain static site; `dc-static.js` is the small runtime they need; `images/` holds every image.
- `site/dist/` — the built static site, ready to upload.

## Build and deploy

```bash
cd site/gen && python3 build.py && python3 home_refresh.py && python3 home_v3.py && python3 check.py
cd ../export && python3 export.py ../dist
```

Upload `site/dist/` to the web root (staging lives at `public_html/new/`).

Placeholder content (sample quotes, results, metrics and prices) is generated filler and must be replaced before launch.
