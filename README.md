# chord-site

The website and docs for Chord, a chat client for XMPP.

- Homepage: `src/pages/index.astro`
- Docs: `src/content/docs/docs/` (Markdown, rendered by [Starlight](https://starlight.astro.build))
- Live site: https://bigaouette.com/chord-site/

## Run it locally

1. Install Node.js 22.12 or later.
2. Run `npm install`.
3. Run `npm run dev`.
4. Open http://localhost:4321/chord-site/ in a browser.

## Deploy

A push to `main` starts `.github/workflows/astro.yml`. The workflow builds the site and publishes it to GitHub Pages.

Before the first deploy, turn on Pages once:

1. Open **Settings > Pages** in this repo.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.

## Styles

| File | Scope |
| --- | --- |
| `src/styles/chord.css` | Tokens and shared classes for every page. |
| `src/styles/home.css` | Homepage-only styles: the hero, the app mock, the federation diagram. |
| `src/styles/starlight.css` | Maps the Chord tokens onto the docs theme. |

The tokens come from the Chord design system. Change a color in the `:root` block of `chord.css`, not in markup. Add `data-theme="light"` to an element to show the light theme.

## Logo files

`public/brand/` holds the logo pack: SVG and PNG for each setup, plus `chord-brand.zip`. The style guide page links to them.

To rebuild the pack after a logo or color change:

1. Get the Bricolage Grotesque 700 font as a `.woff` file (for example from the `@fontsource/bricolage-grotesque` package).
2. Run `python3 scripts/build-logos.py path/to/bricolage-grotesque-latin-700-normal.woff`.

The script needs Python with `fonttools` and `playwright`. It turns the wordmark into outlines, so the SVGs do not need the font.

## Links and the base path

The site lives under `/chord-site/`, so a hard-coded link such as `/docs/` breaks. Use the `url()` helper from `src/lib/url.ts`:

```astro
<a href={url('docs/self-host/')}>Self-host</a>
```

If the site moves to its own domain (for example chord.example), remove `base` from `astro.config.mjs` and change `site`.

## Open items

- The app mock in `src/components/AppMock.astro` is a drawing. Replace it with a screenshot when the client exists.
- The Download and Open in browser buttons point at the getting-started page. Point them at the release page and the web client when those exist.
- The docs pages have `[TODO]` markers where facts are not known yet.
- Pick a license.
