/** Canonical image base — jsDelivr serves repo assets until Vercel /images/ is live. */
export const IMAGE_REPO_BASE =
  'https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main'

const IMAGE_CDN = process.env.NEXT_PUBLIC_IMAGE_CDN_URL ?? IMAGE_REPO_BASE

export function cdnImage(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${IMAGE_CDN.replace(/\/$/, '')}${normalized}`
}

export function propertyImage(mlsNumber: string): string {
  return cdnImage(`/properties/${mlsNumber.toLowerCase()}-main.jpg`)
}
