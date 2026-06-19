import { createApp } from 'vue'
import pinia from './stores'
import App from './App.vue'
import './index.css'

const app = createApp(App)

// Instala o Pinia PRIMEIRO, antes de qualquer outro plugin.
// Isso garante que getActivePinia() retorne a instância correta
// em qualquer contexto (guards do router, stores, etc.)
app.use(pinia)

// Importa o Router dinamicamente APÓS o Pinia estar globalmente ativo.
// Imports estáticos são hoisted e avaliados antes do corpo do módulo,
// o que causava o erro "getActivePinia() was called but there was no active Pinia".
import('./router').then(({ default: router }) => {
  app.use(router)
  app.mount('#app')
})
