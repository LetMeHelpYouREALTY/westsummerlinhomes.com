'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Star, Quote, ChevronLeft, ChevronRight } from 'lucide-react'
import { siteImages } from '@/lib/images'

interface Testimonial {
  id: string
  name: string
  role: string
  image: string
  rating: number
  content: string
  property: string
  date: string
}

const testimonials: Testimonial[] = [
  {
    id: '1',
    name: 'Sarah Johnson',
    role: 'Home Buyer',
    image: siteImages.testimonial(1),
    rating: 5,
    content: 'Working with West Summerlin Homes was an absolute pleasure. They found us the perfect home in Red Rock Country Club within our budget and timeline. Their knowledge of the area and attention to detail made the entire process seamless.',
    property: 'Red Rock Country Club Villa',
    date: 'December 2024'
  },
  {
    id: '2',
    name: 'Michael Chen',
    role: 'Home Seller',
    image: siteImages.testimonial(2),
    rating: 5,
    content: 'I was amazed at how quickly they sold my home above asking price. Their marketing strategy and professional photography showcased my property perfectly. The entire team was responsive and kept me informed every step of the way.',
    property: 'Summerlin West Contemporary',
    date: 'November 2024'
  },
  {
    id: '3',
    name: 'Jennifer Rodriguez',
    role: 'Investor',
    image: siteImages.testimonial(3),
    rating: 5,
    content: 'As a real estate investor, I appreciate working with agents who understand market trends and investment potential. West Summerlin Homes provided invaluable insights that helped me make informed decisions and maximize my returns.',
    property: 'The Ridges Luxury Estate',
    date: 'October 2024'
  },
  {
    id: '4',
    name: 'David Thompson',
    role: 'First-time Buyer',
    image: siteImages.testimonial(4),
    rating: 5,
    content: 'Being a first-time homebuyer, I had many questions and concerns. The team at West Summerlin Homes patiently guided me through every step, explaining the process clearly and ensuring I felt confident in my decision.',
    property: 'Summerlin Starter Home',
    date: 'September 2024'
  }
]

export default function Testimonials() {
  const [currentIndex, setCurrentIndex] = useState(0)

  const nextTestimonial = () => {
    setCurrentIndex((prev) => (prev + 1) % testimonials.length)
  }

  const prevTestimonial = () => {
    setCurrentIndex((prev) => (prev - 1 + testimonials.length) % testimonials.length)
  }

  const goToTestimonial = (index: number) => {
    setCurrentIndex(index)
  }

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-5 h-5 ${
          i < rating ? 'text-yellow-400 fill-current' : 'text-neutral-300'
        }`}
      />
    ))
  }

  return (
    <section className="section-padding bg-neutral-50">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold mb-6">
            What Our Clients Say
          </h2>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Don't just take our word for it. Here's what our satisfied clients have to say about 
            their experience working with West Summerlin Homes by Dr. Jan Duffy.
          </p>
        </div>

        {/* Featured Testimonial */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="card relative">
            <Quote className="absolute top-8 right-8 w-16 h-16 text-primary-200" />
            
            <div className="flex flex-col lg:flex-row items-center lg:items-start gap-8">
              <div className="flex-shrink-0">
                <div className="relative w-24 h-24 rounded-full overflow-hidden">
                  <Image
                    src={testimonials[currentIndex].image}
                    alt={testimonials[currentIndex].name}
                    fill
                    className="object-cover"
                  />
                </div>
              </div>
              
              <div className="flex-1 text-center lg:text-left">
                <div className="flex justify-center lg:justify-start mb-4">
                  {renderStars(testimonials[currentIndex].rating)}
                </div>
                
                <blockquote className="text-xl text-neutral-700 mb-6 leading-relaxed">
                  "{testimonials[currentIndex].content}"
                </blockquote>
                
                <div className="mb-4">
                  <div className="font-bold text-lg text-neutral-900">
                    {testimonials[currentIndex].name}
                  </div>
                  <div className="text-neutral-600">
                    {testimonials[currentIndex].role}
                  </div>
                </div>
                
                <div className="text-sm text-neutral-500">
                  Purchased: {testimonials[currentIndex].property}
                </div>
                <div className="text-sm text-neutral-500">
                  {testimonials[currentIndex].date}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Controls */}
        <div className="flex justify-center items-center gap-4 mb-12">
          <button
            onClick={prevTestimonial}
            className="p-3 rounded-full bg-white border border-neutral-200 hover:bg-neutral-50 transition-colors duration-200"
            aria-label="Previous testimonial"
          >
            <ChevronLeft className="w-5 h-5 text-neutral-600" />
          </button>
          
          <div className="flex gap-2">
            {testimonials.map((_, index) => (
              <button
                key={index}
                onClick={() => goToTestimonial(index)}
                className={`w-3 h-3 rounded-full transition-all duration-200 ${
                  index === currentIndex
                    ? 'bg-primary-600 scale-125'
                    : 'bg-neutral-300 hover:bg-neutral-400'
                }`}
                aria-label={`Go to testimonial ${index + 1}`}
              />
            ))}
          </div>
          
          <button
            onClick={nextTestimonial}
            className="p-3 rounded-full bg-white border border-neutral-200 hover:bg-neutral-50 transition-colors duration-200"
            aria-label="Next testimonial"
          >
            <ChevronRight className="w-5 h-5 text-neutral-600" />
          </button>
        </div>

        {/* All Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {testimonials.map((testimonial) => (
            <div key={testimonial.id} className="card">
              <div className="flex items-start gap-4 mb-4">
                <div className="relative w-16 h-16 rounded-full overflow-hidden flex-shrink-0">
                  <Image
                    src={testimonial.image}
                    alt={testimonial.name}
                    fill
                    className="object-cover"
                  />
                </div>
                
                <div className="flex-1">
                  <div className="flex mb-2">
                    {renderStars(testimonial.rating)}
                  </div>
                  <div className="font-bold text-neutral-900">
                    {testimonial.name}
                  </div>
                  <div className="text-sm text-neutral-600">
                    {testimonial.role}
                  </div>
                </div>
              </div>
              
              <blockquote className="text-neutral-700 mb-4 leading-relaxed">
                "{testimonial.content}"
              </blockquote>
              
              <div className="text-sm text-neutral-500">
                <div>Property: {testimonial.property}</div>
                <div>Date: {testimonial.date}</div>
              </div>
            </div>
          ))}
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16">
          <div className="bg-white rounded-3xl p-12 shadow-lg border border-neutral-200">
            <h3 className="text-2xl font-bold text-neutral-900 mb-4">
              Ready to Experience the Difference?
            </h3>
            <p className="text-lg text-neutral-600 mb-8 max-w-2xl mx-auto">
              Join hundreds of satisfied clients who have found their dream homes with West Summerlin Homes by Dr. Jan Duffy.
              Let us help you navigate the real estate market with confidence.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="btn-primary px-8 py-4">
                Schedule a Consultation
              </button>
              <button className="btn-secondary px-8 py-4">
                View Our Reviews
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
