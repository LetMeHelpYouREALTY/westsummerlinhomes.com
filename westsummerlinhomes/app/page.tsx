import { getHomes } from '../lib/homes';
import HomeCard from '../components/HomeCard';

export default async function HomePage() {
  const homes = await getHomes();
  
  return (
    <div className="max-w-7xl mx-auto p-4">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          West Summerlin Homes by Dr. Jan Duffy
        </h1>
        <p className="text-xl text-gray-600 mb-2">
          {homes.length} Homes Under True Cost
        </p>
        <p className="text-sm text-gray-500">
          Updated {new Date().toLocaleTimeString()}
        </p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label htmlFor="price-range" className="block text-sm font-medium text-gray-700 mb-2">
              Price Range
            </label>
            <select 
              id="price-range"
              name="price-range"
              aria-label="Select price range"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any Price</option>
              <option value="500-750">$500k - $750k</option>
              <option value="750-1000">$750k - $1M</option>
              <option value="1000+">$1M+</option>
            </select>
          </div>
          <div>
            <label htmlFor="beds" className="block text-sm font-medium text-gray-700 mb-2">
              Beds
            </label>
            <select 
              id="beds"
              name="beds"
              aria-label="Select number of bedrooms"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any</option>
              <option value="1">1+</option>
              <option value="2">2+</option>
              <option value="3">3+</option>
              <option value="4">4+</option>
              <option value="5">5+</option>
            </select>
          </div>
          <div>
            <label htmlFor="baths" className="block text-sm font-medium text-gray-700 mb-2">
              Baths
            </label>
            <select 
              id="baths"
              name="baths"
              aria-label="Select number of bathrooms"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any</option>
              <option value="1">1+</option>
              <option value="2">2+</option>
              <option value="3">3+</option>
              <option value="4">4+</option>
            </select>
          </div>
          <div>
            <label htmlFor="property-type" className="block text-sm font-medium text-gray-700 mb-2">
              Property Type
            </label>
            <select 
              id="property-type"
              name="property-type"
              aria-label="Select property type"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="single-family">Single Family</option>
              <option value="townhouse">Townhouse</option>
              <option value="condo">Condo</option>
            </select>
          </div>
        </div>
      </div>

      {/* Homes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {homes.map(home => (
          <HomeCard key={home.mlsNumber} {...home} />
        ))}
      </div>

      {/* Footer */}
      <div className="text-center mt-12 text-gray-500">
        <p>Data updates every 12 hours • Last refresh: {new Date().toLocaleString()}</p>
      </div>
    </div>
  );
}
