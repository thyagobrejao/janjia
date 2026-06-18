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
          Crie sua credencial galáctica para interagir com a inteligência nonsense.
        </p>
      </div>

      <!-- Alerta de Erro -->
      <div v-if="error" class="mb-4 p-3 bg-red-100 border border-red-200 text-red-800 dark:bg-red-950/30 dark:border-red-900/50 dark:text-red-300 rounded-lg text-sm flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span>{{ error }}</span>
      </div>

      <!-- Alerta de Sucesso -->
      <div v-if="success" class="mb-4 p-3 bg-green-100 border border-green-200 text-green-800 dark:bg-green-950/30 dark:border-green-900/50 dark:text-green-300 rounded-lg text-sm flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Cadastro realizado! Redirecionando...</span>
      </div>

      <!-- Formulário -->
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label for="username" class="block text-xs font-semibold text-slate-700 dark:text-zinc-300 uppercase tracking-wider mb-2">
            Nome de Usuário
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            placeholder="Escolha seu nome de usuário"
            class="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-950/50 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition"
          />
        </div>

        <div>
          <label for="email" class="block text-xs font-semibold text-slate-700 dark:text-zinc-300 uppercase tracking-wider mb-2">
            E-mail
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="usuario@dominio.com"
            class="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-950/50 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition"
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
            placeholder="Mínimo 6 caracteres"
            class="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-950/50 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition"
          />
        </div>

        <button
          type="submit"
          :disabled="loading || success"
          class="w-full py-3 px-4 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:cursor-not-allowed transform active:scale-[0.98] transition-all duration-150 flex items-center justify-center gap-2"
        >
          <svg v-if="loading" class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Sincronizando com a CPI...' : 'Cadastrar' }}</span>
        </button>
      </form>

      <!-- Rodapé do Card -->
      <div class="mt-6 text-center text-sm text-slate-600 dark:text-zinc-400">
        Já tem registro galáctico?
        <router-link to="/login" class="text-violet-600 dark:text-violet-400 font-semibold hover:underline">
          Faça login
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(false)

const handleRegister = async () => {
  if (password.value.length < 6) {
    error.value = 'A senha deve ter no mínimo 6 caracteres.'
    return
  }

  loading.value = true
  error.value = null
  success.value = false
  
  try {
    await authStore.register(username.value, email.value, password.value)
    success.value = true
    
    // Aguarda 2 segundos para o feedback visual de sucesso e vai para login
    setTimeout(() => {
      router.push({ name: 'login' })
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao realizar o cadastro. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>
