import { defineStore } from 'pinia'
import api from '../utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.is_admin || false
  },
  
  actions: {
    async register(username, email, password) {
      await api.post('/auth/register', { username, email, password })
    },
    
    async login(username, password) {
      const response = await api.post('/auth/login-json', { username, password })
      const { access_token, refresh_token } = response.data
      
      this.token = access_token
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      
      await this.fetchUser()
    },
    
    async fetchUser() {
      try {
        const response = await api.get('/auth/me')
        this.user = response.data
      } catch (error) {
        this.logout()
        throw error
      }
    },
    
    async restoreSession() {
      if (!this.token) return false
      try {
        await this.fetchUser()
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }
})
