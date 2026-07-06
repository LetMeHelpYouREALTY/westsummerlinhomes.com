import type { Metadata } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
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

export const metadata: Metadata = {
  title: {
    default: 'West Summerlin Homes | Luxury Real Estate in Summerlin, Las Vegas',
    template: '%s | West Summerlin Homes'
  },
  description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
  keywords: ['Summerlin homes', 'Las Vegas real estate', 'luxury homes', 'West Summerlin', 'real estate agent', 'Summerlin properties'],
  authors: [{ name: 'West Summerlin Homes' }],
  creator: 'West Summerlin Homes',
  publisher: 'West Summerlin Homes',
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
    title: 'West Summerlin Homes | Luxury Real Estate in Summerlin, Las Vegas',
    description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
    url: 'https://westsummerlinhomes.com',
    siteName: 'West Summerlin Homes',
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: siteImages.og,
        width: 1200,
        height: 630,
        alt: 'West Summerlin Homes - Luxury Real Estate',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'West Summerlin Homes | Luxury Real Estate in Summerlin, Las Vegas',
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
      <body className={`${inter.className} antialiased bg-white text-neutral-900`}>
        {children}
      </body>
    </html>
  )
}
