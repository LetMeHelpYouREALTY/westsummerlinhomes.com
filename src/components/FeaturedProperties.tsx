export default function FeaturedProperties() {
  return (
    <section className="section-padding bg-neutral-50">
      <div className="container">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold mb-6">
            Featured Properties
          </h2>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Browse live MLS listings in West Summerlin from $800K to $1M.
          </p>
        </div>

        <div
          className="realscout-listings-widget"
          dangerouslySetInnerHTML={{
            __html:
              '<realscout-office-listings agent-encoded-id="QWdlbnQtMjI1MDUw" sort-order="SOLD_DATE_NEWEST" listing-status="For Sale" property-types=",SFR,MOBILE" price-min="800000" price-max="1000000"></realscout-office-listings>',
          }}
        />
      </div>
    </section>
  )
}
