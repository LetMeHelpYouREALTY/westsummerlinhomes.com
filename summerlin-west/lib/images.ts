/** Canonical image base — Cloudflare R2 CDN (fallback: jsDelivr from GitHub). */
export const IMAGE_CLOUDFLARE_CDN = 'https://cdn.westsummerlinhomes.com'
export const IMAGE_REPO_BASE =
  'https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main'

const IMAGE_CDN = process.env.NEXT_PUBLIC_IMAGE_CDN_URL ?? IMAGE_CLOUDFLARE_CDN

export function cdnImage(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${IMAGE_CDN.replace(/\/$/, '')}${normalized}`
}

export function propertyImage(mlsNumber: string): string {
  return cdnImage(`/properties/${mlsNumber.toLowerCase()}-main.jpg`)
}
