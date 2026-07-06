# Sample Images (hosted on Cloudflare R2)

Photos are served from the Cloudflare CDN — not stored in this Git repo.

**CDN base URL:** `https://cdn.westsummerlinhomes.com`

Override via `NEXT_PUBLIC_IMAGE_CDN_URL` in `.env` for Next.js apps.

## Image List

- **hero-bg.jpg** - Luxury homes in West Summerlin, Las Vegas (1920x1080)
- **property-1.jpg** - Luxury Mediterranean Villa (800x600)
- **property-2.jpg** - Modern Contemporary Home (800x600)
- **property-3.jpg** - Elegant Spanish Revival (800x600)
- **testimonial-1.jpg** - Sarah Johnson - Home Buyer (200x200)
- **testimonial-2.jpg** - Michael Chen - Home Seller (200x200)
- **testimonial-3.jpg** - Jennifer Rodriguez - Investor (200x200)
- **testimonial-4.jpg** - David Thompson - First-time Buyer (200x200)
- **dr-janet-duffy.jpg** - Agent headshot (300x300)
- **dr-janet-duffy-real-estate.jpg** - OG/social share image (1200x630)
- **logo.png** - Site logo
- **og-image.jpg** - Open Graph fallback

## Cloudflare R2 folder structure

```
/images/hero-bg.jpg
/images/property-{1,2,3}.jpg
/images/testimonial-{1-4}.jpg
/images/dr-janet-duffy.jpg
/images/dr-janet-duffy-real-estate.jpg
/images/logo.png
/images/og-image.jpg
/properties/{mls#}-main.jpg
```

## Usage

These images are referenced via `src/lib/images.ts` (Next.js) and `image-cdn.js` (static HTML).
