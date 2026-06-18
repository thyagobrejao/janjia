<template>
  <div class="flex h-screen bg-slate-50 dark:bg-darkbg-chat text-slate-800 dark:text-zinc-100 overflow-hidden">
    
    <!-- BARRA LATERAL (SIDEBAR) -->
    <aside 
      :class="[
        'fixed inset-y-0 left-0 z-30 w-64 bg-slate-900 text-slate-200 flex flex-col transform md:translate-x-0 transition-transform duration-300 ease-in-out',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:relative'
      ]"
    >
      <!-- Cabeçalho Sidebar -->
      <div class="p-4 flex items-center justify-between border-b border-slate-800">
        <h2 class="text-xl font-bold tracking-wider flex items-center gap-2 text-violet-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          JanjIA Chat
        </h2>
        <button @click="isSidebarOpen = false" class="md:hidden p-1 text-slate-400 hover:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Ação Principal: Nova Conversa -->
      <div class="p-4">
        <button
          @click="startNewConversation"
          class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-violet-600 hover:bg-violet-700 text-white font-semibold rounded-xl transition duration-150 shadow-md hover:shadow-violet-900/20 active:scale-[0.98]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nova Conversa
        </button>
      </div>

      <!-- Histórico de Conversas -->
      <div class="flex-1 overflow-y-auto px-2 space-y-1">
        <div v-if="chatStore.conversations.length === 0" class="text-center text-xs text-slate-500 py-8">
          Nenhuma conversa estelar.
        </div>
        
        <div
          v-for="conv in chatStore.conversations"
          :key="conv.id"
          :class="[
            'group relative flex items-center justify-between px-3 py-2.5 rounded-lg text-sm cursor-pointer transition-colors duration-150',
            chatStore.activeConversation?.id === conv.id 
              ? 'bg-slate-800 text-white font-medium' 
              : 'hover:bg-slate-800/50 text-slate-400 hover:text-slate-200'
          ]"
          @click="selectConversation(conv.id)"
        >
          <!-- Modo Visualização / Edição -->
          <div class="flex items-center gap-2 overflow-hidden w-full pr-10">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            
            <input
              v-if="editingConvId === conv.id"
              ref="renameInput"
              v-model="editingTitle"
              @blur="saveRename(conv.id)"
              @keyup.enter="saveRename(conv.id)"
              @click.stop
              class="bg-slate-700 text-white px-2 py-0.5 rounded focus:outline-none w-full text-xs"
            />
            <span v-else class="truncate text-xs">{{ conv.title }}</span>
          </div>

          <!-- Ações rápidas (Apenas aparecem no Hover no Desktop, ou fixas no Mobile/Active) -->
          <div class="absolute right-2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
            <button 
              @click.stop="startRename(conv.id, conv.title)"
              class="p-1 hover:text-violet-400 text-slate-400 rounded transition"
              title="Renomear"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <button 
              @click.stop="deleteConversation(conv.id)"
              class="p-1 hover:text-red-400 text-slate-400 rounded transition"
              title="Excluir"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Rodapé Sidebar: Admin Link + Perfil -->
      <div class="p-4 border-t border-slate-800 space-y-3">
        <!-- Link de Admin (apenas visível se for admin) -->
        <router-link
          v-if="authStore.isAdmin"
          to="/admin"
          class="flex items-center gap-2 text-xs font-semibold text-emerald-400 hover:text-emerald-300 transition duration-150 py-1.5 px-2 rounded hover:bg-slate-800"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Painel do Administrador
        </router-link>

        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center gap-2 truncate">
            <div class="w-7 h-7 rounded-full bg-violet-500/30 flex items-center justify-center font-bold text-violet-300">
              {{ authStore.user?.username ? authStore.user.username.substring(0, 2).toUpperCase() : 'US' }}
            </div>
            <span class="truncate text-slate-300 font-semibold">{{ authStore.user?.username || 'Carregando...' }}</span>
          </div>
          <button 
            @click="handleLogout"
            class="text-slate-400 hover:text-white p-1.5 rounded hover:bg-slate-800 transition"
            title="Sair"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4.5 w-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- ÁREA PRINCIPAL DO CHAT -->
    <main class="flex-1 flex flex-col h-full relative overflow-hidden">
      
      <!-- BARRA SUPERIOR (TOPBAR) -->
      <header class="h-14 bg-white dark:bg-darkbg-sidebar border-b border-slate-200/80 dark:border-zinc-800/80 px-4 flex items-center justify-between z-10 shrink-0 shadow-sm">
        <div class="flex items-center gap-3">
          <!-- Botão Hamburguer no Mobile -->
          <button 
            @click="isSidebarOpen = true"
            class="md:hidden p-2 text-slate-500 hover:text-slate-700 dark:text-zinc-400 dark:hover:text-white rounded-lg hover:bg-slate-100 dark:hover:bg-zinc-800 transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <span class="font-semibold text-slate-700 dark:text-zinc-200">
            {{ chatStore.activeConversation ? chatStore.activeConversation.title : 'JanjIA Chat' }}
          </span>
        </div>

        <div class="flex items-center gap-2">
          <!-- Botão de Alternância de Tema -->
          <ThemeToggle />
        </div>
      </header>

      <!-- HISTÓRICO DE MENSAGENS -->
      <div 
        ref="chatContainer"
        class="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 scroll-smooth bg-slate-50/50 dark:bg-darkbg-chat"
      >
        <!-- Estado Vazio: Janela de Introdução -->
        <div v-if="!chatStore.activeConversation || chatStore.messages.length === 0" class="max-w-2xl mx-auto h-full flex flex-col justify-center items-center py-10 md:py-16 text-center">
          
          <div class="w-20 h-20 rounded-2xl bg-gradient-to-tr from-violet-600 to-indigo-600 shadow-xl flex items-center justify-center text-white mb-6 transform hover:rotate-12 transition duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 9H3m14.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 12.728l-.707-.707M12 12a3 3 0 100-6 3 3 0 000 6z" />
            </svg>
          </div>

          <h2 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-violet-600 to-indigo-600 dark:from-violet-400 dark:to-indigo-400 bg-clip-text text-transparent mb-3">
            Bem-vindo ao JanjIA
          </h2>
          <p class="text-slate-500 dark:text-zinc-400 text-sm max-w-md mb-8">
            Faça perguntas sérias. Ou de preferência absurdas. A IA responderá sempre mantendo o auto-controle absurdo dela.
          </p>

          <!-- Sugestões de Prompts -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
            <button
              v-for="sug in suggestions"
              :key="sug.text"
              @click="useSuggestion(sug.text)"
              class="p-4 bg-white dark:bg-zinc-900 border border-slate-200/60 dark:border-zinc-800/80 rounded-xl text-left hover:border-violet-500 dark:hover:border-violet-500 hover:shadow-md dark:hover:bg-zinc-800/30 transition duration-150 group"
            >
              <div class="text-lg mb-1">{{ sug.icon }}</div>
              <p class="text-xs font-semibold text-slate-700 dark:text-zinc-300 group-hover:text-violet-600 dark:group-hover:text-violet-400">
                {{ sug.text }}
              </p>
            </button>
          </div>
        </div>

        <!-- Lista de Mensagens do Chat -->
        <div v-else class="max-w-3xl mx-auto space-y-6">
          <div
            v-for="msg in chatStore.messages"
            :key="msg.id"
            :class="[
              'flex gap-4 p-4 rounded-xl transition duration-150 shadow-sm border border-slate-200/30 dark:border-zinc-800/30',
              msg.role === 'user'
                ? 'bg-violet-500/5 dark:bg-violet-500/5 ml-12 border-violet-500/10'
                : 'bg-white dark:bg-zinc-900 mr-12'
            ]"
          >
            <!-- Avatar -->
            <div 
              :class="[
                'w-9 h-9 rounded-xl shrink-0 flex items-center justify-center font-bold text-sm shadow-sm',
                msg.role === 'user' 
                  ? 'bg-violet-600 text-white' 
                  : 'bg-emerald-600 text-white'
              ]"
            >
              <span v-if="msg.role === 'user'">U</span>
              <span v-else>J</span>
            </div>

            <!-- Corpo da mensagem -->
            <div class="flex-1 space-y-2 overflow-hidden">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-slate-500 dark:text-zinc-400">
                  {{ msg.role === 'user' ? 'Você' : 'JanjIA' }}
                </span>
                
                <!-- Informações Extras da Mensagem (Apenas IA) -->
                <div v-if="msg.role === 'assistant'" class="flex items-center gap-2 text-[10px] text-slate-400 dark:text-zinc-500">
                  <span 
                    v-if="msg.satire_level > 0"
                    :class="[
                      'px-1.5 py-0.5 rounded font-semibold',
                      msg.satire_level === 1 ? 'bg-amber-100 text-amber-800 dark:bg-amber-950/30 dark:text-amber-300' :
                      msg.satire_level === 2 ? 'bg-orange-100 text-orange-800 dark:bg-orange-950/30 dark:text-orange-300' :
                      'bg-red-100 text-red-800 dark:bg-red-950/30 dark:text-red-300'
                    ]"
                  >
                    Satirização Lvl {{ msg.satire_level }}
                  </span>
                  <span v-if="msg.tokens_completion > 0" title="Prompt + Resposta">
                    {{ msg.tokens_prompt + msg.tokens_completion }} tokens
                  </span>
                </div>
              </div>
              
              <!-- Texto da Mensagem -->
              <div v-if="msg.role === 'assistant' && !msg.content && chatStore.isStreaming" class="flex items-center gap-1.5 py-1 text-slate-400 dark:text-zinc-500">
                <span class="text-xs font-semibold animate-pulse">Consultando os abacates...</span>
                <span class="w-1.5 h-1.5 bg-slate-400 dark:bg-zinc-500 rounded-full dot-bounce"></span>
                <span class="w-1.5 h-1.5 bg-slate-400 dark:bg-zinc-500 rounded-full dot-bounce delay-200"></span>
                <span class="w-1.5 h-1.5 bg-slate-400 dark:bg-zinc-500 rounded-full dot-bounce delay-400"></span>
              </div>
              <p v-else class="text-sm leading-relaxed whitespace-pre-wrap break-words text-slate-700 dark:text-zinc-200">
                {{ msg.content }}<span v-if="msg.role === 'assistant' && chatStore.isStreaming && msg.id === chatStore.messages[chatStore.messages.length - 1]?.id" class="inline-block w-1.5 h-4 ml-1 bg-violet-600 dark:bg-violet-400 align-middle animate-blink"></span>
              </p>
            </div>
          </div>
          
          <!-- Elemento de ancoragem para o Scroll -->
          <div ref="bottomMarker" class="h-2"></div>
        </div>

      </div>

      <!-- FOOTER DE ENVIO E CONTROLES -->
      <footer class="p-4 border-t border-slate-200/80 dark:border-zinc-800/80 bg-white dark:bg-darkbg-sidebar shrink-0 shadow-inner">
        <div class="max-w-3xl mx-auto space-y-3">
          
          <!-- Seletor de Intensidade da Satirização (0 a 3) -->
          <div class="flex items-center justify-between px-2">
            <div class="flex items-center gap-1.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-violet-500 dark:text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span class="text-xs font-semibold text-slate-600 dark:text-zinc-400">Intensidade Satírica:</span>
            </div>
            
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-violet-600 dark:text-violet-400 bg-violet-100 dark:bg-violet-950/30 px-2.5 py-0.5 rounded-full">
                {{ satireLevels[satireLevel] }}
              </span>
            </div>
          </div>
          
          <div class="px-2">
            <input 
              v-model.number="satireLevel"
              type="range"
              min="0"
              max="3"
              step="1"
              class="w-full h-1.5 bg-slate-200 dark:bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-violet-600 dark:accent-violet-500"
            />
            <div class="flex justify-between text-[10px] text-slate-400 dark:text-zinc-500 mt-1 font-semibold">
              <span>0 (Normal)</span>
              <span>1 (Leve)</span>
              <span>2 (Moderado)</span>
              <span>3 (Total Nonsense)</span>
            </div>
          </div>

          <!-- Caixa de Entrada de Texto -->
          <form @submit.prevent="sendMessage" class="relative flex items-center">
            <textarea
              v-model="inputMessage"
              rows="1"
              @keydown.enter.prevent="onEnterKey"
              placeholder="Pergunte sobre a CPI dos guarda-chuvas..."
              :disabled="chatStore.isStreaming"
              class="w-full pr-12 pl-4 py-3 border border-slate-200 dark:border-zinc-800 rounded-xl bg-slate-50 dark:bg-zinc-950 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent resize-none overflow-hidden max-h-48 text-sm dark:text-zinc-200 disabled:opacity-50"
            ></textarea>
            
            <button
              type="submit"
              :disabled="!inputMessage.trim() || chatStore.isStreaming"
              class="absolute right-2.5 p-2 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 disabled:from-slate-300 disabled:to-slate-300 dark:disabled:from-zinc-800 dark:disabled:to-zinc-800 text-white rounded-lg transition duration-150 active:scale-95 disabled:scale-100 shadow-md disabled:shadow-none"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>

          <!-- Disclaimer de paródia -->
          <p class="text-center text-[10px] text-slate-400 dark:text-zinc-500 tracking-wide font-medium">
            JanjIA é um chatbot de humor e paródia. As respostas são absurdas por design e não refletem pessoas ou fatos reais.
          </p>

        </div>
      </footer>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import ThemeToggle from '../components/ThemeToggle.vue'

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

