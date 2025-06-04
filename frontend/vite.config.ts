
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['src/**/*.test.{ts,tsx}'],
    exclude: ['tests/**'],
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: ['frontend', 'localhost'],
  },
})