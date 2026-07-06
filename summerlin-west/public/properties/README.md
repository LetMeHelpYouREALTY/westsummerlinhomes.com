# Property Images Directory

This directory contains property images for the West Summerlin Homes website.

## Image Requirements

- **Format**: JPEG, PNG, or WebP
- **Resolution**: Minimum 1200x800px for main images, 400x300px for thumbnails
- **File Size**: Optimize to under 500KB for main images, under 100KB for thumbnails
- **Naming Convention**: `prop-{ID}-{type}.{ext}` (e.g., `prop-001-main.jpg`)

## Current Sample Images

The following sample images are referenced in the demo:

- `prop-001-main.jpg` - Main image for property 001
- `prop-001-1.jpg` through `prop-001-4.jpg` - Gallery images for property 001
- `prop-002-main.jpg` - Main image for property 002
- `prop-002-1.jpg` through `prop-002-3.jpg` - Gallery images for property 002
- `prop-003-main.jpg` - Main image for property 003
- `prop-003-1.jpg` through `prop-003-5.jpg` - Gallery images for property 003

## Adding Real Images

1. Replace sample images with actual property photos
2. Ensure images are properly optimized and compressed
3. Update the `sampleProperties.ts` file with correct image paths
4. Test image loading performance using the browser's Network tab

## Performance Notes

- Images are automatically optimized by Next.js Image component
- WebP and AVIF formats are served when supported by the browser
- Lazy loading is implemented for images below the fold
- Priority loading is set for featured properties and hero images
