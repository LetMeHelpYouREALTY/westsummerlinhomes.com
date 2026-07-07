declare namespace JSX {
  interface IntrinsicElements {
    'realscout-office-listings': React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement>,
      HTMLElement
    > & {
      'agent-encoded-id'?: string
      'sort-order'?: string
      'listing-status'?: string
      'property-types'?: string
      'price-min'?: string
      'price-max'?: string
    }
  }
}
