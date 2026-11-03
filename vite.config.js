import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // 相对路径构建，适配 GitHub Pages 子路径部署
  base: './',
  plugins: [vue()],
  server: {
    port: 5173,
    open: true
  }
})
