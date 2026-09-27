/**
 * West Summerlin hyperlocal amenity map configuration.
 * Center: Downtown Summerlin retail core (1980 Festival Plaza Dr, Las Vegas, NV 89135)
 * — documented hub for dining, shopping, and services serving Summerlin West villages.
 * Coordinates: Google Maps geocode of that address (~36.1486, -115.3342).
 */
(function (global) {
  var WEST_SUMMERLIN_AMENITY_CONFIG = {
    community: {
      name: 'West Summerlin',
      shortLabel: 'West Summerlin',
      city: 'Las Vegas',
      region: 'NV',
      center: { lat: 36.148611, lng: -115.334167 },
      zoom: 13,
      markerTitle: 'West Summerlin',
    },
    searchRadiusMeters: 8000,
    categoryOrder: [
      'golf',
      'parks',
      'grocery',
      'restaurants',
      'healthcare',
      'shopping',
      'fitness',
      'cafes',
      'pharmacies',
      'schools',
      'parking',
    ],
    categories: {
      golf: {
        label: 'Golf',
        primaryTypes: ['golf_course'],
        legacyType: 'golf_course',
      },
      parks: {
        label: 'Parks',
        primaryTypes: ['park'],
        legacyType: 'park',
      },
      grocery: {
        label: 'Grocery',
        primaryTypes: ['grocery_store', 'supermarket'],
        legacyType: 'grocery_or_supermarket',
      },
      restaurants: {
        label: 'Restaurants',
        primaryTypes: ['restaurant'],
        legacyType: 'restaurant',
      },
      healthcare: {
        label: 'Healthcare',
        primaryTypes: ['hospital', 'doctor'],
        legacyType: 'hospital',
      },
      shopping: {
        label: 'Shopping',
        primaryTypes: ['shopping_mall', 'department_store'],
        legacyType: 'shopping_mall',
      },
      fitness: {
        label: 'Fitness',
        primaryTypes: ['gym'],
        legacyType: 'gym',
      },
      cafes: {
        label: 'Cafes',
        primaryTypes: ['cafe'],
        legacyType: 'cafe',
      },
      pharmacies: {
        label: 'Pharmacies',
        primaryTypes: ['pharmacy'],
        legacyType: 'pharmacy',
      },
      schools: {
        label: 'Schools',
        primaryTypes: ['school', 'primary_school', 'secondary_school'],
        legacyType: 'school',
      },
      parking: {
        label: 'Parking',
        primaryTypes: ['parking'],
        legacyType: 'parking',
      },
    },
    staticAmenities: [
      {
        category: 'shopping',
        name: 'Downtown Summerlin',
        address: '1980 Festival Plaza Dr, Las Vegas, NV 89135',
        schemaType: 'ShoppingCenter',
      },
      {
        category: 'grocery',
        name: 'Whole Foods Market',
        address: '1700 Pavilion Center Dr, Las Vegas, NV 89135',
        schemaType: 'GroceryStore',
      },
      {
        category: 'grocery',
        name: "Smith's Food and Drug",
        address: '4750 W Flamingo Rd, Las Vegas, NV 89103',
        schemaType: 'GroceryStore',
      },
      {
        category: 'healthcare',
        name: 'Summerlin Hospital Medical Center',
        address: '657 N Town Center Dr, Las Vegas, NV 89144',
        schemaType: 'Hospital',
      },
      {
        category: 'parks',
        name: 'Exploration Peak Park',
        address: '9600 Scenic Desert Dr, Las Vegas, NV 89149',
        schemaType: 'Park',
      },
      {
        category: 'parks',
        name: 'Summerlin Centre Community Park',
        address: '10588 Discovery Springs Dr, Las Vegas, NV 89135',
        schemaType: 'Park',
      },
      {
        category: 'golf',
        name: 'Red Rock Country Club',
        address: '4615 S Red Rock Country Club Dr, Las Vegas, NV 89135',
        schemaType: 'GolfCourse',
      },
      {
        category: 'golf',
        name: 'Angel Park Golf Club',
        address: '1001 S Rampart Blvd, Las Vegas, NV 89145',
        schemaType: 'GolfCourse',
      },
      {
        category: 'golf',
        name: 'TPC Las Vegas',
        address: '1700 Village Center Cir, Las Vegas, NV 89134',
        schemaType: 'GolfCourse',
      },
      {
        category: 'schools',
        name: 'Palo Verde High School',
        address: '333 S Pavilion Center Dr, Las Vegas, NV 89144',
        schemaType: 'School',
      },
      {
        category: 'schools',
        name: 'Doral Academy Red Rock',
        address: '4141 N Buffalo Dr, Las Vegas, NV 89129',
        schemaType: 'School',
      },
    ],
  };

  global.WEST_SUMMERLIN_AMENITY_CONFIG = WEST_SUMMERLIN_AMENITY_CONFIG;
})(typeof window !== 'undefined' ? window : globalThis);
