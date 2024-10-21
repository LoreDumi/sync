import { fileURLToPath, URL } from 'node:url'
import path from "path";

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  assetsInclude: ["**/*.sql"],
  optimizeDeps: {
    exclude: ["@electric-sql/pglite"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
