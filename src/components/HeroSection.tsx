'use client'

import Image from 'next/image'
import { useState } from 'react'
import { Search, MapPin, Home, DollarSign } from 'lucide-react'
import { siteImages } from '@/lib/images'

export default function HeroSection() {
  const [searchQuery, setSearchQuery] = useState('')
  const [propertyType, setPropertyType] = useState('all')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle search logic here
    console.log('Search:', { searchQuery, propertyType })
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image
          src={siteImages.hero}
          alt="Luxury homes in West Summerlin, Las Vegas"
          fill
          priority
          className="object-cover"
          sizes="100vw"
          quality={90}
        />
        <div className="absolute inset-0 bg-gradient-to-r from-primary-900/80 to-primary-600/60" />
      </div>

      {/* Content */}
      <div className="relative z-10 container text-center text-white">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-display font-bold mb-6 leading-tight">
            Discover Your Dream Home in
            <span className="text-gradient block">West Summerlin</span>
          </h1>
          
          <p className="text-xl md:text-2xl mb-8 text-neutral-100 max-w-3xl mx-auto leading-relaxed">
            Experience luxury living in one of Las Vegas' most prestigious communities. 
            Find your perfect home with expert guidance and personalized service.
          </p>

          {/* Search Form */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
            <div className="flex flex-col sm:flex-row gap-4 p-2 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
              <div className="flex-1 relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Enter address, neighborhood, or zip code"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-4 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200"
                />
              </div>
              
              <select
                value={propertyType}
                onChange={(e) => setPropertyType(e.target.value)}
                aria-label="Select property type"
                className="px-4 py-4 bg-white/90 text-neutral-900 rounded-xl border-0 focus:ring-2 focus:ring-primary-400 focus:outline-none transition-all duration-200 min-w-[140px]"
              >
                <option value="all">All Types</option>
                <option value="single-family">Single Family</option>
                <option value="condo">Condo</option>
                <option value="townhouse">Townhouse</option>
                <option value="luxury">Luxury</option>
              </select>
              
              <button
                type="submit"
                className="btn-primary px-8 py-4 text-lg font-semibold"
              >
                <Search className="w-5 h-5 inline-block mr-2" />
                Search
              </button>
            </div>
          </form>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                <Home className="w-8 h-8 mx-auto mb-3 text-primary-300" />
                <div className="text-3xl font-bold mb-1">500+</div>
                <div className="text-neutral-200">Properties Sold</div>
              </div>
            </div>
            
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                <DollarSign className="w-8 h-8 mx-auto mb-3 text-primary-300" />
                <div className="text-3xl font-bold mb-1">$2.5M+</div>
                <div className="text-neutral-200">Total Sales Volume</div>
              </div>
            </div>
            
            <div className="text-center">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                <div className="w-8 h-8 mx-auto mb-3 text-primary-300 text-2xl font-bold">⭐</div>
                <div className="text-3xl font-bold mb-1">4.9</div>
                <div className="text-neutral-200">Client Rating</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10">
        <div className="animate-bounce">
          <div className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center">
            <div className="w-1 h-3 bg-white/70 rounded-full mt-2 animate-pulse" />
          </div>
        </div>
      </div>
    </section>
  )
}
