import 'server-only';
import { propertyImage } from './images';

// Sample home data - in production, this would come from your MLS API or database
const sampleHomes = [
  {
    mlsNumber: 'MLS001',
    address: '123 Summerlin West Dr',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 875000,
    beds: 4,
    baths: 3.5,
    sqft: 2850,
    yearBuilt: 2020,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Beautiful Mediterranean-style home in the heart of West Summerlin',
    features: ['Pool', 'Gourmet Kitchen', 'Master Suite', '2-Car Garage'],
    lastUpdated: new Date('2024-01-15T10:30:00Z')
  },
  {
    mlsNumber: 'MLS002',
    address: '456 Red Rock Canyon Blvd',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 925000,
    beds: 5,
    baths: 4,
    sqft: 3200,
    yearBuilt: 2019,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Luxury contemporary home with mountain views',
    features: ['Mountain Views', 'Chef\'s Kitchen', 'Home Theater', '3-Car Garage'],
    lastUpdated: new Date('2024-01-14T14:20:00Z')
  },
  {
    mlsNumber: 'MLS003',
    address: '789 Tuscany Way',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 750000,
    beds: 3,
    baths: 2.5,
    sqft: 2200,
    yearBuilt: 2021,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Charming Tuscan-inspired home with modern amenities',
    features: ['Courtyard', 'Updated Kitchen', 'Guest Suite', '2-Car Garage'],
    lastUpdated: new Date('2024-01-13T09:15:00Z')
  },
  {
    mlsNumber: 'MLS004',
    address: '321 Desert Springs Ave',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 1100000,
    beds: 6,
    baths: 5.5,
    sqft: 4200,
    yearBuilt: 2018,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Estate-style home with resort-like amenities',
    features: ['Resort Pool', 'Wine Cellar', 'Chef\'s Kitchen', '4-Car Garage'],
    lastUpdated: new Date('2024-01-12T16:45:00Z')
  },
  {
    mlsNumber: 'MLS005',
    address: '654 Mountain Vista Dr',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 680000,
    beds: 3,
    baths: 2,
    sqft: 1950,
    yearBuilt: 2022,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Modern townhome with mountain views',
    features: ['Mountain Views', 'Open Floor Plan', 'Private Patio', '2-Car Garage'],
    lastUpdated: new Date('2024-01-11T11:30:00Z')
  },
  {
    mlsNumber: 'MLS006',
    address: '987 Canyon Ridge Ln',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 950000,
    beds: 4,
    baths: 3,
    sqft: 2800,
    yearBuilt: 2020,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Elegant home with panoramic city views',
    features: ['City Views', 'Gourmet Kitchen', 'Master Suite', '2-Car Garage'],
    lastUpdated: new Date('2024-01-10T13:20:00Z')
  },
  {
    mlsNumber: 'MLS007',
    address: '147 Valley View Dr',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 820000,
    beds: 4,
    baths: 3.5,
    sqft: 2600,
    yearBuilt: 2021,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Spacious family home with great outdoor living space',
    features: ['Covered Patio', 'Updated Kitchen', 'Bonus Room', '2-Car Garage'],
    lastUpdated: new Date('2024-01-09T15:10:00Z')
  },
  {
    mlsNumber: 'MLS008',
    address: '258 Sunset Hills Blvd',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 1150000,
    beds: 5,
    baths: 4.5,
    sqft: 3800,
    yearBuilt: 2019,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Luxury home with resort-style amenities',
    features: ['Resort Pool', 'Home Theater', 'Wine Room', '3-Car Garage'],
    lastUpdated: new Date('2024-01-08T10:45:00Z')
  },
  {
    mlsNumber: 'MLS009',
    address: '369 Heritage Park Dr',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 720000,
    beds: 3,
    baths: 2.5,
    sqft: 2100,
    yearBuilt: 2022,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Charming home in a family-friendly neighborhood',
    features: ['Family Room', 'Updated Kitchen', 'Backyard', '2-Car Garage'],
    lastUpdated: new Date('2024-01-07T14:30:00Z')
  },
  {
    mlsNumber: 'MLS010',
    address: '741 West Summerlin Dr',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 890000,
    beds: 4,
    baths: 3,
    sqft: 2700,
    yearBuilt: 2020,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Beautiful home with modern design and great location',
    features: ['Modern Design', 'Gourmet Kitchen', 'Master Suite', '2-Car Garage'],
    lastUpdated: new Date('2024-01-06T12:15:00Z')
  },
  {
    mlsNumber: 'MLS011',
    address: '852 Red Rock View Dr',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 1050000,
    beds: 5,
    baths: 4,
    sqft: 3500,
    yearBuilt: 2018,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Estate-style home with breathtaking mountain views',
    features: ['Mountain Views', 'Chef\'s Kitchen', 'Home Office', '3-Car Garage'],
    lastUpdated: new Date('2024-01-05T09:20:00Z')
  },
  {
    mlsNumber: 'MLS012',
    address: '963 Tuscany Gardens Ln',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 780000,
    beds: 4,
    baths: 3.5,
    sqft: 2400,
    yearBuilt: 2021,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Elegant Tuscan-inspired home with modern updates',
    features: ['Tuscan Design', 'Updated Kitchen', 'Courtyard', '2-Car Garage'],
    lastUpdated: new Date('2024-01-04T16:40:00Z')
  },
  {
    mlsNumber: 'MLS013',
    address: '147 Desert Oasis Ave',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 920000,
    beds: 4,
    baths: 3,
    sqft: 2900,
    yearBuilt: 2020,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Spacious home with resort-style amenities',
    features: ['Resort Pool', 'Gourmet Kitchen', 'Bonus Room', '2-Car Garage'],
    lastUpdated: new Date('2024-01-03T11:25:00Z')
  },
  {
    mlsNumber: 'MLS014',
    address: '258 Mountain Vista Way',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 850000,
    beds: 4,
    baths: 3.5,
    sqft: 2600,
    yearBuilt: 2021,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Modern home with stunning mountain views',
    features: ['Mountain Views', 'Open Floor Plan', 'Master Suite', '2-Car Garage'],
    lastUpdated: new Date('2024-01-02T14:15:00Z')
  },
  {
    mlsNumber: 'MLS015',
    address: '369 Canyon Ridge Dr',
    city: 'Las Vegas',
    state: 'NV',
    zip: '89138',
    price: 980000,
    beds: 5,
    baths: 4,
    sqft: 3200,
    yearBuilt: 2019,
    propertyType: 'Single Family',
    status: 'Active',
    imageUrl: '/api/placeholder/800/600',
    description: 'Luxury home with panoramic views and premium finishes',
    features: ['Panoramic Views', 'Chef\'s Kitchen', 'Home Theater', '3-Car Garage'],
    lastUpdated: new Date('2024-01-01T10:50:00Z')
  }
];

