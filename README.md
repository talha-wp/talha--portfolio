# Talha Ali Portfolio

Responsive personal portfolio with Home, Services, and Work pages. Built with plain HTML, CSS, and JavaScript. Includes local THICCCBOI fonts, project images, and an 18-second MP4 portfolio reel.

## Run locally

From the repository root:

```sh
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Serve the `dist` folder as the website root; opening HTML files directly will not resolve the root-relative navigation and asset paths.

## Pages

- `/` — Home
- `/services/` — Services, process, FAQs, and video
- `/work/` — Project portfolio and video

## Editing

- `dist/index.html`: home content and shared header/footer source
- `dist/styles.css`: original black/lime theme and typography
- `dist/pages.css`: Services and Work page layouts
- `dist/script.js`: mobile navigation, service selection, and email draft form
- `dist/assets/`: fonts, images, and the finished MP4 reel
- `scripts/build-pages.py`: regenerate the Services and Work pages from shared home sections and the script content
- `scripts/build-showreel.py`: optional video regeneration using FFmpeg and a supplied THICCCBOI Bold TTF font

To regenerate the inner pages after editing the source template:

```sh
python3 scripts/build-pages.py
```

The finished website requires no build step, package installation, backend, or API keys. Publish the contents of `dist` with a static host that serves directory `index.html` files. The contact form opens a draft in the visitor’s email application; it does not submit messages to a server.

## Design

The black/lime palette and THICCCBOI typography are preserved across all pages. Portfolio layouts draw on the supplied Shahid Ali and Webyansh references. Personal and project imagery comes from the portfolio’s supplied sources; asset and font rights remain with their respective owners.
