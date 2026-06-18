import { defineStore } from 'pinia'
import api from '../utils/api'

export const useChatStore = defineStore('chat', {
  state: () => ({
    conversations: [],
    activeConversation: null,
    messages: [],
    isStreaming: false,
    streamingContent: ''
  }),
  
  actions: {
    async fetchConversations() {
      try {
        const response = await api.get('/conversations')
        this.conversations = response.data
      } catch (error) {
        console.error("Erro ao carregar conversas:", error)
      }
    },
    
    async fetchMessages(conversationId) {
      try {
        const response = await api.get(`/conversations/${conversationId}/messages`)
        this.messages = response.data
      } catch (error) {
        console.error("Erro ao carregar mensagens:", error)
      }
    },
    
    async selectConversation(conversationId) {
      const conv = this.conversations.find(c => c.id === conversationId)
      if (conv) {
        this.activeConversation = conv
        await this.fetchMessages(conversationId)
      }
    },
    
    async createConversation(title = 'Nova Conversa') {
      try {
        const response = await api.post('/conversations', { title })
        const newConv = response.data
        this.conversations.unshift(newConv)
        this.activeConversation = newConv
        this.messages = []
        return newConv
      } catch (error) {
        console.error("Erro ao criar conversa:", error)
        throw error
      }
    },
    
    async renameConversation(conversationId, title) {
      try {
        const response = await api.patch(`/conversations/${conversationId}`, { title })
        const index = this.conversations.findIndex(c => c.id === conversationId)
        if (index !== -1) {
          this.conversations[index] = response.data
        }
        if (this.activeConversation?.id === conversationId) {
          this.activeConversation.title = title
        }
      } catch (error) {
        console.error("Erro ao renomear conversa:", error)
        throw error
      }
    },
    
    async deleteConversation(conversationId) {
      try {
        await api.delete(`/conversations/${conversationId}`)
        this.conversations = this.conversations.filter(c => c.id !== conversationId)
        if (this.activeConversation?.id === conversationId) {
          this.activeConversation = null
          this.messages = []
        }
      } catch (error) {
        console.error("Erro ao excluir conversa:", error)
        throw error
      }
    },
    
    async sendMessage(content, satireLevel) {
      if (!this.activeConversation) return
      
      const conversationId = this.activeConversation.id
      this.isStreaming = true
      this.streamingContent = ''
      
      // 1. Adiciona a mensagem do usuário localmente
      const userMessage = {
        id: Date.now(), // ID temporário
        role: 'user',
        content,
        satire_level: 0,
        tokens_prompt: 0,
        tokens_completion: 0,
        created_at: new Date().toISOString()
      }
      this.messages.push(userMessage)
      
      // 2. Adiciona o placeholder para a resposta do assistente
      const assistantMessagePlaceholder = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '',
        satire_level: satireLevel,
        tokens_prompt: 0,
        tokens_completion: 0,
        created_at: new Date().toISOString()
      }
      this.messages.push(assistantMessagePlaceholder)
      
      try {
        // Envia via Fetch Nativo para conseguir ler a Stream com headers de Auth
        const response = await fetch(`/api/conversations/${conversationId}/messages`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            content,
            satire_level: satireLevel
          })
        })
        
        if (!response.ok) {
          throw new Error(`Servidor respondeu com status ${response.status}`)
        }
        
        const reader = response.body.getReader()
        const decoder = new TextDecoder('utf-8')
        let buffer = ''
        
        const processBlock = (block) => {
          const lines = block.split(/\r?\n/)
          let eventType = 'message'
          let eventData = null
          
          for (const line of lines) {
            const trimmed = line.trim()
            if (!trimmed) continue
            if (trimmed.startsWith('event:')) {
              eventType = trimmed.replace('event:', '').trim()
            } else if (trimmed.startsWith('data:')) {
              const jsonStr = trimmed.replace('data:', '').trim()
              if (jsonStr) {
                try {
                  eventData = JSON.parse(jsonStr)
                } catch (e) {
                  console.warn("Falha ao decodificar JSON do bloco SSE:", jsonStr)
                }
              }
            }
          }
          
          if (eventData) {
            if (eventType === 'message') {
              this.streamingContent += eventData.content
              const lastMsg = this.messages[this.messages.length - 1]
              if (lastMsg && lastMsg.role === 'assistant') {
                lastMsg.content = this.streamingContent
              }
            } else if (eventType === 'done') {
              this.messages.pop() // remove o temporário
              this.messages.push(eventData) // insere o modelo oficial do DB
              this.streamingContent = ''
              this.fetchConversations() // Atualiza sidebar
            } else if (eventType === 'error') {
              throw new Error(eventData.detail || "Erro desconhecido na stream do LLM")
            }
          }
        }

        while (true) {
          const { value, done } = await reader.read()
          if (value) {
            buffer += decoder.decode(value, { stream: true })
          }
          
          const blocks = buffer.split(/\r?\n\r?\n/)
          buffer = blocks.pop() // mantém o último bloco incompleto no buffer
          
          for (const block of blocks) {
            if (block.trim()) {
              processBlock(block)
            }
          }
          
          if (done) {
            // Processa o resíduo do buffer se houver
            if (buffer.trim()) {
              processBlock(buffer)
            }
            break
          }
        }
      } catch (error) {
        console.error("Erro no envio de mensagem:", error)
        // Sobrescreve o placeholder com a mensagem de erro
        const lastMsg = this.messages[this.messages.length - 1]
        if (lastMsg && lastMsg.role === 'assistant') {
          lastMsg.content = `[JanjIA encontrou um obstáculo cósmico: ${error.message}. Talvez os jacarés tenham desligado o roteador.]`
        }
      } finally {
        this.isStreaming = false
      }
    }
  }
})
