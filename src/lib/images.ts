/** Canonical image base — jsDelivr serves repo assets until Vercel /images/ is live. */
export const IMAGE_REPO_BASE =
  'https://cdn.jsdelivr.net/gh/LetMeHelpYouREALTY/westsummerlinhomes.com@main'

const IMAGE_CDN = process.env.NEXT_PUBLIC_IMAGE_CDN_URL ?? IMAGE_REPO_BASE

export function cdnImage(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${IMAGE_CDN.replace(/\/$/, '')}${normalized}`
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