export interface Home {
  mlsNumber: string;
  address: string;
  city: string;
  state: string;
  zip: string;
  price: number;
  beds: number;
  baths: number;
  sqft: number;
  yearBuilt: number;
  propertyType: string;
  status: string;
  imageUrl: string;
  description: string;
  features: string[];
  lastUpdated: Date;
}

export async function getHomes(): Promise<Home[]> {
  'use cache';
  
  console.log('[Next.js] Fetching home data for /');
  console.log(`[Next.js] Homes found: ${sampleHomes.length}`);
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 100));
  
  // In production, this would fetch from your MLS API or database
  // const homes = await fetchMLSHomes();
  
  return sampleHomes.map((home) => ({
    ...home,
    imageUrl: propertyImage(home.mlsNumber),
  }));
}

export async function getHomeByMLS(mlsNumber: string): Promise<Home | null> {
  'use cache';
  
  console.log(`[Next.js] Fetching home data for MLS: ${mlsNumber}`);
  
  const home = sampleHomes.find(h => h.mlsNumber === mlsNumber);
  
  if (!home) {
    return null;
  }
  
  return {
    ...home,
    imageUrl: propertyImage(home.mlsNumber),
  };
}

// Future function for real MLS API integration
async function fetchMLSHomes(): Promise<Home[]> {
  // This would integrate with your MLS provider (e.g., MLS Grid, RETS, etc.)
  // For now, return sample data
  return sampleHomes;
}
