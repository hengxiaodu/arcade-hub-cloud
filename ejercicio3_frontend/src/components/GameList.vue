<script setup>
import { ref, computed, onMounted } from 'vue'
import { gamesApi, apiKey, errorMessage, verifyKey } from '../services/gamesApi'
import GameForm from './GameForm.vue'

// Los juegos vienen del backend (PostgreSQL), ya no hay array estático
const juegos = ref([])
const cargando = ref(false)
const error = ref('')
const aviso = ref('')

// Modo administrador: hay una API Key guardada
const admin = ref(!!apiKey.get())
const claveInput = ref('')
const mostrarForm = ref(false)
const editando = ref(null)
const imgFallidas = ref({}) // imágenes que no han podido cargarse

async function cargarJuegos() {
  cargando.value = true
  imgFallidas.value = {}
  error.value = ''
  try {
    juegos.value = await gamesApi.list()
  } catch (e) {
    error.value = errorMessage(e)
  } finally {
    cargando.value = false
  }
}

// Solo se activa el modo administrador si el backend acepta la clave
async function entrarAdmin() {
  const clave = claveInput.value.trim()
  if (!clave) return
  error.value = ''
  aviso.value = ''
  try {
    if (await verifyKey(clave)) {
      apiKey.set(clave)
      admin.value = true
      claveInput.value = ''
    } else {
      error.value = 'API Key incorrecta.'
    }
  } catch (e) {
    error.value = errorMessage(e)
  }
}

function salirAdmin() {
  apiKey.clear()
  admin.value = false
  cerrarForm()
}

function abrirNuevo() {
  editando.value = null
  mostrarForm.value = true
}

function editar(juego) {
  editando.value = juego
  mostrarForm.value = true
}

function cerrarForm() {
  editando.value = null
  mostrarForm.value = false
}

// Ejecuta una operación protegida, gestiona errores (incluido el 401) y recarga la lista
async function ejecutar(accion, mensajeOk) {
  error.value = ''
  aviso.value = ''
  try {
    await accion()
    aviso.value = mensajeOk
    await cargarJuegos() // recarga desde la BBDD
    return true
  } catch (e) {
    if (e.response?.status === 401) {
      salirAdmin()
      error.value = 'API Key incorrecta. Vuelve a introducirla.'
    } else {
      error.value = errorMessage(e)
    }
    return false
  }
}

async function guardarJuego(datos) {
  const ok = editando.value
    ? await ejecutar(() => gamesApi.update(editando.value.id, datos), 'Juego actualizado.')
    : await ejecutar(() => gamesApi.create(datos), 'Juego añadido.')
  if (ok) cerrarForm()
}

function eliminarJuego(juego) {
  if (!confirm(`¿Eliminar "${juego.title}"?`)) return
  ejecutar(() => gamesApi.remove(juego.id), 'Juego eliminado.')
}

onMounted(cargarJuegos)

// ---------- Búsqueda, orden y palabras clave (adaptado de la P1B) ----------
const busqueda = ref('')
const orden = ref('desc')

const juegosFiltrados = computed(() => {
  const query = busqueda.value.trim().toLowerCase()

  const filtrados = juegos.value.filter(j =>
    j.title.toLowerCase().includes(query) ||
    (j.genre || '').toLowerCase().includes(query) ||
    (j.platform || '').toLowerCase().includes(query)
  )

  return filtrados.sort((a, b) =>
    orden.value === 'asc' ? a.rating - b.rating : b.rating - a.rating
  )
})

