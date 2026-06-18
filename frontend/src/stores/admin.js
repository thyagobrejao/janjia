import { defineStore } from 'pinia'
import api from '../utils/api'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [],
    stats: null,
    loading: false
  }),
  
  actions: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await api.get('/admin/users')
        this.users = response.data
      } catch (error) {
        console.error("Erro ao carregar usuários administrativos:", error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchStats() {
      this.loading = true
      try {
        const response = await api.get('/admin/stats')
        this.stats = response.data
      } catch (error) {
        console.error("Erro ao carregar estatísticas do dashboard:", error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
