# chord-site

The website and docs for Chord, a chat client for XMPP.

- Homepage: `src/pages/index.astro`
- Docs: `src/content/docs/docs/` (Markdown, rendered by [Starlight](https://starlight.astro.build))
- Live site: https://chordapp.foid.space/

## Run it locally

1. Install Node.js 22.12 or later.
2. Run `npm install`.
3. Run `npm run dev`.
4. Open http://localhost:4321/ in a browser.

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

The site lives at the root of its own domain, so `/docs/` works. Still use the `url()` helper from `src/lib/url.ts`, so a link keeps working if the site ever moves under a path again:

```astro
<a href={url('features/')}>Features</a>
```

## Hidden pages

For now the docs, Find a server, Self-host and the style guide are hidden. Nothing links to them and the build does not publish them.

- The docs pages in `src/content/docs/docs/` have `draft: true`. Remove that line from a page to publish it.
- The style guide is `src/pages/_style-guide.astro`. The leading underscore keeps Astro from building it. Rename it to `style-guide.astro` to bring it back.
- The nav, footer, and homepage links are removed. `git log` has them (the commit that hides the docs).
- `sidebar` in `astro.config.mjs` is empty. Restore the four docs entries when you publish them.
- The logo pack in `public/brand/` is still served, since it is a plain file.

## Domain

The site is served at https://chordapp.foid.space/. `public/CNAME` tells GitHub Pages the domain. Two things live outside this repo:

1. In **Settings > Pages**, set the custom domain to `chordapp.foid.space` and turn on **Enforce HTTPS** once the certificate is ready.
2. At the DNS host for foid.space, add a `CNAME` record for `chordapp` that points to `abbyfluoroethane.github.io`.

## Screenshots

`public/screenshots/` holds the app screenshots (WebP, dark and light of each). The `Shot` component shows them, and the Dark / Light toggle on the homepage and the features page switches between the two. In the docs the shots follow the docs theme.

The originals are PNGs in `~/Pictures/chord-internal` (desktop and android). They show the sample "friend group" data, with third-party character art for avatars and the YouTube thumbnail in the link preview. Check the rights before the site goes public.

## Open items

- The hero (`src/components/AppMock.astro`) is a drawing on purpose: it plays a fake conversation. It uses the same cast as the screenshots (konata, kagami, tsukasa, miyuki, patty). The avatars in `public/avatars/` are cropped from them, so they carry the same rights question.
- The Open in browser button points at the getting-started page. There is no web client yet.
- The docs pages have `[TODO]` markers where facts are not known yet.
