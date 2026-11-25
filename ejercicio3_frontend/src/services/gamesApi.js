import axios from 'axios'

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
const http = axios.create({ baseURL: `${API_URL}/api` })

// La clave se guarda en sessionStorage y solo se envía en POST, PUT y DELETE
http.interceptors.request.use((config) => {
  const key = sessionStorage.getItem('apiKey')
  if (key && config.method !== 'get' && !config.headers['X-API-Key']) {
    config.headers['X-API-Key'] = key
  }
  return config
})

export const apiKey = {
  get: () => sessionStorage.getItem('apiKey') || '',
  set: (k) => sessionStorage.setItem('apiKey', k),
  clear: () => sessionStorage.removeItem('apiKey'),
}

// Comprueba si una API Key es válida sin modificar nada en la BBDD:
// un DELETE sobre el id 0 (que no existe) devuelve 404 con clave válida y 401 con clave incorrecta.
export async function verifyKey(key) {
  const res = await http.delete('/games/0', {
    headers: { 'X-API-Key': key },
    validateStatus: () => true,
  })
  return res.status !== 401
}

export const gamesApi = {
  // el backend devuelve rating como texto ("8.5"), lo pasamos a número
  list: () => http.get('/games').then((r) => r.data.map((g) => ({ ...g, rating: Number(g.rating) }))),
  create: (game) => http.post('/games', game).then((r) => r.data),
  update: (id, game) => http.put(`/games/${id}`, game).then((r) => r.data),
  remove: (id) => http.delete(`/games/${id}`).then((r) => r.data),
}

export function errorMessage(e) {
  if (!e.response) return 'No se puede conectar con el servidor.'
  return e.response.data?.error || `Error ${e.response.status}`
}
