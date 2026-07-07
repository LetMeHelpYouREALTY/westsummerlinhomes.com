import { getHomes } from '../lib/homes';
import HomeCard from './components/HomeCard';
import SkeletonCard from './components/SkeletonCard';
import React from 'react';

export default async function HomePage() {
  const homes = await getHomes();
  
  return (
    <div>
      {/* Trust Bar */}
      <div className="trust-bar">
        <span>🏠 Trusted by 500+ Summerlin West Buyers</span>
      </div>

      {/* Header */}
      <header>
        <div className="container">
          <div className="logo">Summerlin West Homes</div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1 className="hero-title">
            Summerlin West Daily Tracker
          </h1>
          <p className="hero-subtitle">
            Track 15 new construction homes with builder incentives. See the real cost after incentives.
          </p>
          
          {/* Key Metrics Bar */}
          <div className="hero-metrics">
            <div className="metric">
              <div className="metric-value">15</div>
              <div className="metric-label">Homes Available</div>
            </div>
            <div className="metric">
              <div className="metric-value">$650K</div>
              <div className="metric-label">Starting Price</div>
            </div>
            <div className="metric">
              <div className="metric-value">$42K</div>
              <div className="metric-label">Avg Incentives</div>
            </div>
            <div className="metric">
              <div className="metric-value">Daily</div>
              <div className="metric-label">Updates</div>
            </div>
          </div>
        </div>
      </section>

      {/* Live Counter */}
      <div className="live-counter">
        <span className="live-dot"></span>
        {homes.length} Homes Available Now
      </div>

      {/* RealScout Advanced Search */}
      <section className="search-section">
        <div className="container">
          <h2 style={{ 
            textAlign: 'center', 
            marginBottom: '2rem',
            fontSize: '2rem',
            fontWeight: '700',
            color: 'var(--primary)'
          }}>
            Find Your Perfect Summerlin West Home
          </h2>
          {React.createElement('realscout-advanced-search', {
            'agent-encoded-id': 'QWdlbnQtMjI1MDUw',
            'sort-order': 'STATUS_AND_SIGNIFICANT_CHANGE',
            'listing-status': 'For Sale',
            'property-types': 'SFR,MF',
            'price-min': '600000',
            'price-max': '750000',
            'city': 'Las Vegas',
            'state': 'NV',
            'neighborhood': 'Summerlin West'
          })}
        </div>
      </section>

      {/* RealScout Office Listings - Summerlin West Focused */}
      <section className="listings-section">
        <div className="container">
          <h2 style={{ 
            textAlign: 'center', 
            marginBottom: '2rem',
            fontSize: '2rem',
            fontWeight: '700',
            color: 'var(--primary)'
          }}>
            Current Summerlin West Listings
          </h2>
          {React.createElement('realscout-office-listings', {
            'agent-encoded-id': 'QWdlbnQtMjI1MDUw',
            'sort-order': 'STATUS_AND_SIGNIFICANT_CHANGE',
            'listing-status': 'For Sale',
            'property-types': 'SFR,MF',
            'price-min': '600000',
            'price-max': '750000',
            'city': 'Las Vegas',
            'state': 'NV',
            'neighborhood': 'Summerlin West'
          })}
        </div>
      </section>

      {/* Legacy Property Cards (Fallback) */}
      <section className="legacy-properties" style={{ display: 'none' }}>
        <div className="container">
          <h2 style={{ 
            textAlign: 'center', 
            marginBottom: '2rem',
            fontSize: '2rem',
            fontWeight: '700',
            color: 'var(--primary)'
          }}>
            Featured Properties
          </h2>
          <div className="properties-grid">
            {homes.length > 0 ? (
              homes.map(home => (
                <HomeCard key={home.mlsNumber} {...home} />
              ))
            ) : (
              // Show skeleton loading while data loads
              Array.from({ length: 6 }).map((_, index) => (
                <SkeletonCard key={index} />
              ))
            )}
          </div>
        </div>
      </section>

      {/* Sticky CTA Bar */}
      <div className="sticky-cta">
        <button className="sticky-cta-button">
          📞 Call Now: (702) 222-1964
        </button>
        <button className="sticky-cta-button">
          📧 Get Daily Updates
        </button>
      </div>
    </div>
  );
}
