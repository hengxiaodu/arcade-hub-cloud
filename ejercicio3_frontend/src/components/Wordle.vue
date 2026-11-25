<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const DICCIONARIO = [
  'PLANO', 'JUEGO', 'PISTA', 'LUCES', 'DISCO', 'RADAR', 'FUEGO', 'MUNDO', 'LINEA', 'TORRE',
  'ARBOL', 'PLAYA', 'MONTE', 'CAMPO', 'SELVA', 'FLORA', 'FAUNA', 'PERRO', 'GATOS', 'OVEJA',
  'BURRO', 'RATON', 'CEBRA', 'TIGRE', 'LEONA', 'MOSCA', 'ABEJA', 'PULPO', 'LLAMA', 'COBRA',
  'LOBOS', 'PATOS', 'LIBRO', 'MESAS', 'SILLA', 'RELOJ', 'LLAVE', 'VASOS', 'PLATO', 'COPAS',
  'CABLE', 'MOTOR', 'RUEDA', 'RADIO', 'FOTOS', 'BOLSA', 'CAJAS', 'PAPEL', 'LAPIZ', 'MARCO',
  'PARED', 'TECHO', 'SUELO', 'CINTA', 'JARRA', 'CALLE', 'PLAZA', 'HOTEL', 'BANCO',
  'CASAS', 'ANDEN', 'BARCO', 'AVION', 'ISLAS', 'NORTE', 'SURCO', 'PANES', 'QUESO', 'CARNE',
  'ARROZ', 'PASTA', 'FRUTA', 'MELON', 'PERAS', 'TARTA', 'HUEVO', 'SALSA', 'CACAO', 'LIMON',
  'FRESA', 'OLIVA', 'CHILE', 'SOPAS', 'GENTE', 'AMIGO', 'MADRE', 'PADRE', 'HIJOS', 'MANOS',
  'PIEZA', 'BRAZO', 'DEDOS', 'BOCAS', 'NARIZ', 'LABIO', 'PECHO', 'MENTE', 'ANDAR', 'SALIR',
  'ENTRA', 'SUBIR', 'BAJAR', 'COMER', 'BEBER', 'VIVIR', 'BAILA', 'CORRE', 'JUGAR', 'MIRAR',
  'SABER', 'PODER', 'TENER', 'HACER', 'DECIR', 'VENIR', 'PONER', 'TRAER', 'CREER', 'PENSAR',
  'BUSCA', 'LLORA', 'TOCAR', 'VOLAR', 'BELLO', 'FELIZ', 'DULCE', 'VERDE', 'NEGRO', 'ROJOS',
  'CLARO', 'NUEVO', 'VIEJO', 'FACIL', 'CORTO', 'LARGO', 'ANCHO', 'BAJOS', 'IDEAS', 'MAGIA',
  'VALOR', 'HONOR', 'MIEDO', 'RISAS', 'ORDEN', 'ERROR', 'EXITO', 'CLAVE', 'SIGNO', 'FORMA',
  'COLOR', 'RUMBO', 'ETAPA', 'NIVEL', 'PUNTO', 'CICLO', 'RITMO', 'NOCHE', 'TARDE', 'CIELO',
  'NUBES', 'NIEVE', 'FAROL', 'METAL', 'ACERO', 'PLATA', 'MINAS', 'JOYAS', 'REINA', 'REYES',
  'DUQUE', 'MAGOS', 'HADAS', 'BRUJA', 'MONJE', 'SANTO', 'ANGEL', 'ALMAS', 'VIDAS', 'DESEO',
  'CALMA', 'GRITO', 'VOCES', 'NOTAS', 'CANTO', 'DANZA', 'BAILE', 'RIMAS', 'VERSO', 'POEMA',
  'TEXTO', 'FRASE', 'LETRA', 'DATOS', 'CIFRA', 'REGLA', 'NORMA', 'FIRMA', 'SELLO',
  'CARGO', 'RENTA', 'PAGAR', 'GASTO', 'DEUDA', 'COSTE', 'EUROS', 'RUINA',
  'POBRE', 'LISTO', 'SABIO', 'TONTO', 'TORPE', 'SERIO', 'GRAVE', 'FALSO', 'JUSTO',
  'LEGAL', 'MORAL', 'SOCIO', 'LOCAL', 'TOTAL', 'PARTE', 'RESTO', 'MITAD', 'DOBLE', 'UNICO',
  'IGUAL', 'CERCA', 'LEJOS', 'ATRAS', 'ANTES', 'LUEGO', 'NUNCA', 'QUIZA', 'JAMAS', 'OTROS',
  'AMBOS', 'QUIEN', 'DONDE', 'ENTRE', 'HASTA', 'DESDE', 'SOBRE', 'SEGUN', 'MEDIO', 'LLENO',
  'SUCIO', 'CALOR', 'SUAVE', 'TENSO', 'FLOJO', 'CREAR', 'NACER', 'MORIR',
  'ABRIR', 'TAPAR', 'TIRAR', 'LANZA', 'COGER', 'TOMAR', 'DEJAR', 'PEDIR', 'ROBAR', 'MATAR',
  'SALVA', 'CURAR', 'SANAR', 'DOLER', 'TEMER', 'ODIAR', 'REZAR', 'LLORO', 'SALTO',
  'NADAR', 'PESCA', 'CAZAR', 'LUCHA', 'GANAR', 'BALON', 'PASES', 'RIVAL', 'LIGAS', 'TENIS',
  'MOTOS', 'COCHE', 'FRENO', 'MAPAS', 'OESTE', 'ZONAS', 'COSTA', 'VALLE', 'CERRO', 'LLANO',
  'PRADO', 'TRIGO', 'GRANO', 'RAMAS', 'HOJAS', 'ROBLE', 'OLMOS', 'CACTO', 'MUSGO', 'HONGO',
  'SETAS', 'FRUTO', 'TALLO', 'PODAR', 'REGAR', 'TODOS', 'VARIO', 'POCOS', 'MUCHO', 'MENOS',
  'BASTA', 'FALTA', 'SOBRA', 'NUEVE', 'SIETE', 'CINCO'
]

