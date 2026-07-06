/**
 * Image URLs — local /public by default; Cloudflare CDN when NEXT_PUBLIC_IMAGE_CDN_URL is set.
 */
const IMAGE_CDN = process.env.NEXT_PUBLIC_IMAGE_CDN_URL

export function cdnImage(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  if (IMAGE_CDN) {
    return `${IMAGE_CDN.replace(/\/$/, '')}${normalized}`
  }
  return normalized
}

export function propertyImage(mlsNumber: string): string {
  return cdnImage(`/properties/${mlsNumber.toLowerCase()}-main.jpg`)
}
