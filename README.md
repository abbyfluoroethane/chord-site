# chord-site

The website and docs for Chord, a chat client for XMPP.

- Homepage: `src/pages/index.astro`
- Docs: `src/content/docs/docs/` (Markdown, rendered by [Starlight](https://starlight.astro.build))
- Live site: https://abbyfluoroethane.github.io/chord-site/

## Run it locally

1. Install Node.js 22.12 or later.
2. Run `npm install`.
3. Run `npm run dev`.
4. Open http://localhost:4321/chord-site/ in a browser.

## Deploy

A push to `main` starts `.github/workflows/deploy.yml`. The workflow builds the site and publishes it to GitHub Pages.

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

## Links and the base path

The site lives under `/chord-site/`, so a hard-coded link such as `/docs/` breaks. Use the `url()` helper from `src/lib/url.ts`:

```astro
<a href={url('docs/self-host/')}>Self-host</a>
```

If the site moves to a custom domain, remove `base` from `astro.config.mjs`.

## Open items

- The app mock in `src/components/AppMock.astro` is a drawing. Replace it with a screenshot when the client exists.
- The Download and Open in browser buttons point at the getting-started page. Point them at the release page and the web client when those exist.
- The docs pages have `[TODO]` markers where facts are not known yet.
- Pick a license.
