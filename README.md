# Mecury — A parallel life

Mecury's homepage introduces Zhi Luo, his scientific background, the origin of Mecury, and the story of Vibeit. Timenu and Server Sentinel remain secondary product links.

## Publishing

GitHub Pages publishes the root of `main` to https://www.mecury.co.uk/ . Preserve `CNAME`, `.nojekyll`, the ownership-verification files, and existing product routes when updating the homepage.

## Local preview

```sh
python3 -m http.server 8740 --bind 127.0.0.1
```

Open `http://127.0.0.1:8740/` for English or `/zh-hans/` for Simplified Chinese.

## Editing

- `content/home.json`: complete homepage text for 11 languages.
- `scripts/build_homepage.py`: static-page generator using Python's standard library.
- `home.css`, `home.js`: visual styling and language-menu keyboard behavior.
- `assets/home/`: original portraits, existing product images, bundled fonts and licenses.

After editing the copy, regenerate the pages:

```sh
python3 scripts/build_homepage.py
```

English lives at `/`. Other locales are `/fr/`, `/de/`, `/th/`, `/ja/`, `/ko/`, `/zh-hans/`, `/zh-hant/`, `/es/`, `/ar/`, and `/it/`.

Each page includes its own canonical URL, all language alternates, localized metadata and structured data. Arabic uses right-to-left layout with isolated Latin brand names. Content and the native language selector work without JavaScript; JavaScript adds Escape and outside-click dismissal.

The root sitemap index includes the homepage sitemap and the Vibeit sitemap. The homepage sitemap retains the privacy page and all three product entry points. The privacy page continues to use its original stylesheet.

## Validation

The selected design was checked in the in-app browser at desktop and phone widths across all 11 languages, with additional narrow-screen checks for German, Japanese, Thai and Arabic. Language switching, keyboard dismissal, story navigation, local assets, canonical/hreflang targets, JSON-LD and sitemap XML were verified. Original portrait and product-image files are preserved.
