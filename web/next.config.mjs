/** @type {import('next').NextConfig} */
const nextConfig = {
  // The Shared Air model is a standalone page in public/shared-air/; serve it at /shared-air too.
  async rewrites() {
    return [{ source: '/shared-air', destination: '/shared-air/index.html' }]
  },
  // The former "Proof Outline" page is now "Conjecture and Gaps" at /outline.
  async redirects() {
    return [{ source: '/proof', destination: '/outline', permanent: false }]
  },
}
export default nextConfig