// Keywords comunes: palabras de género/plataforma que aparecen en al menos 2 juegos
const keywords = computed(() => {
  const stopWords = new Set([
    'de', 'la', 'el', 'en', 'y', 'a', 'los', 'las', 'un', 'una',
    'con', 'para', 'por', 'que', 'su', 'al', 'del', 'cada', 'donde', 'dos', 'sin', 'antes', 'entre'
  ])

  const conteoPorJuego = new Map()

  juegosFiltrados.value.forEach(juego => {
    const limpio = `${juego.genre} ${juego.platform}`
      .toLowerCase()
      .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')

    // Set para contar la palabra solo 1 vez por cada juego
    const palabrasUnicasJuego = new Set(limpio.split(/\s+/))

    palabrasUnicasJuego.forEach(palabra => {
      if (palabra.length > 3 && !stopWords.has(palabra)) {
        conteoPorJuego.set(palabra, (conteoPorJuego.get(palabra) || 0) + 1)
      }
    })
  })

  // Si hay más de un juego visible, la palabra debe repetirse al menos en 2 juegos
  const umbralMinimo = juegosFiltrados.value.length > 1 ? 2 : 1

  return Array.from(conteoPorJuego.entries())
    .filter(([_, conteo]) => conteo >= umbralMinimo)
    .map(([palabra]) => palabra)
    .sort()
})
</script>

<template>
  <div class="catalogo-wrapper">
    <!-- Barra superior de búsqueda y orden -->
    <div class="barra-controles">
      <div class="input-contenedor">
        <span class="lupa">🔍</span>
        <input
          v-model="busqueda"
          type="text"
          placeholder="Buscar por título, género o plataforma..."
          class="input-busqueda"
        />
        <button v-if="busqueda" class="btn-limpiar" @click="busqueda = ''">✕</button>
      </div>

      <div class="control-orden">
        <label for="ordenNota">Ordenar:</label>
        <div class="select-custom">
          <select id="ordenNota" v-model="orden">
            <option value="desc">Nota: de mayor a menor</option>
            <option value="asc">Nota: de menor a mayor</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Acceso de administrador (API Key) -->
    <div class="admin-bar">
      <form v-if="!admin" class="admin-form" @submit.prevent="entrarAdmin">
        <input v-model="claveInput" type="password" placeholder="API Key para editar" class="input-clave" />
        <button type="submit" class="btn-admin">Entrar</button>
      </form>
      <template v-else>
        <span class="admin-activo">🔓 Modo administrador</span>
        <button type="button" class="btn-admin" @click="abrirNuevo">+ Añadir juego</button>
        <button type="button" class="btn-admin gris" @click="salirAdmin">Salir</button>
      </template>
    </div>

    <p v-if="aviso" class="mensaje ok">{{ aviso }}</p>
    <p v-if="error" class="mensaje error">{{ error }}</p>
    <p v-if="cargando" class="mensaje">Cargando juegos...</p>

    <!-- Grid de juegos -->
    <div v-if="juegosFiltrados.length > 0" class="juegos-grid">
      <article v-for="juego in juegosFiltrados" :key="juego.id" class="card">
        <div class="card-img-wrapper">
          <img
            v-if="juego.image_url && !imgFallidas[juego.id]"
            :src="juego.image_url"
            :alt="juego.title"
            class="card-imagen"
            @error="imgFallidas[juego.id] = true"
          />
          <div v-else class="sin-imagen">Sin imagen</div>
          <span class="badge-anio">★ {{ juego.rating.toFixed(1) }}</span>
        </div>

        <div class="card-contenido">
          <h3 class="card-titulo">{{ juego.title }}</h3>
          <p class="card-descripcion">{{ juego.genre }} · {{ juego.platform }}</p>

          <div v-if="admin" class="card-acciones">
            <button type="button" class="btn-admin" @click="editar(juego)">Editar</button>
            <button type="button" class="btn-admin peligro" @click="eliminarJuego(juego)">Eliminar</button>
          </div>
        </div>
      </article>
    </div>

    <div v-else-if="!cargando && !error" class="sin-resultados">
      <div class="icono-vacio">🕹️</div>
      <h3>No se encontraron coincidencias</h3>
      <p>Prueba con otro término de búsqueda o limpia el filtro.</p>
    </div>

    <!-- Formulario de añadir / editar (solo en modo administrador) -->
    <GameForm
      v-if="admin && mostrarForm"
      :juego="editando"
      @guardar="guardarJuego"
      @cancelar="cerrarForm"
    />

    <!-- Pie con keywords comunes reducidas -->
    <footer class="keywords-seccion">
      <div class="keywords-header">
        <h4>Palabras clave comunes</h4>
        <span class="keywords-counter">{{ keywords.length }} destacadas</span>
      </div>
      <div v-if="keywords.length > 0" class="keywords-contenedor">
        <span v-for="kw in keywords" :key="kw" class="kw-chip">
          #{{ kw }}
        </span>
      </div>
      <p v-else class="sin-keywords">No hay palabras clave comunes disponibles.</p>
    </footer>
  </div>
