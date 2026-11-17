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
| `FUB_API_KEY` | Follow Up Boss lead submission (`api/leads/submit.js`) |
| `GSC_VERIFICATION` | Google Search Console verification |
| `NEXT_PUBLIC_IMAGE_CDN_URL` | Image CDN origin |

## Lead capture

RealScout is the primary lead path and Calendly is secondary. Avoid adding new generic lead forms.

## License

See `LICENSE`.
