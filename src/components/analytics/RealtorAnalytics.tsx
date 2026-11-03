'use client'
// Realtor GA4 kit v1.2 (2026-11-03). Drop into app/components/ and render once in app/layout.tsx:
//   <RealtorAnalytics siteName="Skye Canyon" />
// Env vars (Vercel): NEXT_PUBLIC_GA_ID = this site's own ID (optional)
//                    NEXT_PUBLIC_GA_ROLLUP_ID = shared Las Vegas Portfolio ID (defaults to G-8CHTB4H2WB)
import Script from 'next/script'
import { useEffect } from 'react'

const SITE_ID = process.env.NEXT_PUBLIC_GA_ID
// Las Vegas Portfolio, GA4 property 562151191. Measurement IDs are public, so a default is safe.
const ROLLUP_ID = process.env.NEXT_PUBLIC_GA_ROLLUP_ID || 'G-8CHTB4H2WB'
const IDS = [ROLLUP_ID, SITE_ID].filter((id): id is string => !!id && id !== 'G-XXXXXXXXXX')

declare global {
  interface Window { gtag?: (...args: unknown[]) => void; dataLayer?: unknown[] }
}

// Shared event names across every site. Do not rename without updating GA key events.
export type LeadEvent =
  | 'generate_lead' | 'phone_click' | 'text_click' | 'email_click'
  | 'realscout_search' | 'home_value_request' | 'book_appointment'

export function trackLead(event: LeadEvent, params: Record<string, string | number> = {}) {
  window.gtag?.('event', event, params)
}

// Calls and texts are intent, not leads: count each kind once per session.
function trackOncePerSession(event: LeadEvent, params: Record<string, string | number>) {
  try {
    const key = `ga4_${event}`
    if (sessionStorage.getItem(key)) return
    sessionStorage.setItem(key, '1')
  } catch {}
  trackLead(event, params)
}

// Preview deployments and local dev must not count as real visits.
function isProductionHost() {
  const h = window.location.hostname
  return !(h === 'localhost' || h.endsWith('.vercel.app') || h.endsWith('.pages.dev'))
}

export default function RealtorAnalytics({ siteName }: { siteName: string }) {
  useEffect(() => {
    if (!IDS.length || !isProductionHost()) return
    // One delegated listener catches every tel:, sms:, mailto:, Calendly and RealScout link on the page.
    const onClick = (e: MouseEvent) => {
      const a = (e.target as HTMLElement | null)?.closest('a')
      const href = a?.getAttribute('href') ?? ''
      if (href.startsWith('tel:')) trackOncePerSession('phone_click', { link_url: href })
      else if (href.startsWith('sms:')) trackOncePerSession('text_click', { link_url: href })
      else if (href.startsWith('mailto:')) trackLead('email_click', { link_url: href })
      else if (href.includes('calendly.com')) trackLead('book_appointment', { link_url: href, method: 'link' })
      else if (href.includes('realscout.com')) trackLead('realscout_search', { link_url: href })
      else if (href.includes('homebot')) trackLead('home_value_request', { link_url: href })
      // RealScout widgets render as <realscout-*> web components, not links.
      else if ((e.target as HTMLElement | null)?.closest('[class*="realscout"], realscout-office-listings, realscout-simple-search, realscout-advanced-search, realscout-home-value'))
        trackLead('realscout_search', { method: 'widget' })
    }
    // Calendly embeds post a message when a booking completes.
    const onMessage = (e: MessageEvent) => {
      if (!e.origin.endsWith('calendly.com')) return
      if (typeof e.data === 'object' && e.data?.event === 'calendly.event_scheduled') {
        // A completed booking is a real lead, so it also feeds GA's Lead acquisition report.
        trackLead('book_appointment', { method: 'embed' })
        trackLead('generate_lead', { form_name: 'calendly', lead_type: 'appointment' })
      }
    }
    document.addEventListener('click', onClick, { capture: true })
    window.addEventListener('message', onMessage)
    return () => {
      document.removeEventListener('click', onClick, { capture: true })
      window.removeEventListener('message', onMessage)
    }
  }, [])

  if (!IDS.length) return null
  return (
    <>
      <Script src={`https://www.googletagmanager.com/gtag/js?id=${IDS[0]}`} strategy="afterInteractive" />
      <Script id="ga4-init" strategy="afterInteractive">{`
        var h = location.hostname;
        if (h === 'localhost' || /\.vercel\.app$|\.pages\.dev$/.test(h)) { ${IDS.map((id) => `window['ga-disable-${id}'] = true;`).join(' ')} }
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        window.gtag = gtag;
        gtag('js', new Date());
        ${IDS.map((id) => `gtag('config', '${id}', { site_name: ${JSON.stringify(siteName)} });`).join('\n')}
      `}</Script>
    </>
  )
}
