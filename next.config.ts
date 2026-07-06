import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.jsdelivr.net', pathname: '/gh/**' },
      { protocol: 'https', hostname: 'cdn.westsummerlinhomes.com', pathname: '/**' },
      { protocol: 'https', hostname: 'images.westsummerlinhomes.com', pathname: '/**' },
      { protocol: 'https', hostname: 'imagedelivery.net', pathname: '/**' },
      { protocol: 'https', hostname: '*.r2.dev', pathname: '/**' },
    ],
  },
  compress: true,
  poweredByHeader: false,
  reactStrictMode: true,
  swcMinify: true,
}

export default nextConfig
