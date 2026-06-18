import axios from 'axios'

// A URL da API aponta para o proxy Nginx
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepta todas as requisições para anexar o token de acesso
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Intercepta respostas para tratar erros 401 (token expirado) e tentar o refresh automático
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    // Se receber 401, tenta renovar o token apenas se não for uma tentativa de login ou refresh
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== '/auth/login-json' && originalRequest.url !== '/auth/refresh') {
      originalRequest._retry = true
      
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          // Faz requisição direta com axios comum para evitar loops de interceptores
          const response = await axios.post('/api/auth/refresh', {
            refresh_token: refreshToken
          })
          
          const { access_token, refresh_token: new_refresh_token } = response.data
          
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', new_refresh_token)
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        } catch (refreshError) {
          // Falha no refresh: desloga usuário limpando localStorage
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
