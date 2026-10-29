'use client'

import { useEffect } from 'react'

// Follow Up Boss Widget Tracker (WT-XQHVYQWW). Loads after the page is idle,
// without an inline script, so it works under the site's CSP.
export default function WidgetTracker() {
  useEffect(() => {
    const w = window as unknown as Record<string, unknown> & {
      widgetTracker?: ((...args: unknown[]) => void) & { q?: unknown[]; ds?: number }
    }
    if (document.getElementById('widget-tracker-src')) return

    const load = () => {
      if (document.getElementById('widget-tracker-src')) return
      w.WidgetTrackerObject = 'widgetTracker'
      if (!w.widgetTracker) {
        const fn = ((...args: unknown[]) => {
          ;(fn.q = fn.q || []).push(args)
        }) as ((...args: unknown[]) => void) & { q?: unknown[]; ds?: number }
        w.widgetTracker = fn
      }
      w.widgetTracker.ds = Date.now()
      const s = document.createElement('script')
      s.id = 'widget-tracker-src'
      s.async = true
      s.src = 'https://widgetbe.com/agent'
      document.head.appendChild(s)
      w.widgetTracker('create', 'WT-XQHVYQWW')
      w.widgetTracker('send', 'pageview')
    }

    const idle = (window as Window & { requestIdleCallback?: (cb: () => void, o?: { timeout: number }) => number })
      .requestIdleCallback
    const t = window.setTimeout(() => (idle ? idle(load, { timeout: 3000 }) : load()), 2500)
    return () => window.clearTimeout(t)
  }, [])

  return null
}