// Garantiza que todas las palabras secretas tengan exactamente cinco letras.
const PALABRAS_VALIDAS = [...new Set(DICCIONARIO.filter(p => /^[A-ZÑ]{5}$/.test(p)))]

const INTENTOS_MAX = 6
const LONGITUD_PALABRA = 5

const palabraSecreta = ref('')
const intentos = ref([])
const intentoActual = ref('')
const juegoTerminado = ref(false)
const mensaje = ref('')

let temporizadorAviso = null

function iniciarPartida() {
  const indice = Math.floor(Math.random() * PALABRAS_VALIDAS.length)
  palabraSecreta.value = PALABRAS_VALIDAS[indice]
  intentos.value = []
  intentoActual.value = ''
  juegoTerminado.value = false
  limpiarAviso()
}

// Algoritmo de dos pasadas: primero verdes, luego amarillos
// limitados a las letras que aún no se han "gastado".
function evaluarIntento(intento, secreta) {
  const resultado = Array(LONGITUD_PALABRA).fill('gris')
  const restantes = {}

  for (let i = 0; i < LONGITUD_PALABRA; i++) {
    if (intento[i] === secreta[i]) {
      resultado[i] = 'verde'
    } else {
      restantes[secreta[i]] = (restantes[secreta[i]] || 0) + 1
    }
  }

  for (let i = 0; i < LONGITUD_PALABRA; i++) {
    if (resultado[i] === 'verde') continue
    if (restantes[intento[i]] > 0) {
      resultado[i] = 'amarillo'
      restantes[intento[i]]--
    }
  }

  return resultado
}

const evaluaciones = computed(() =>
  intentos.value.map(intento => evaluarIntento(intento, palabraSecreta.value))
)

function obtenerEstadoLetra(filaIndex, colIndex) {
  return evaluaciones.value[filaIndex]?.[colIndex] ?? ''
}

// El teclado conserva el mejor resultado de cada letra:
// verde > amarillo > gris.
const PRIORIDAD = { gris: 1, amarillo: 2, verde: 3 }
const CLASE_TECLA = { gris: 'tecla-gris', amarillo: 'tecla-amarilla', verde: 'tecla-verde' }

const estadoTeclas = computed(() => {
  const mejor = {}
  intentos.value.forEach((intento, fila) => {
    ;[...intento].forEach((letra, col) => {
      const estado = evaluaciones.value[fila][col]
      if (!mejor[letra] || PRIORIDAD[estado] > PRIORIDAD[mejor[letra]]) {
        mejor[letra] = estado
      }
    })
  })
  return mejor
})

function obtenerEstadoTecla(letra) {
  const estado = estadoTeclas.value[letra]
  return estado ? CLASE_TECLA[estado] : ''
}

function presionarTecla(tecla) {
  if (juegoTerminado.value) return

  if (tecla === 'ENTER') {
    if (intentoActual.value.length < LONGITUD_PALABRA) {
      mostrarAviso('Completa las 5 letras')
      return
    }

    const intento = intentoActual.value
    intentos.value.push(intento)
    intentoActual.value = ''

    if (intento === palabraSecreta.value) {
      juegoTerminado.value = true
      mostrarAviso('¡Correcto! Has ganado 🎉')
    } else if (intentos.value.length === INTENTOS_MAX) {
      juegoTerminado.value = true
      mostrarAviso(`Fin del juego. Era: ${palabraSecreta.value}`)
    }
  } else if (tecla === 'BORRAR') {
    intentoActual.value = intentoActual.value.slice(0, -1)
  } else if (/^[A-ZÑ]$/.test(tecla)) {
    if (intentoActual.value.length < LONGITUD_PALABRA) {
      intentoActual.value += tecla
    }
  }
}

function limpiarAviso() {
  clearTimeout(temporizadorAviso)
  temporizadorAviso = null
  mensaje.value = ''
}

function mostrarAviso(texto) {
  clearTimeout(temporizadorAviso)
  mensaje.value = texto
  // Los avisos de fin de partida se quedan fijos
  if (!juegoTerminado.value) {
    temporizadorAviso = setTimeout(() => {
      mensaje.value = ''
    }, 2000)
  }
}

