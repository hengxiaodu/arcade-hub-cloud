<script setup>
import { ref } from 'vue'
import GameList from './components/GameList.vue'
import Wordle from './components/Wordle.vue'

const vistas = [
  { id: 'catalogo', etiqueta: 'Catálogo & Palabras Clave', icono: '📚', componente: GameList },
  { id: 'minijuego', etiqueta: 'Wordle', icono: '🎮', componente: Wordle }
]

const vistaActual = ref('catalogo')
</script>

<template>
  <div class="contenedor-principal">
    <header class="cabecera">
      <div class="logo-badge">PRACTICA 1B &bull; VUE.JS</div>
      <h1>Arcade Hub</h1>
      <p class="subtitulo">Explora los grandes clásicos del videojuego y juega en el navegador</p>

      <nav class="navegacion" aria-label="Navegación principal">
        <button
          v-for="vista in vistas"
          :key="vista.id"
          type="button"
          :class="{ activo: vistaActual === vista.id }"
          :aria-current="vistaActual === vista.id ? 'page' : undefined"
          @click="vistaActual = vista.id"
        >
          <span class="icon" aria-hidden="true">{{ vista.icono }}</span>
          {{ vista.etiqueta }}
        </button>
      </nav>
    </header>

    <main class="area-contenido">
      <!-- key fuerza a reiniciar la animación al cambiar de vista -->
      <component
        :is="vistas.find(v => v.id === vistaActual).componente"
        :key="vistaActual"
      />
    </main>
  </div>
</template>

<style>
/* Estilos globales y reset moderno */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 40%, #020617 100%);
  background-attachment: fixed;
  color: #f8fafc;
  min-height: 100vh;
  min-height: 100dvh;
}
</style>

<style scoped>
.contenedor-principal {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1.25rem;
}

.cabecera {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #a855f7;
  background: rgba(168, 85, 247, 0.12);
  border: 1px solid rgba(168, 85, 247, 0.3);
  padding: 0.3rem 0.8rem;
  border-radius: 9999px;
  margin-bottom: 0.75rem;
}

.cabecera h1 {
  margin: 0;
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #ffffff 40%, #c084fc 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitulo {
  color: #94a3b8;
  margin: 0.6rem 0 2rem 0;
  font-size: 1.05rem;
}

.navegacion {
  display: inline-flex;
  flex-wrap: wrap;
  justify-content: center;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(12px);
  padding: 0.35rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
  gap: 0.35rem;
}

.navegacion button {
  padding: 0.65rem 1.4rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 600;
  color: #94a3b8;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.navegacion button:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

.navegacion button:focus-visible {
  outline: 2px solid #c084fc;
  outline-offset: 2px;
}

.navegacion button.activo {
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(168, 85, 247, 0.35);
}

.area-contenido {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>