// Estados Locais
const isSidebarOpen = ref(false)
const inputMessage = ref('')
const satireLevel = ref(2) // Padrão: Moderado
const editingConvId = ref(null)
const editingTitle = ref('')
const renameInput = ref(null)

const chatContainer = ref(null)
const bottomMarker = ref(null)

const satireLevels = {
  0: 'Nível 0 - Resposta Normal',
  1: 'Nível 1 - Humor Leve',
  2: 'Nível 2 - Moderadamente Absurdo',
  3: 'Nível 3 - Totalmente Nonsense'
}

const suggestions = [
  { icon: '☂️', text: 'Devemos abrir uma CPI dos guarda-chuvas?' },
  { icon: '🥑', text: 'Qual a opinião dos especialistas em abacates sobre a física quântica?' },
  { icon: '🐦', text: 'Qual o papel dos pombos na economia global?' }
]

// Logout
const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'login' })
}

// Seleciona conversa e fecha sidebar no mobile
const selectConversation = async (id) => {
  isSidebarOpen.value = false
  await chatStore.selectConversation(id)
  scrollToBottom()
}

// Nova conversa
const startNewConversation = async () => {
  try {
    const newConv = await chatStore.createConversation('Nova Conversa Absurda')
    isSidebarOpen.value = false
    scrollToBottom()
  } catch (error) {
    console.error("Falha ao abrir nova conversa:", error)
  }
}

