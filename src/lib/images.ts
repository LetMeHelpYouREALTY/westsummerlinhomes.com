/**
 * Cloudflare R2 / Images CDN configuration.
 * Photos are stored on Cloudflare — set NEXT_PUBLIC_IMAGE_CDN_URL to your bucket's custom domain.
 */
const IMAGE_CDN =
  process.env.NEXT_PUBLIC_IMAGE_CDN_URL ?? 'https://cdn.westsummerlinhomes.com'

export function cdnImage(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${IMAGE_CDN}${normalized}`
}

export const siteImages = {
  hero: cdnImage('/images/hero-bg.jpg'),
  og: cdnImage('/images/og-image.jpg'),
  agent: cdnImage('/images/dr-janet-duffy.jpg'),
  agentOg: cdnImage('/images/dr-janet-duffy-real-estate.jpg'),
  logo: cdnImage('/images/logo.png'),
  property: (n: number) => cdnImage(`/images/property-${n}.jpg`),
  testimonial: (n: number) => cdnImage(`/images/testimonial-${n}.jpg`),
}

export function propertyImage(mlsNumber: string): string {
  return cdnImage(`/properties/${mlsNumber.toLowerCase()}-main.jpg`)
}
