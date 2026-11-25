<script setup>
import { ref, watch } from 'vue'

const props = defineProps({ juego: { type: Object, default: null } })
const emit = defineEmits(['guardar', 'cancelar'])

const vacio = () => ({ title: '', genre: '', platform: '', rating: 0, image_url: '' })
const form = ref(vacio())

watch(() => props.juego, (j) => { form.value = j ? { ...j } : vacio() }, { immediate: true })

function enviar() {
  emit('guardar', { ...form.value, rating: Number(form.value.rating) || 0 })
  if (!props.juego) form.value = vacio()
}
</script>

<template>
  <form class="form-juego" @submit.prevent="enviar">
    <h3>{{ juego ? 'Editar juego' : 'Añadir juego' }}</h3>
    <label>Título <input v-model="form.title" required /></label>
    <label>Género <input v-model="form.genre" required /></label>
    <label>Plataforma <input v-model="form.platform" required /></label>
    <label>Nota (0-10) <input v-model="form.rating" type="number" min="0" max="10" step="0.1" /></label>
    <label class="ancho">URL de la imagen <input v-model="form.image_url" type="url" /></label>
    <div class="ancho botones">
      <button type="submit" class="btn">{{ juego ? 'Guardar cambios' : 'Añadir juego' }}</button>
      <button type="button" class="btn gris" @click="$emit('cancelar')">Cancelar</button>
    </div>
  </form>
</template>

<style scoped>
.form-juego { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.9rem;
  background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 12px; padding: 1.5rem; }
h3 { grid-column: 1 / -1; margin: 0; }
label { display: flex; flex-direction: column; gap: 0.3rem; font-size: 0.85rem; color: #94a3b8; }
.ancho { grid-column: 1 / -1; }
input { padding: 0.6rem 0.8rem; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: #fff; outline: none; }
input:focus { border-color: #a855f7; }
.botones { display: flex; gap: 0.6rem; }
.btn { padding: 0.65rem 1.3rem; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; color: #fff;
  background: linear-gradient(135deg, #6366f1, #a855f7); }
.btn.gris { background: #334155; }
</style>
