import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // 构建产物根路径：适配 GitHub Pages 新仓库名 nanqiao-night-market
  base: '/nanqiao-night-market/',
  plugins: [vue()],
  server: {
    port: 5173,
    open: true
  }
})
