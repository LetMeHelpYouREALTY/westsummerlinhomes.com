# West Summerlin Homes

Marketing site for **https://www.westsummerlinhomes.com**. Dr. Jan Duffy, Berkshire Hathaway HomeServices Nevada Properties (license S.0197614.LLC).

## How the live site works

The production site is **static HTML at the repo root**, served as-is by Vercel:

- `vercel.json` sets `buildCommand: ""` and `outputDirectory: "."`, so nothing is compiled. Each `*.html` file is a page.
- Clean URLs (`/about`, `/buyers`, …) are permanent redirects to the `.html` files, defined in `vercel.json`.
- The apex domain redirects to `www`.
- Shared assets: `site.css`, `header.css`, `site.js`, `header.js`, `calendly.js`, `realscout-loader.js`, `image-cdn.js`, `fonts/`, `images/`, `properties/`.
- `api/leads/submit.js` is the lead endpoint (Vercel serverless function, posts to Follow Up Boss).
- `sitemap.xml` and `robots.txt` are hand-maintained; update the sitemap when adding a page.

> **Note:** `src/`, `next.config.ts`, `tailwind.config.ts` and the `summerlin-west/` and `westsummerlinhomes/` folders are Next.js projects that are **not deployed** with the current `vercel.json`. Changes there do not affect the live site.

## Editing pages

1. Edit or add an `*.html` file at the root.
2. For a new page, add a redirect in `vercel.json` (`/slug` → `/slug.html`) and an entry in `sitemap.xml`.
3. Helper scripts in `scripts/` apply the shared header/footer and SEO templates across pages:
   - `normalize-pages.py`, `apply-site-design.py`, `build-seo-pages.py`

Preview locally with any static server, e.g. `npx serve .`, or `vercel dev` for redirects and the API route.

## Environment variables

Set in the Vercel project dashboard, never committed. See `.env.example`:

| Variable | Used for |
|---|---|
| `FUB_API_KEY` | Follow Up Boss lead submission (`api/leads/submit.js`). **The only variable the live site reads.** |
| `GSC_VERIFICATION` | Listed in `.env.example`, but not read by the static site (there is no build step to inject it). To verify Search Console, add the `google-site-verification` meta tag to `index.html` by hand. |
| `NEXT_PUBLIC_IMAGE_CDN_URL` | Only used by the undeployed Next.js code. The static site's CDN origin is set in `image-cdn.js` (default `https://cdn.westsummerlinhomes.com`, overridable with `window.IMAGE_CDN`). |

## Lead capture

RealScout is the primary lead path and Calendly is secondary. Avoid adding new generic lead forms.

## License

See `LICENSE`.
