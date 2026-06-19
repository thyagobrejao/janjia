import { createPinia, setActivePinia } from 'pinia'

const pinia = createPinia()

// Ativa o Pinia globalmente no exato momento em que este módulo é carregado.
// Isso é necessário porque imports estáticos do ES Modules são resolvidos
// ANTES de app.use(pinia) executar — e guards do router ou interceptors
// podem chamar useStore() nesse intervalo.
setActivePinia(pinia)

export default pinia
