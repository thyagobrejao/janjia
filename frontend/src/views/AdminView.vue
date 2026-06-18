<template>
  <div class="min-h-screen bg-slate-50 dark:bg-darkbg-chat text-slate-800 dark:text-zinc-100 transition-colors duration-200">
    
    <!-- BARRA SUPERIOR ADMIN -->
    <header class="h-16 bg-white dark:bg-darkbg-sidebar border-b border-slate-200/80 dark:border-zinc-800/80 px-6 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h1 class="text-xl font-bold tracking-wide">JanjIA - Painel de Controle</h1>
      </div>
      
      <div class="flex items-center gap-4">
        <ThemeToggle />
        <router-link
          to="/"
          class="flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 text-xs font-semibold rounded-xl transition duration-150 border border-slate-200/60 dark:border-zinc-700"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Voltar ao Chat
        </router-link>
      </div>
    </header>

    <!-- CONTEÚDO PRINCIPAL -->
    <main class="max-w-7xl mx-auto p-6 space-y-8">
      
      <!-- CARTÕES DE ESTATÍSTICAS (KPIs) -->
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Total de Usuários -->
        <div class="bg-white dark:bg-zinc-900 border border-slate-200/50 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex items-center justify-between hover:shadow-md transition">
          <div class="space-y-1">
            <span class="text-xs font-semibold text-slate-500 dark:text-zinc-400">Total de Usuários</span>
            <div class="text-3xl font-extrabold tracking-tight">
              {{ adminStore.stats?.total_users || 0 }}
            </div>
            <div class="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">
              {{ adminStore.stats?.active_users_24h || 0 }} ativos nas últimas 24h
            </div>
          </div>
          <div class="w-12 h-12 rounded-xl bg-violet-100 dark:bg-violet-950/30 flex items-center justify-center text-violet-600 dark:text-violet-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>

        <!-- Total de Conversas -->
        <div class="bg-white dark:bg-zinc-900 border border-slate-200/50 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex items-center justify-between hover:shadow-md transition">
          <div class="space-y-1">
            <span class="text-xs font-semibold text-slate-500 dark:text-zinc-400">Total de Conversas</span>
            <div class="text-3xl font-extrabold tracking-tight">
              {{ adminStore.stats?.total_conversations || 0 }}
            </div>
            <div class="text-[10px] text-slate-400">Salvas no PostgreSQL</div>
          </div>
          <div class="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-950/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
        </div>

        <!-- Total de Perguntas/Respostas -->
        <div class="bg-white dark:bg-zinc-900 border border-slate-200/50 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex items-center justify-between hover:shadow-md transition">
          <div class="space-y-1">
            <span class="text-xs font-semibold text-slate-500 dark:text-zinc-400">Interações Totais</span>
            <div class="text-3xl font-extrabold tracking-tight">
              {{ adminStore.stats?.total_questions || 0 }}
            </div>
            <div class="text-[10px] text-indigo-600 dark:text-indigo-400 font-bold">
              {{ adminStore.stats?.total_answers || 0 }} respostas da JanjIA
            </div>
          </div>
          <div class="w-12 h-12 rounded-xl bg-indigo-100 dark:bg-indigo-950/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
          </div>
        </div>

        <!-- Consumo do Modelo (Tokens) -->
        <div class="bg-white dark:bg-zinc-900 border border-slate-200/50 dark:border-zinc-800/80 rounded-2xl p-6 shadow-sm flex items-center justify-between hover:shadow-md transition">
          <div class="space-y-1">
            <span class="text-xs font-semibold text-slate-500 dark:text-zinc-400">Consumo Acumulado</span>
            <div class="text-3xl font-extrabold tracking-tight text-emerald-600 dark:text-emerald-400">
              {{ formatTokens(adminStore.stats?.total_prompt_tokens + adminStore.stats?.total_completion_tokens || 0) }}
            </div>
            <div class="text-[10px] text-slate-400 truncate max-w-[160px]" :title="adminStore.stats?.model_name">
              Modelo: {{ adminStore.stats?.model_name }}
            </div>
          </div>
          <div class="w-12 h-12 rounded-xl bg-emerald-100 dark:bg-emerald-950/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
          </div>
        </div>

      </section>

      <!-- SEÇÃO DETALHADA: LISTA DE USUÁRIOS -->
      <section class="bg-white dark:bg-zinc-900 border border-slate-200/50 dark:border-zinc-800/80 rounded-2xl shadow-sm overflow-hidden">
        <div class="p-6 border-b border-slate-200/80 dark:border-zinc-800/80 flex items-center justify-between">
          <h2 class="text-lg font-bold">Usuários Cadastrados</h2>
          <span class="text-xs text-slate-500 dark:text-zinc-400 font-semibold bg-slate-100 dark:bg-zinc-800 px-3 py-1 rounded-full">
            {{ adminStore.users.length }} usuários
          </span>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 dark:bg-zinc-950/50 text-[10px] uppercase font-bold tracking-wider text-slate-500 dark:text-zinc-400 border-b border-slate-200/80 dark:border-zinc-800/80">
                <th class="p-4 pl-6">ID</th>
                <th class="p-4">Nome de Usuário</th>
                <th class="p-4">E-mail</th>
                <th class="p-4">Tipo</th>
                <th class="p-4">Conversas Criadas</th>
                <th class="p-4 pr-6">Data de Cadastro</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-zinc-800/50 text-xs">
              <tr 
                v-for="user in adminStore.users" 
                :key="user.id"
                class="hover:bg-slate-50/50 dark:hover:bg-zinc-800/20 transition-colors"
              >
                <td class="p-4 pl-6 font-mono text-slate-400">#{{ user.id }}</td>
                <td class="p-4 font-semibold">{{ user.username }}</td>
                <td class="p-4 text-slate-600 dark:text-zinc-400">{{ user.email }}</td>
                <td class="p-4">
                  <span 
                    :class="[
                      'px-2 py-0.5 rounded text-[10px] font-bold',
                      user.is_admin 
                        ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/30 dark:text-emerald-300' 
                        : 'bg-slate-100 text-slate-600 dark:bg-zinc-800 dark:text-zinc-400'
                    ]"
                  >
                    {{ user.is_admin ? 'Admin' : 'Membro' }}
                  </span>
                </td>
                <td class="p-4 font-mono font-semibold">{{ user.conversation_count }}</td>
                <td class="p-4 pr-6 text-slate-400 font-medium">{{ formatDate(user.created_at) }}</td>
              </tr>
              
              <tr v-if="adminStore.users.length === 0">
                <td colspan="6" class="p-8 text-center text-slate-500 dark:text-zinc-400">
                  Nenhum usuário catalogado.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAdminStore } from '../stores/admin'
import ThemeToggle from '../components/ThemeToggle.vue'

const adminStore = useAdminStore()

const formatTokens = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await adminStore.fetchStats()
  await adminStore.fetchUsers()
})
</script>
