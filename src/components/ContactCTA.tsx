'use client'

import { Phone, Mail, MapPin, Clock } from 'lucide-react'
import Script from 'next/script'

const CALENDLY_URL = 'https://calendly.com/drjanduffy/in-person-real-estate-consultation'

const contactInfo = [
  {
    icon: Phone,
    title: 'Call Us',
    details: ['702-222-1964'],
    action: 'Call Now',
    href: 'tel:7022221964',
  },
  {
    icon: Mail,
    title: 'Email Us',
    details: ['janet@westsummerlinhomes.com'],
    action: 'Send Email',
    href: 'mailto:janet@westsummerlinhomes.com',
  },
  {
    icon: MapPin,
    title: 'Visit Our Office',
    details: ['12446 Weather Ridge Pl', 'Las Vegas, NV 89138'],
    action: 'Get Directions',
    href: 'https://maps.google.com/?q=12446+Weather+Ridge+Pl+Las+Vegas+NV+89138',
  },
  {
    icon: Clock,
    title: 'Office Hours',
    details: ['Available 7 days a week', '8:00 AM - 8:00 PM'],
    action: 'Schedule Meeting',
    href: '#',
    calendly: true,
  },
]

export default function ContactCTA() {
  function openCalendlyPopup(event: React.MouseEvent<HTMLAnchorElement>) {
    event.preventDefault()
    if (window.Calendly) {
      window.Calendly.initPopupWidget({ url: CALENDLY_URL })
    }
  }

  return (
    <section className="section-padding bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 text-white">
      <Script
        src="https://assets.calendly.com/assets/external/widget.js"
        strategy="lazyOnload"
        onLoad={() => {
          if (window.Calendly) {
            window.Calendly.initBadgeWidget({
              url: CALENDLY_URL,
              text: 'Schedule time with me',
              color: '#0069ff',
              textColor: '#ffffff',
              branding: false,
            })
          }
        }}
      />

      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold mb-6">
            Ready to Find Your Dream Home?
          </h2>
          <p className="text-xl text-primary-100 max-w-3xl mx-auto">
            Book an in-person real estate consultation with Dr. Janet Duffy.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20">
            <h3 className="text-2xl font-bold mb-4">Schedule a Consultation</h3>
            <p className="text-primary-100 mb-6">
              <a
                href="#"
                className="text-primary-200 hover:text-white font-medium underline"
                onClick={openCalendlyPopup}
              >
                Schedule time with me
              </a>
            </p>
            <div
              className="calendly-inline-widget rounded-2xl overflow-hidden"
              data-url={CALENDLY_URL}
              style={{ minWidth: '320px', height: '700px' }}
            />
          </div>

          <div className="space-y-8">
            <div>
              <h3 className="text-2xl font-bold mb-6">Get in Touch</h3>
              <p className="text-lg text-primary-100 leading-relaxed">
                Whether you&apos;re buying, selling, or investing in West Summerlin real estate,
                reach out today for personalized service and expert guidance.
              </p>
            </div>

            <div className="space-y-6">
              {contactInfo.map((item) => (
                <div key={item.title} className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center">
                    <item.icon className="w-6 h-6 text-white" />
                  </div>

                  <div className="flex-1">
                    <h4 className="font-semibold text-lg mb-2">{item.title}</h4>
                    <div className="space-y-1 mb-3">
                      {item.details.map((detail) => (
                        <p key={detail} className="text-primary-100">
                          {detail}
                        </p>
                      ))}
                    </div>
                    <a
                      href={item.href}
                      className="text-primary-200 hover:text-white font-medium transition-colors duration-200"
                      onClick={item.calendly ? openCalendlyPopup : undefined}
                    >
                      {item.action}
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

declare global {
  interface Window {
    Calendly?: {
      initPopupWidget: (options: { url: string }) => void
      initBadgeWidget: (options: {
        url: string
        text: string
        color: string
        textColor: string
        branding: boolean
      }) => void
    }
  }
}
