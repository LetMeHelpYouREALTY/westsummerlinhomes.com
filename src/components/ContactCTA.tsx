'use client'

import { useState } from 'react'
import { Phone, Mail, MapPin, Clock, MessageCircle, Send } from 'lucide-react'

interface ContactForm {
  name: string
  email: string
  phone: string
  message: string
  propertyInterest: string
  timeline: string
}

export default function ContactCTA() {
  const [formData, setFormData] = useState<ContactForm>({
    name: '',
    email: '',
    phone: '',
    message: '',
    propertyInterest: '',
    timeline: ''
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setIsSubmitting(false)
    setSubmitSuccess(true)
    
    // Reset form after success
    setTimeout(() => {
      setSubmitSuccess(false)
      setFormData({
        name: '',
        email: '',
        phone: '',
        message: '',
        propertyInterest: '',
        timeline: ''
      })
    }, 5000)
  }

  const contactInfo = [
    {
      icon: Phone,
      title: 'Call Us',
      details: ['702-222-1964'],
      action: 'Call Now'
    },
    {
      icon: Mail,
      title: 'Email Us',
      details: ['janet@westsummerlinhomes.com'],
      action: 'Send Email'
    },
    {
      icon: MapPin,
      title: 'Visit Our Office',
      details: ['1234 Summerlin Pkwy', 'Las Vegas, NV 89134'],
      action: 'Get Directions'
    },
    {
      icon: Clock,
      title: 'Office Hours',
      details: ['Available 7 days a week', '8:00 AM - 8:00 PM'],
      action: 'Schedule Meeting'
    }
  ]

  return (
    <section className="section-padding bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 text-white">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold mb-6">
            Ready to Find Your Dream Home?
          </h2>
          <p className="text-xl text-primary-100 max-w-3xl mx-auto">
            Let's start your journey to finding the perfect home in West Summerlin. 
            Our expert team is here to guide you every step of the way.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          {/* Contact Form */}
          <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20">
            <h3 className="text-2xl font-bold mb-6">Send Us a Message</h3>
            
            {submitSuccess ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Send className="w-8 h-8 text-white" />
                </div>
                <h4 className="text-xl font-bold text-green-400 mb-2">Message Sent!</h4>
                <p className="text-primary-100">
                  Thank you for reaching out. We'll get back to you within 24 hours.
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-primary-100 mb-2">
                      Full Name *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200"
                      placeholder="Enter your full name"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-primary-100 mb-2">
                      Email Address *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200"
                      placeholder="Enter your email"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-primary-100 mb-2">
                      Phone Number
                    </label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200"
                      placeholder="Enter your phone number"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="timeline" className="block text-sm font-medium text-primary-100 mb-2">
                      Timeline
                    </label>
                    <select
                      id="timeline"
                      name="timeline"
                      value={formData.timeline}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200"
                    >
                      <option value="">Select timeline</option>
                      <option value="immediate">Immediate (0-3 months)</option>
                      <option value="soon">Soon (3-6 months)</option>
                      <option value="planning">Planning (6-12 months)</option>
                      <option value="future">Future (12+ months)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label htmlFor="propertyInterest" className="block text-sm font-medium text-primary-100 mb-2">
                    Property Interest
                  </label>
                  <select
                    id="propertyInterest"
                    name="propertyInterest"
                    value={formData.propertyInterest}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200"
                  >
                    <option value="">Select property type</option>
                    <option value="buying">Buying a Home</option>
                    <option value="selling">Selling a Home</option>
                    <option value="investing">Real Estate Investment</option>
                    <option value="renting">Rental Property</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-primary-100 mb-2">
                    Message *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleInputChange}
                    required
                    rows={4}
                    className="w-full px-4 py-3 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200 resize-none"
                    placeholder="Tell us about your real estate needs..."
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full btn-secondary text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Sending Message...
                    </div>
                  ) : (
                    <>
                      <MessageCircle className="w-5 h-5 inline-block mr-2" />
                      Send Message
                    </>
                  )}
                </button>
              </form>
            )}
          </div>

          {/* Contact Information */}
          <div className="space-y-8">
            <div>
              <h3 className="text-2xl font-bold mb-6">Get in Touch</h3>
              <p className="text-lg text-primary-100 leading-relaxed">
                Whether you're buying, selling, or investing in West Summerlin real estate, 
                our experienced team is here to help. Reach out today for personalized service 
                and expert guidance.
              </p>
            </div>

            <div className="space-y-6">
              {contactInfo.map((item, index) => (
                <div key={index} className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center">
                    <item.icon className="w-6 h-6 text-white" />
                  </div>
                  
                  <div className="flex-1">
                    <h4 className="font-semibold text-lg mb-2">{item.title}</h4>
                    <div className="space-y-1 mb-3">
                      {item.details.map((detail, detailIndex) => (
                        <p key={detailIndex} className="text-primary-100">
                          {detail}
                        </p>
                      ))}
                    </div>
                    <button className="text-primary-200 hover:text-white font-medium transition-colors duration-200">
                      {item.action}
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Quick Stats */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <h4 className="font-semibold text-lg mb-4">Why Choose Us?</h4>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-primary-200">500+</div>
                  <div className="text-sm text-primary-100">Happy Clients</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary-200">15+</div>
                  <div className="text-sm text-primary-100">Years Experience</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary-200">98%</div>
                  <div className="text-sm text-primary-100">Client Satisfaction</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary-200">24h</div>
                  <div className="text-sm text-primary-100">Response Time</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