</template>

<style scoped>
.catalogo-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.barra-controles {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(8px);
  padding: 1rem 1.25rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.input-contenedor {
  position: relative;
  flex: 1 1 300px;
  display: flex;
  align-items: center;
}

.lupa {
  position: absolute;
  left: 0.9rem;
  font-size: 0.9rem;
  opacity: 0.6;
}

.input-busqueda {
  width: 100%;
  padding: 0.65rem 2.2rem 0.65rem 2.4rem;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.92rem;
  outline: none;
  transition: all 0.2s ease;
}

.input-busqueda:focus {
  border-color: #a855f7;
  box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2);
}

.btn-limpiar {
  position: absolute;
  right: 0.8rem;
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  font-size: 0.85rem;
}

.btn-limpiar:hover {
  color: #cbd5e1;
}

.control-orden {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.control-orden label {
  font-size: 0.88rem;
  color: #94a3b8;
}

.select-custom select {
  padding: 0.65rem 1rem;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.88rem;
  outline: none;
  cursor: pointer;
}

.select-custom select:focus {
  border-color: #a855f7;
}

.juegos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.card {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

.card:hover {
  transform: translateY(-4px);
  border-color: rgba(168, 85, 247, 0.4);
  box-shadow: 0 12px 25px -4px rgba(0, 0, 0, 0.5), 0 0 15px rgba(168, 85, 247, 0.15);
}

.card-img-wrapper {
  position: relative;
  width: 100%;
  height: 170px;
  overflow: hidden;
}

.card-imagen {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.card:hover .card-imagen {
  transform: scale(1.05);
}

.badge-anio {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(4px);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 700;
}

.card-contenido {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-titulo {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #f8fafc;
}

.card-descripcion {
  font-size: 0.9rem;
  color: #94a3b8;
  flex-grow: 1;
  line-height: 1.5;
  margin: 0;
}

.sin-resultados {
  text-align: center;
  padding: 3rem 1rem;
  background: rgba(30, 41, 59, 0.4);
  border-radius: 12px;
  border: 1px dashed #334155;
}

.icono-vacio {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.sin-resultados h3 {
  margin: 0 0 0.4rem 0;
  color: #e2e8f0;
}

.sin-resultados p {
  margin: 0;
  color: #64748b;
  font-size: 0.9rem;
}

.keywords-seccion {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.25rem;
}

.keywords-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.keywords-header h4 {
  margin: 0;
  font-size: 0.95rem;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.keywords-counter {
  font-size: 0.8rem;
  color: #64748b;
  background: #0f172a;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
}

.keywords-contenedor {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.kw-chip {
  background: rgba(99, 102, 241, 0.12);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.25);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  font-size: 0.82rem;
  font-family: monospace;
}

.sin-keywords {
  color: #64748b;
  font-size: 0.85rem;
  margin: 0;
}

/* ---------- Administración y conexión con la API ---------- */
.admin-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
}

.admin-form {
  display: flex;
  gap: 0.5rem;
}

.input-clave {
  padding: 0.6rem 0.9rem;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9rem;
  outline: none;
}

.input-clave:focus {
  border-color: #a855f7;
}

.admin-activo {
  color: #4ade80;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-admin {
  padding: 0.55rem 1.1rem;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: #ffffff;
  font-family: inherit;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
}

.btn-admin.gris {
  background: #334155;
}

.btn-admin.peligro {
  background: #dc2626;
}

.btn-admin:hover {
  filter: brightness(1.12);
}

.mensaje {
  text-align: center;
  margin: 0;
  color: #94a3b8;
}

.mensaje.ok {
  color: #4ade80;
}

.mensaje.error {
  color: #f87171;
}

.sin-imagen {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: #0f172a;
  color: #64748b;
  font-size: 0.9rem;
}

.card-acciones {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}
</style>
