import type { NextConfig } from "next";
import { settings } from "@/settings";


const nextConfig: NextConfig = {
  //reactStrictMode: true,
  //compress: false,
  output: 'export',
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  //assetPrefix: settings.isDev ? "": settings.server.my_s3_bucket_domain_name,

  //images: {
    //unoptimized: true,
  //},
};

export default nextConfig;