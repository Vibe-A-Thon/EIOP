import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    proxy: process.env.EOIP_DEV_API_URL ? {
      '/api': {target: process.env.EOIP_DEV_API_URL},
      '/health': {target: process.env.EOIP_DEV_API_URL},
      '/metrics': {target: process.env.EOIP_DEV_API_URL},
    } : undefined,
  },
  build: {
    manifest: true,
  },
});
