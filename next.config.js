/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  trailingSlash: false,
  assetPrefix: process.env.NODE_ENV === 'production' ? process.env.NEXT_PUBLIC_API_URL : undefined,
  basePath: process.env.NODE_ENV === 'production' ? '' : undefined,
}

module.exports = nextConfig 