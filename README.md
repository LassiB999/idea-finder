# Idea Finder

**Spot the need before anyone else.** Seed a niche, hunt 12 free live sources, capture what you find, and let a weighted score tell you what's actually worth building.

🔗 **Live:** https://lassib999.github.io/idea-finder/

## What it does

- **Hunt** — one seed keyword builds pre-filled searches across Reddit, Google Trends, AlsoAsked, Google Suggest, Etsy, Amazon, Pinterest, YouTube, Product Hunt, Quora, Gumroad and the App Store.
- **Angles** — 7 search angles (pain points, alternatives, jobs-to-be-done, cheap unmet demand, sellable formats…) reshape the query per source.
- **Capture & score** — log each opportunity and rate it on demand, low competition, monetization and your own passion. The board ranks them for you.
- **Export** — pull everything out as JSON whenever you want.

## Privacy

100% client-side. No account, no backend, no analytics, no cookies. Everything you save lives in your browser's `localStorage` and never leaves your device. Works offline after the first load (PWA).

## Running locally

```bash
python3 -m http.server 4321
```

Then open http://localhost:4321. A real HTTP origin is required — the service worker won't register over `file://`.

## Regenerating assets

```bash
python3 make_icon.py   # app icons → icons/
python3 make_og.py     # social share card → og-image.png
```

Both need Pillow (`pip install Pillow`).

## Stack

One `index.html` — no build step, no dependencies, no framework.

## License

MIT
