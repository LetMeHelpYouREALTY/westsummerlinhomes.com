// This will eventually integrate with RealScout API and Google Sheets
// For now, using mock data to get the site running

import { propertyImage } from './images';

export interface Home {
  mlsNumber: string;
  address: string;
  community: string;
  builder: string;
  listPrice: number;
  trueCost: number;
  incentives: Array<{
    type: string;
    amount: number;
    description: string;
    expiresAt: string;
  }>;
  bedrooms: number;
  bathrooms: number;
  sqft: number;
  moveInDate: string;
  status: string;
  photoUrl: string;
  isNew: boolean;
  hasPriceDrop: boolean;
}

// Mock data for development - replace with RealScout API calls
const mockHomes: Home[] = [
  {
    mlsNumber: "MLS123456",
    address: "12446 Weather Ridge Pl",
    community: "The Vistas",
    builder: "Lennar",
    listPrice: 725000,
    trueCost: 683000,
    incentives: [
      {
        type: "closing_cost",
        amount: 22000,
        description: "Closing cost credit",
        expiresAt: "2025-02-15"
      },
      {
        type: "rate_buydown",
        amount: 12000,
        description: "Rate buydown",
        expiresAt: "2025-02-15"
      }
    ],
    bedrooms: 3,
    bathrooms: 2.5,
    sqft: 2450,
    moveInDate: "2025-03-01",
    status: "Available",
    photoUrl: "",
    isNew: true,
    hasPriceDrop: false
  },
  {
    mlsNumber: "MLS789012",
    address: "5678 Red Rock Canyon Dr",
    community: "The Ridges",
    builder: "Pulte",
    listPrice: 695000,
    trueCost: 665000,
    incentives: [
      {
        type: "price_reduction",
        amount: 30000,
        description: "Builder incentive",
        expiresAt: "2025-02-20"
      }
    ],
    bedrooms: 4,
    bathrooms: 3,
    sqft: 2850,
    moveInDate: "2025-02-15",
    status: "Available",
    photoUrl: "",
    isNew: false,
    hasPriceDrop: true
  },
  {
    mlsNumber: "MLS345678",
    address: "9012 Grand Park Blvd",
    community: "Grand Park District",
    builder: "KB Homes",
    listPrice: 750000,
    trueCost: 700000,
    incentives: [
      {
        type: "upgrades",
        amount: 25000,
        description: "Design center credit",
        expiresAt: "2025-02-25"
      },
      {
        type: "closing_cost",
        amount: 25000,
        description: "Closing cost assistance",
        expiresAt: "2025-02-25"
      }
    ],
    bedrooms: 3,
    bathrooms: 2.5,
    sqft: 2600,
    moveInDate: "2025-03-15",
    status: "Available",
    photoUrl: "",
    isNew: true,
    hasPriceDrop: false
  }
];

export async function getHomes(): Promise<Home[]> {
  // TODO: Replace with RealScout API call
  // const realScoutHomes = await fetchFromRealScout();
  
  // TODO: Replace with Google Sheets API call for incentives
  // const incentives = await fetchFromGoogleSheets();
  
  // TODO: Merge RealScout data with incentives
  // return mergeHomeData(realScoutHomes, incentives);
  
  // For now, return mock data
  return mockHomes
    .map((home) => ({
      ...home,
      photoUrl: propertyImage(home.mlsNumber),
    }))
    .sort((a, b) => a.trueCost - b.trueCost);
}

// Future RealScout integration
export async function fetchFromRealScout() {
  // TODO: Implement RealScout API call
  // GET https://api.realscout.com/v2/saved_searches/{savedSearchId}/listings
  // Filter: Summerlin West, $650-750K, New Construction
  throw new Error("RealScout integration not yet implemented");
}

// Future Google Sheets integration
export async function fetchFromGoogleSheets() {
  // TODO: Implement Google Sheets API call for incentives
  throw new Error("Google Sheets integration not yet implemented");
}

// Future data merging function
export function mergeHomeData(mlsHomes: any[], incentives: any[]) {
  // TODO: Merge MLS data with incentive data
  // Calculate true cost for each home
  throw new Error("Data merging not yet implemented");
}
