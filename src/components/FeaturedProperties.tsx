'use client'

import Image from 'next/image'
import { useState } from 'react'
import { Bed, Bath, Square, MapPin, Heart, Share2 } from 'lucide-react'
import { siteImages } from '@/lib/images'

interface Property {
  id: string
  title: string
  address: string
  price: string
  beds: number
  baths: number
  sqft: number
  image: string
  status: 'for-sale' | 'sold' | 'pending'
  featured: boolean
}

const sampleProperties: Property[] = [
  {
    id: '1',
    title: 'Luxury Mediterranean Villa',
    address: '1234 Summerlin Pkwy, Las Vegas, NV 89134',
    price: '$1,250,000',
    beds: 4,
    baths: 3.5,
    sqft: 3200,
    image: siteImages.property(1),
    status: 'for-sale',
    featured: true
  },
  {
    id: '2',
    title: 'Modern Contemporary Home',
    address: '5678 Red Rock Dr, Las Vegas, NV 89135',
    price: '$875,000',
    beds: 3,
    baths: 2.5,
    sqft: 2400,
    image: siteImages.property(2),
    status: 'for-sale',
    featured: true
  },
  {
    id: '3',
    title: 'Elegant Spanish Revival',
    address: '9012 Tropicana Ave, Las Vegas, NV 89136',
    price: '$1,450,000',
    beds: 5,
    baths: 4,
    sqft: 3800,
    image: siteImages.property(3),
    status: 'for-sale',
    featured: true
  }
]

export default function FeaturedProperties() {
  const [favorites, setFavorites] = useState<Set<string>>(new Set())

  const toggleFavorite = (propertyId: string) => {
    const newFavorites = new Set(favorites)
    if (newFavorites.has(propertyId)) {
      newFavorites.delete(propertyId)
    } else {
      newFavorites.add(propertyId)
    }
    setFavorites(newFavorites)
  }

  const shareProperty = (property: Property) => {
    if (navigator.share) {
      navigator.share({
        title: property.title,
        text: `Check out this amazing property: ${property.title}`,
        url: `https://westsummerlinhomes.com/property/${property.id}`
      })
    } else {
      // Fallback to copying to clipboard
      navigator.clipboard.writeText(`https://westsummerlinhomes.com/property/${property.id}`)
    }
  }

  return (
    <section className="section-padding bg-neutral-50">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold mb-6">
            Featured Properties
          </h2>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Discover our handpicked selection of premium homes in West Summerlin. 
            Each property offers exceptional value and lifestyle opportunities.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {sampleProperties.map((property) => (
            <article key={property.id} className="card group hover:scale-[1.02] transition-transform duration-300">
              {/* Property Image */}
              <div className="relative overflow-hidden">
                <Image
                  src={property.image}
                  alt={property.title}
                  width={400}
                  height={300}
                  className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
                
                {/* Status Badge */}
                <div className="absolute top-4 left-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    property.status === 'for-sale' 
                      ? 'bg-accent-success text-white' 
                      : property.status === 'sold'
                      ? 'bg-neutral-600 text-white'
                      : 'bg-accent-warning text-white'
                  }`}>
                    {property.status === 'for-sale' ? 'For Sale' : 
                     property.status === 'sold' ? 'Sold' : 'Pending'}
                  </span>
                </div>

                {/* Action Buttons */}
                <div className="absolute top-4 right-4 flex flex-col gap-2">
                  <button
                    onClick={() => toggleFavorite(property.id)}
                    className={`p-2 rounded-full backdrop-blur-sm transition-all duration-200 ${
                      favorites.has(property.id)
                        ? 'bg-red-500 text-white'
                        : 'bg-white/20 text-white hover:bg-white/30'
                    }`}
                    aria-label={favorites.has(property.id) ? 'Remove from favorites' : 'Add to favorites'}
                  >
                    <Heart className={`w-5 h-5 ${favorites.has(property.id) ? 'fill-current' : ''}`} />
                  </button>
                  
                  <button
                    onClick={() => shareProperty(property)}
                    className="p-2 rounded-full bg-white/20 text-white hover:bg-white/30 backdrop-blur-sm transition-all duration-200"
                    aria-label="Share property"
                  >
                    <Share2 className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Property Details */}
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2 text-neutral-900 group-hover:text-primary-600 transition-colors duration-200">
                  {property.title}
                </h3>
                
                <div className="flex items-center text-neutral-600 mb-4">
                  <MapPin className="w-4 h-4 mr-2 flex-shrink-0" />
                  <span className="text-sm">{property.address}</span>
                </div>

                <div className="text-2xl font-bold text-primary-600 mb-4">
                  {property.price}
                </div>

                <div className="flex items-center justify-between text-sm text-neutral-600">
                  <div className="flex items-center">
                    <Bed className="w-4 h-4 mr-1" />
                    <span>{property.beds} beds</span>
                  </div>
                  <div className="flex items-center">
                    <Bath className="w-4 h-4 mr-1" />
                    <span>{property.baths} baths</span>
                  </div>
                  <div className="flex items-center">
                    <Square className="w-4 h-4 mr-1" />
                    <span>{property.sqft.toLocaleString()} sqft</span>
                  </div>
                </div>

                <button className="w-full btn-primary mt-6">
                  View Details
                </button>
              </div>
            </article>
          ))}
        </div>

        <div className="text-center mt-12">
          <button className="btn-secondary text-lg px-8 py-4">
            View All Properties
          </button>
        </div>
      </div>
    </section>
  )
}
