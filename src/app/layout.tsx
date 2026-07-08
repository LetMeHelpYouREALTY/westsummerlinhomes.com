import type { Metadata } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
import Script from 'next/script'
import './globals.css'
import { siteImages } from '@/lib/images'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const playfair = Playfair_Display({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-playfair',
})

const SITE_NAME = 'West Summerlin Homes by Dr. Jan Duffy'

export const metadata: Metadata = {
  title: {
    default: `${SITE_NAME} | Las Vegas & Summerlin Real Estate`,
    template: `%s | ${SITE_NAME}`
  },
  description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
  keywords: ['Summerlin homes', 'Las Vegas real estate', 'luxury homes', 'West Summerlin', 'real estate agent', 'Summerlin properties'],
  authors: [{ name: SITE_NAME }],
  creator: SITE_NAME,
  publisher: SITE_NAME,
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://westsummerlinhomes.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: `${SITE_NAME} | Las Vegas & Summerlin Real Estate`,
    description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
    url: 'https://westsummerlinhomes.com',
    siteName: SITE_NAME,
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: siteImages.og,
        width: 1200,
        height: 630,
        alt: `${SITE_NAME} - Luxury Real Estate`,
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: `${SITE_NAME} | Las Vegas & Summerlin Real Estate`,
    description: 'Discover luxury homes for sale in West Summerlin, Las Vegas.',
    images: [siteImages.og],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <head>
        <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet" />
        <style
          dangerouslySetInnerHTML={{
            __html: `
              realscout-office-listings {
                --rs-listing-divider-color: rgb(101, 141, 172);
                width: 100%;
              }
            `,
          }}
        />
      </head>
      <body className={`${inter.className} antialiased bg-white text-neutral-900`}>
        <Script
          src="https://em.realscout.com/widgets/realscout-web-components.umd.js"
          type="module"
          strategy="afterInteractive"
        />
        {children}
      </body>
    </html>
  )
}
