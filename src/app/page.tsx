import type { Metadata } from 'next'
import { Suspense } from 'react'
import HeroSection from '@/components/HeroSection'
import FeaturedProperties from '@/components/FeaturedProperties'
import MarketInsights from '@/components/MarketInsights'
import Testimonials from '@/components/Testimonials'
import ContactCTA from '@/components/ContactCTA'
import Loading from '@/components/Loading'

const SITE_NAME = 'West Summerlin Homes by Dr. Jan Duffy'

export const metadata: Metadata = {
  title: `${SITE_NAME} | Las Vegas & Summerlin Real Estate`,
  description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
  keywords: ['Summerlin homes', 'Las Vegas real estate', 'luxury homes', 'West Summerlin', 'real estate agent', 'Summerlin properties'],
  openGraph: {
    title: `${SITE_NAME} | Las Vegas & Summerlin Real Estate`,
    description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
    url: 'https://westsummerlinhomes.com',
    siteName: SITE_NAME,
    locale: 'en_US',
    type: 'website',
  },
}

export default function HomePage() {
  return (
    <main className="min-h-screen">
      {/* Structured Data for Real Estate */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "RealEstateAgent",
            "name": "West Summerlin Homes by Dr. Jan Duffy",
            "description": "Luxury real estate services in West Summerlin, Las Vegas",
            "url": "https://westsummerlinhomes.com",
            "telephone": "+1-702-XXX-XXXX",
            "address": {
              "@type": "PostalAddress",
              "addressLocality": "Summerlin",
              "addressRegion": "NV",
              "addressCountry": "US"
            },
            "areaServed": {
              "@type": "City",
              "name": "Summerlin",
              "containedInPlace": {
                "@type": "City",
                "name": "Las Vegas"
              }
            },
            "serviceType": "Real Estate Services",
            "priceRange": "$$$"
          })
        }}
      />

      <Suspense fallback={<Loading />}>
        <HeroSection />
      </Suspense>

      <Suspense fallback={<Loading />}>
        <FeaturedProperties />
      </Suspense>

      <Suspense fallback={<Loading />}>
        <MarketInsights />
      </Suspense>

      <Suspense fallback={<Loading />}>
        <Testimonials />
      </Suspense>

      <Suspense fallback={<Loading />}>
        <ContactCTA />
      </Suspense>
    </main>
  )
}
