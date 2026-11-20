import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

// host: true makes the dev server reachable through a forwarded port.
// allowedHosts lets GitHub Codespaces preview URLs (*.app.github.dev) through.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { host: true, port: 5173, strictPort: true, allowedHosts: ['.app.github.dev'] },
  preview: { host: true, port: 4173, strictPort: true, allowedHosts: ['.app.github.dev'] },
})
