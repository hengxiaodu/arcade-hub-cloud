<script setup>
import { ref, computed, onMounted } from 'vue'
import { gamesApi, apiKey, errorMessage } from '../services/gamesApi'
import GameCard from '../components/GameCard.vue'
import GameForm from '../components/GameForm.vue'

const games = ref([])
const loading = ref(false)
const error = ref('')
const info = ref('')
const editing = ref(null) // juego que se está editando (null = añadiendo)

// "Modo administrador": hay API Key guardada
const keyInput = ref('')
const admin = ref(!!apiKey.get())

async function loadGames() {
  loading.value = true
  error.value = ''
  try {
    games.value = await gamesApi.list()
  } catch (e) {
    error.value = errorMessage(e)
  } finally {
    loading.value = false
  }
}

function enterAdmin() {
  if (!keyInput.value.trim()) return
  apiKey.set(keyInput.value.trim())
  admin.value = true
  keyInput.value = ''
}

function exitAdmin() {
  apiKey.clear()
  admin.value = false
  editing.value = null
}

// Ejecuta una operación protegida y gestiona los errores (incluido el 401)
async function run(action, okMessage) {
  error.value = ''
  info.value = ''
  try {
    await action()
    info.value = okMessage
    await loadGames() // recargamos desde la BBDD para ver el estado real
  } catch (e) {
    if (e.response?.status === 401) {
      exitAdmin()
      error.value = 'API Key incorrecta. Vuelve a introducirla.'
    } else {
      error.value = errorMessage(e)
    }
  }
}

function saveGame(data) {
  if (editing.value) {
    const id = editing.value.id
    return run(async () => {
      await gamesApi.update(id, data)
      editing.value = null
    }, 'Juego actualizado.')
  }
  return run(() => gamesApi.create(data), 'Juego añadido.')
}

function removeGame(game) {
  if (!confirm(`¿Eliminar "${game.title}"?`)) return
  run(() => gamesApi.remove(game.id), 'Juego eliminado.')
}

const empty = computed(() => !loading.value && !error.value && games.value.length === 0)

onMounted(loadGames)
</script>

<template>
  <main class="container">
    <h1>Videojuegos</h1>

    <!-- Acceso de administrador (API Key) -->
    <section class="admin-bar">
      <template v-if="!admin">
        <form @submit.prevent="enterAdmin">
          <input v-model="keyInput" type="password" placeholder="API Key para editar" />
          <button>Entrar</button>
        </form>
      </template>
      <template v-else>
        <span>Modo administrador activo</span>
        <button class="secondary" @click="exitAdmin">Salir</button>
      </template>
    </section>

    <p v-if="info" class="message ok">{{ info }}</p>
    <p v-if="error" class="message error">{{ error }}</p>
    <p v-if="loading" class="message">Cargando...</p>
    <p v-if="empty" class="message">Todavía no hay juegos. Añade el primero.</p>

    <section class="grid">
      <GameCard
        v-for="g in games"
        :key="g.id"
        :game="g"
        :admin="admin"
        @edit="editing = $event"
        @remove="removeGame"
      />
    </section>

    <GameForm
      v-if="admin"
      :game="editing"
      @save="saveGame"
      @cancel="editing = null"
    />
  </main>
</template>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}
h1 {
  text-align: center;
}
.admin-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.admin-bar form {
  display: flex;
  gap: 0.5rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.message {
  text-align: center;
}
.ok {
  color: #047857;
}
.error {
  color: #dc2626;
}
</style>