// Renomear Conversa
const startRename = (id, title) => {
  editingConvId.value = id
  editingTitle.value = title
  nextTick(() => {
    // Foca no input após renderização
    if (renameInput.value && renameInput.value[0]) {
      renameInput.value[0].focus()
    }
  })
}

const saveRename = async (id) => {
  if (!editingTitle.value.trim()) {
    editingConvId.value = null
    return
  }
  try {
    await chatStore.renameConversation(id, editingTitle.value)
  } catch (err) {
    console.error("Erro ao salvar renomeação:", err)
  } finally {
    editingConvId.value = null
  }
}

// Excluir Conversa
const deleteConversation = async (id) => {
  if (confirm("Você deseja apagar essa conversa intergaláctica para sempre?")) {
    try {
      await chatStore.deleteConversation(id)
    } catch (err) {
      console.error(err)
    }
  }
}

// Enviar Mensagem
const sendMessage = async () => {
  const text = inputMessage.value.trim()
  if (!text || chatStore.isStreaming) return
  
  // Se não houver nenhuma conversa aberta, cria uma primeiro automaticamente
  if (!chatStore.activeConversation) {
    try {
      // Abre conversa com as primeiras 4 palavras da mensagem
      const convTitle = text.split(' ').slice(0, 4).join(' ') || 'Conversa Iniciada'
      await chatStore.createConversation(convTitle)
    } catch (e) {
      return
    }
  }
  
  inputMessage.value = ''
  
  // Rola instantaneamente ao enviar
  nextTick(scrollToBottom)
  
  await chatStore.sendMessage(text, satireLevel.value)
}

// Submeter ao pressionar Enter (mas permitir Shift+Enter para quebra de linha)
const onEnterKey = (event) => {
  if (!event.shiftKey) {
    sendMessage()
  }
}

// Usa prompt de sugestão rápida
const useSuggestion = (text) => {
  inputMessage.value = text
  sendMessage()
}

// Rola a área de mensagens para o final
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// Observa mudanças nas mensagens para rolar a tela
watch(() => chatStore.messages, () => {
  nextTick(scrollToBottom)
}, { deep: true })

// Observa streaming de chunk para rolar a tela em tempo real
watch(() => chatStore.streamingContent, () => {
  nextTick(scrollToBottom)
})

onMounted(async () => {
  await chatStore.fetchConversations()
  if (chatStore.conversations.length > 0) {
    await selectConversation(chatStore.conversations[0].id)
  }
})
</script>
