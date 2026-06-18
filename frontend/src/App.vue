<template>
  <div class="h-full font-sans antialiased text-slate-900 bg-slate-50 dark:bg-darkbg-chat dark:text-slate-100 transition-colors duration-200">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // Inicializa o tema preferido do usuário ou o padrão do sistema
  const isDark = 
    localStorage.theme === 'dark' || 
    (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
    
  if (isDark) {
    document.documentElement.classList.add('dark')
    localStorage.theme = 'dark'
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.theme = 'light'
  }
})
</script>

<style>
/* Força que o container ocupe toda a altura */
#app {
  height: 100%;
}
</style>
