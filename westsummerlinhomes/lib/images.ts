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

export function propertyImage(mlsNumber: string): string {
  return cdnImage(`/properties/${mlsNumber.toLowerCase()}-main.jpg`)
}
