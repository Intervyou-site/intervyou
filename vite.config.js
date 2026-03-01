import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'static/react-dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        practice: './src/practice-entry.jsx'
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
      '/get_mock_question': 'http://localhost:8000',
      '/evaluate_answer': 'http://localhost:8000',
      '/set_category': 'http://localhost:8000',
      '/save_question': 'http://localhost:8000',
      '/clear_question_cache': 'http://localhost:8000'
    }
  }
})