function manejarTecladoFisico(event) {
  if (event.ctrlKey || event.metaKey || event.altKey) return

  const tecla = event.key.toUpperCase()

  if (tecla === 'ENTER') {
    // Evita que un botón con foco dispare también su click
    event.preventDefault()
    presionarTecla('ENTER')
  } else if (tecla === 'BACKSPACE') {
    presionarTecla('BORRAR')
  } else if (/^[A-ZÑ]$/.test(tecla)) {
    presionarTecla(tecla)
  }
}

onMounted(() => {
  iniciarPartida()
  window.addEventListener('keydown', manejarTecladoFisico)
})

onUnmounted(() => {
  window.removeEventListener('keydown', manejarTecladoFisico)
  clearTimeout(temporizadorAviso)
})

const FILAS_TECLADO = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ'],
  ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BORRAR']
]
</script>

<template>
  <div class="wordle-container">
    <div class="wordle-header">
      <h2>Wordle Clásico</h2>
      <p class="instrucciones">Adivina la palabra oculta de 5 letras en 6 intentos</p>
    </div>

    <div class="zona-aviso" role="status" aria-live="polite">
      <div v-if="mensaje" class="banner-aviso">{{ mensaje }}</div>
    </div>

    <div class="rejilla">
      <div v-for="filaIdx in INTENTOS_MAX" :key="filaIdx" class="fila">
        <div
          v-for="colIdx in LONGITUD_PALABRA"
          :key="colIdx"
          class="casilla"
          :class="obtenerEstadoLetra(filaIdx - 1, colIdx - 1)"
        >
          <span v-if="filaIdx - 1 < intentos.length">
            {{ intentos[filaIdx - 1][colIdx - 1] }}
          </span>
          <span v-else-if="filaIdx - 1 === intentos.length">
            {{ intentoActual[colIdx - 1] || '' }}
          </span>
        </div>
      </div>
    </div>

    <div class="teclado">
      <div v-for="(fila, fIdx) in FILAS_TECLADO" :key="fIdx" class="teclado-fila">
        <button
          v-for="tecla in fila"
          :key="tecla"
          type="button"
          class="tecla-btn"
          :class="[
            { 'tecla-ancha': tecla === 'ENTER' || tecla === 'BORRAR' },
            tecla.length === 1 ? obtenerEstadoTecla(tecla) : ''
          ]"
          @click="presionarTecla(tecla)"
        >
          {{ tecla }}
        </button>
      </div>
    </div>

    <button
      v-if="juegoTerminado"
      type="button"
      class="btn-nueva-partida"
      @click="iniciarPartida"
    >
      Nueva Partida
    </button>
  </div>
</template>

<style scoped>
.wordle-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 480px;
  margin: 0 auto;
  padding: 1rem;
}

.wordle-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #f8fafc;
  text-align: center;
}

.instrucciones {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0.4rem 0 1rem;
  text-align: center;
}

/* Reserva el espacio del aviso para que la rejilla no "salte" */
.zona-aviso {
  min-height: 2.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.banner-aviso {
  background: #38bdf8;
  color: #0f172a;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.9rem;
}

.rejilla {
  display: grid;
  grid-template-rows: repeat(6, 1fr);
  gap: 6px;
  margin-bottom: 1.5rem;
}

.fila {
  display: grid;
  grid-template-columns: repeat(5, 48px);
  gap: 6px;
}

.casilla {
  width: 48px;
  height: 48px;
  box-sizing: border-box;
  border: 2px solid #334155;
  background: rgba(15, 23, 42, 0.6);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  text-transform: uppercase;
  border-radius: 6px;
}

.casilla.verde {
  background-color: #22c55e;
  border-color: #22c55e;
}

.casilla.amarillo {
  background-color: #eab308;
  border-color: #eab308;
}

.casilla.gris {
  background-color: #475569;
  border-color: #475569;
}

.teclado {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.teclado-fila {
  display: flex;
  justify-content: center;
  gap: 4px;
}

.tecla-btn {
  background: #334155;
  color: #f8fafc;
  border: none;
  border-radius: 4px;
  height: 46px;
  min-width: 30px;
  padding: 0 6px;
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.tecla-btn:hover {
  filter: brightness(1.12);
}

.tecla-ancha {
  min-width: 52px;
  font-size: 0.72rem;
  background: #1e293b;
}

.tecla-btn.tecla-verde {
  background-color: #22c55e;
  color: #fff;
}

.tecla-btn.tecla-amarilla {
  background-color: #eab308;
  color: #fff;
}

.tecla-btn.tecla-gris {
  background-color: #475569;
  color: #fff;
}

.btn-nueva-partida {
  margin-top: 1.5rem;
  padding: 0.75rem 1.6rem;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  border: none;
  border-radius: 8px;
  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
}

.tecla-btn:focus-visible,
.btn-nueva-partida:focus-visible {
  outline: 2px solid #c084fc;
  outline-offset: 2px;
}
</style>