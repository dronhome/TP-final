import type { NextConfig } from "next";

/**
 * Build-time switch:
 * - For GitHub Pages: set NEXT_PUBLIC_TARGET=gh-pages  → basePath '/team-19-web'
 * - For Netlify (root): set NEXT_PUBLIC_TARGET=netlify → basePath ''
 */
const target = process.env.NEXT_PUBLIC_TARGET;

const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  basePath: target === "gh-pages" ? "/team-19-web" : "",
};

export default nextConfig;
