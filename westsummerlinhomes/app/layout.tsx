import '../styles/globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'West Summerlin Homes by Dr. Jan Duffy | Las Vegas & Summerlin Real Estate',
  description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
  keywords: ['Summerlin homes', 'Las Vegas real estate', 'luxury homes', 'West Summerlin', 'real estate agent', 'Summerlin properties'],
  openGraph: {
    title: 'West Summerlin Homes by Dr. Jan Duffy | Las Vegas & Summerlin Real Estate',
    description: 'Discover luxury homes for sale in West Summerlin, Las Vegas. Expert real estate services with the latest market insights and exclusive properties.',
    url: 'https://westsummerlinhomes.com',
    siteName: 'West Summerlin Homes by Dr. Jan Duffy',
    locale: 'en_US',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">
        {children}
      </body>
    </html>
  );
}
