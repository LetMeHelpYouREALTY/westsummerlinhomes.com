/**
 * West Summerlin hyperlocal amenity map configuration.
 * Center: Downtown Summerlin retail core (1980 Festival Plaza Dr, Las Vegas, NV 89135)
 * Coordinates: geocode of that address (~36.1486, -115.3342).
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
    searchRadiusMeters: 5000,
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
        sourceUrl: 'https://summerlin.com/downtown-summerlin/',
      },
      {
        category: 'grocery',
        name: 'Whole Foods Market',
        address: '2475 S Town Center Dr, Las Vegas, NV 89135',
        schemaType: 'GroceryStore',
        sourceUrl: 'https://www.wholefoodsmarket.com/stores/summerlin',
      },
      {
        category: 'grocery',
        name: "Smith's Food and Drug",
        address: '9851 W Charleston Blvd, Las Vegas, NV 89117',
        schemaType: 'GroceryStore',
        sourceUrl: 'https://www.smithsfoodanddrug.com/stores/grocery/nv/las-vegas/9851-w-charleston-blvd',
      },
      {
        category: 'healthcare',
        name: 'Summerlin Hospital Medical Center',
        address: '657 N Town Center Dr, Las Vegas, NV 89144',
        schemaType: 'Hospital',
        sourceUrl: 'https://www.summerlinhospital.com/about/contact-us',
      },
      {
        category: 'parks',
        name: 'Exploration Peak Park',
        address: '9700 S Buffalo Dr, Las Vegas, NV 89178',
        schemaType: 'Park',
        sourceUrl: 'https://parkslocator.clarkcountynv.gov/Search/ParkDetail?parkId=62',
      },
      {
        category: 'parks',
        name: 'Summerlin Centre Community Park',
        address: '10588 Marketwalk Pl, Las Vegas, NV 89135',
        schemaType: 'Park',
        sourceUrl: 'https://www.summerlin.com/explore/parks/',
      },
      {
        category: 'golf',
        name: 'Red Rock Country Club',
        address: '2250-A Red Springs Dr, Las Vegas, NV 89135',
        schemaType: 'GolfCourse',
        sourceUrl: 'https://www.redrockcountryclub.com/',
      },
      {
        category: 'golf',
        name: 'Angel Park Golf Club',
        address: '100 S Rampart Blvd, Las Vegas, NV 89145',
        schemaType: 'GolfCourse',
        sourceUrl: 'https://arcisgolf.com/clubs/angel-park-golf-club/hours-and-directions',
      },
      {
        category: 'golf',
        name: 'TPC Las Vegas',
        address: '9851 Canyon Run Dr, Las Vegas, NV 89144',
        schemaType: 'GolfCourse',
        sourceUrl: 'https://tpc.com/lasvegas/contact-directions/',
      },
      {
        category: 'schools',
        name: 'Palo Verde High School',
        address: '333 S Pavilion Center Dr, Las Vegas, NV 89144',
        schemaType: 'School',
        sourceUrl: 'https://www.paloverde.org/contact-us/contact',
      },
    ],
  };

  global.WEST_SUMMERLIN_AMENITY_CONFIG = WEST_SUMMERLIN_AMENITY_CONFIG;
})(typeof window !== 'undefined' ? window : globalThis);
