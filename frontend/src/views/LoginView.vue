<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-tr from-slate-100 via-violet-100 to-indigo-100 dark:from-zinc-950 dark:via-purple-950 dark:to-zinc-900 p-4 transition-colors duration-300">
    <!-- Card Glassmorphism -->
    <div class="w-full max-w-md bg-white/70 dark:bg-zinc-900/70 backdrop-blur-xl border border-white/20 dark:border-zinc-800/50 rounded-2xl shadow-2xl p-8 transition-all duration-300">
      
      <!-- Cabeçalho -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-violet-600 to-indigo-600 dark:from-violet-400 dark:to-indigo-400 bg-clip-text text-transparent mb-2">
          JanjIA
        </h1>
        <p class="text-slate-600 dark:text-zinc-400 text-sm">
          O chatbot que sabe de tudo, mas responde com abacates e pombos.
        </p>
      </div>

      <!-- Alerta de Erro -->
      <div v-if="error" class="mb-4 p-3 bg-red-100 border border-red-200 text-red-800 dark:bg-red-950/30 dark:border-red-900/50 dark:text-red-300 rounded-lg text-sm flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span>{{ error }}</span>
      </div>

      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label for="username" class="block text-xs font-semibold text-slate-700 dark:text-zinc-300 uppercase tracking-wider mb-2">
            Nome de Usuário
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            placeholder="Digite seu usuário"
            class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-950/50 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition"
          />
        </div>

        <div>
          <label for="password" class="block text-xs font-semibold text-slate-700 dark:text-zinc-300 uppercase tracking-wider mb-2">
            Senha
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-950/50 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 px-4 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:cursor-not-allowed transform active:scale-[0.98] transition-all duration-150 flex items-center justify-center gap-2"
        >
          <svg v-if="loading" class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Conectando ao cosmo...' : 'Entrar' }}</span>
        </button>
      </form>

      <!-- Rodapé do Card -->
      <div class="mt-6 text-center text-sm text-slate-600 dark:text-zinc-400">
        Não tem uma conta?
        <router-link to="/register" class="text-violet-600 dark:text-violet-400 font-semibold hover:underline">
          Cadastre-se grátis
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  loading.value = true
  error.value = null
  try {
    await authStore.login(username.value, password.value)
    
    // Redireciona para onde o usuário estava tentando ir, ou para a raiz '/'
    const redirectPath = route.query.redirect || '/'
    router.push(redirectPath)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao realizar login. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>
