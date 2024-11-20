/// <reference types="vitest" />
import vue from '@vitejs/plugin-vue'
import autoprefixer from 'autoprefixer'
import * as path from 'path'
import tailwind from 'tailwindcss'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@composables': path.resolve(__dirname, './src/composables'),
    },
  },
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: ['./test/setup.ts'],
    deps: {
      optimizer: {
        web: {
          include: ['msw'],
        },
      },
    },
  },
})
