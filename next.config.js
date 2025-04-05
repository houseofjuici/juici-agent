/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  trailingSlash: false,
  assetPrefix: process.env.NODE_ENV === 'production' ? undefined : undefined,
  experimental: {
    strictMode: true,
  },
}

module.exports = nextConfig 