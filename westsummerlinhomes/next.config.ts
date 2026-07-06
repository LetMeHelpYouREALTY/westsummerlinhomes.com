import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  experimental: {
    useCache: true,
    inlineCss: true,
  },
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.jsdelivr.net', pathname: '/gh/**' },
      { protocol: 'https', hostname: 'cdn.westsummerlinhomes.com', pathname: '/**' },
      { protocol: 'https', hostname: 'images.westsummerlinhomes.com', pathname: '/**' },
      { protocol: 'https', hostname: 'imagedelivery.net', pathname: '/**' },
      { protocol: 'https', hostname: '*.r2.dev', pathname: '/**' },
      { protocol: 'https', hostname: 'avatars.githubusercontent.com', pathname: '/u/**' },
    ]
  },
  logging: {
    fetches: {
      fullUrl: true
    }
  }
};

export default nextConfig;
