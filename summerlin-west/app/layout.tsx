import type { Metadata } from 'next'
import './styles.css'

import Script from "next/script";
export const metadata: Metadata = {
  title: 'Summerlin West Homes - Daily Tracker | True Cost After Incentives',
  description: 'Track 15 new construction homes in Summerlin West with builder incentives. See the real cost after incentives. Updated daily.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* RealScout Web Components */}
        <script src="https://em.realscout.com/widgets/realscout-web-components.umd.js" type="module"></script>
        <style dangerouslySetInnerHTML={{
          __html: `
            realscout-advanced-search {
              --rs-listing-divider-color: rgb(101, 141, 172);
              width: 100%;
              margin-bottom: 2rem;
            }
            
            realscout-office-listings {
              --rs-listing-divider-color: rgb(101, 141, 172);
              width: 100%;
            }
          `
        }} />
        
        {/* Critical CSS - Inline for above-the-fold performance */}
        <style dangerouslySetInnerHTML={{
          __html: `
            :root {
              --primary: #0A2540;
              --accent: #FF6B35;
              --success: #00D924;
              --urgent: #FF3366;
              --white: #FFFFFF;
              --gray-50: #FAFAFA;
              --gray-100: #F4F4F5;
              --gray-200: #E4E4E7;
              --gray-600: #52525B;
              --gray-900: #18181B;
              --space-xs: 0.5rem;
              --space-sm: 0.75rem;
              --space-md: 1rem;
              --space-lg: 1.5rem;
              --space-xl: 2rem;
              --space-2xl: 3rem;
              --space-3xl: 4rem;
            }
            * {
              margin: 0;
              padding: 0;
              box-sizing: border-box;
            }
            body {
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              color: var(--gray-900);
              background: var(--gray-50);
              line-height: 1.6;
            }
            .container {
              width: 100%;
              max-width: 1200px;
              margin: 0 auto;
              padding: 0 var(--space-md);
            }
            .hero {
              background: var(--white);
              padding: var(--space-3xl) 0 var(--space-xl);
              text-align: center;
            }
            .hero-title {
              font-size: clamp(2rem, 5vw, 3.5rem);
              font-weight: 900;
              line-height: 1.1;
              color: var(--primary);
              margin-bottom: var(--space-md);
            }
            .hero-subtitle {
              font-size: clamp(1.25rem, 3vw, 1.75rem);
              color: var(--gray-600);
              margin-bottom: var(--space-xl);
              font-weight: 400;
            }
            .hero-metrics {
              display: flex;
              justify-content: center;
              gap: var(--space-xl);
              margin-bottom: var(--space-xl);
            }
            .metric {
              text-align: center;
            }
            .metric-value {
              font-size: 2.5rem;
              font-weight: 900;
              color: var(--accent);
            }
            .metric-label {
              font-size: 0.875rem;
              color: var(--gray-600);
              text-transform: uppercase;
              letter-spacing: 0.05em;
            }
            .properties-grid {
              display: grid;
              gap: var(--space-lg);
              grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
              padding: var(--space-xl);
            }
            .property-card {
              background: var(--white);
              border: 1px solid var(--gray-200);
              border-radius: 12px;
              overflow: hidden;
              position: relative;
              cursor: pointer;
            }
            .true-cost-badge {
              position: absolute;
              top: var(--space-md);
              left: var(--space-md);
              background: var(--white);
              padding: var(--space-xs) var(--space-md);
              border-radius: 100px;
              box-shadow: 0 4px 12px rgba(0,0,0,0.08);
              z-index: 10;
            }
            .true-cost-value {
              font-size: 1.75rem;
              font-weight: 900;
              color: var(--primary);
            }
            .savings-badge {
              position: absolute;
              top: var(--space-md);
              right: var(--space-md);
              background: var(--success);
              color: var(--white);
              padding: var(--space-xs) var(--space-sm);
              border-radius: 6px;
              font-weight: 700;
              font-size: 0.875rem;
            }
            .property-image {
              aspect-ratio: 16/10;
              object-fit: cover;
              width: 100%;
            }
            .property-content {
              padding: var(--space-lg);
            }
            .property-monthly {
              font-size: 1.5rem;
              font-weight: 700;
              color: var(--primary);
              margin-bottom: var(--space-xs);
            }
            @media (max-width: 768px) {
              .properties-grid {
                grid-template-columns: 1fr;
              }
              .hero-metrics {
                flex-direction: column;
                gap: var(--space-lg);
              }
            }
          `
        }} />
        
        {/* External CSS for non-critical styles */}
        <link rel="stylesheet" href="/styles.css" />
      </head>
      <body>
        {children}
      
        {/* Follow Up Boss pixel (Widget Tracker) */}
        <Script id="fub-widget-tracker" strategy="afterInteractive">{`
(function(w,i,d,g,e,t){w["WidgetTrackerObject"]=g;(w[g]=w[g]||function()
{(w[g].q=w[g].q||[]).push(arguments);}),(w[g].ds=1*new Date());(e="script"),
(t=d.createElement(e)),(e=d.getElementsByTagName(e)[0]);t.async=1;t.src=i;
e.parentNode.insertBefore(t,e);})
(window,"https://widgetbe.com/agent",document,"widgetTracker");
window.widgetTracker("create", "WT-XQHVYQWW");
window.widgetTracker("send", "pageview");
        `}</Script>
</body>
    </html>
  )
}
