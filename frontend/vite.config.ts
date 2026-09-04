/// <reference types="vitest/config" />
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    // PWA: gera o Service Worker (abrir sem rede) e o manifesto (instalar no
    // celular). Os DADOS offline são responsabilidade do IndexedDB (Fase 1);
    // aqui cacheamos apenas o "app shell" (HTML/JS/CSS/ícones).
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'pwa-icon.svg'],
      manifest: {
        name: 'Arkheion — Fichas de Tormenta 20',
        short_name: 'Arkheion',
        description:
          'Ficha de RPG de Tormenta 20 com cálculos automáticos, funcionando offline.',
        lang: 'pt-BR',
        theme_color: '#590d1c',
        background_color: '#24140f',
        display: 'standalone',
        orientation: 'portrait',
        start_url: '/',
        scope: '/',
        icons: [
          { src: 'pwa-icon.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any' },
          { src: 'pwa-icon.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'maskable' },
        ],
      },
      workbox: {
        // App shell que é pré-cacheado para abrir offline.
        globPatterns: ['**/*.{js,css,html,ico,svg,woff,woff2}'],
        // SPA: navegações offline caem no index.html (o Vue Router assume a rota).
        navigateFallback: '/index.html',
        // A API é outra origem e cuida dos dados via IndexedDB — não interceptar.
        navigateFallbackDenylist: [/^\/arkheion_api/],
        cleanupOutdatedCaches: true,
      },
      devOptions: {
        // SW desligado no `npm run dev` para não atrapalhar o HMR.
        // Para testar offline: `npm run build` + `npm run preview`.
        enabled: false,
      },
    }),
  ],
  server: {
    proxy: {
      '/arkheion_api': {
        target: process.env.VITE_API_URL || 'http://backend:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  test: {
    // O motor de regras é lógica pura — não precisa de DOM.
    environment: 'node',
    include: ['src/**/*.spec.ts'],
  },
})
