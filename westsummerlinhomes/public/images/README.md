# Image assets

Site images live in this folder and are served at `/images/*`.

## Files

| File | Use |
|------|-----|
| `hero-bg.jpg` | Hero background (all pages) |
| `property-1.jpg` … `property-3.jpg` | Featured property cards |
| `testimonial-1.jpg` … `testimonial-4.jpg` | Client testimonials |
| `dr-janet-duffy.jpg` | Agent headshot |
| `dr-janet-duffy-real-estate.jpg` | OG / social share image |
| `og-image.jpg` | Next.js Open Graph fallback |
| `logo.png` | Site logo / schema |

MLS listing photos are in `/public/properties/` (`mls001-main.jpg` … `mls015-main.jpg`).

## Cloudflare R2 (optional)

Images work locally from `/public` by default. To serve from Cloudflare instead, set:

```
NEXT_PUBLIC_IMAGE_CDN_URL=https://cdn.westsummerlinhomes.com
```

Upload this folder’s contents to your R2 bucket under `/images/`, and `/public/properties/` under `/properties/`.
