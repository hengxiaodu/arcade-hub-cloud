import unittest
import requests

BASE_URL = "http://localhost:5000/api/games"
API_KEY = "secreto_super_seguro_123"
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

class TestGamesAPI(unittest.TestCase):

    def test_01_get_games_public(self):
        """Verifica que el GET sea público y devuelva una lista (HTTP 200)."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_02_create_unauthorized(self):
        """Verifica que crear sin cabecera X-API-Key devuelva HTTP 401."""
        body = {"title": "Intento Ilegal", "genre": "Accion"}
        response = requests.post(BASE_URL, json=body)
        self.assertEqual(response.status_code, 401)

    def test_03_crud_workflow(self):
        """Prueba de integración: crear, verificar, editar y eliminar un juego."""
        # 1. Crear juego
        nuevo_juego = {
            "title": "Hollow Knight",
            "genre": "Metroidvania",
            "platform": "PC / Consolas",
            "rating": 9.7,
            "image_url": "https://dummyimage.com/300x180/000/fff&text=HollowKnight"
        }
        res_post = requests.post(BASE_URL, json=nuevo_juego, headers=HEADERS)
        self.assertEqual(res_post.status_code, 201)
        juego_creado = res_post.json()
        game_id = juego_creado["id"]
        self.assertEqual(juego_creado["title"], "Hollow Knight")

        # 2. Consultar el juego recién creado
        res_get = requests.get(f"{BASE_URL}/{game_id}")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["title"], "Hollow Knight")

        # 3. Editar juego
        datos_editados = {
            "title": "Hollow Knight: Silksong",
            "genre": "Metroidvania",
            "platform": "PC / Switch",
            "rating": 10.0,
            "image_url": "https://dummyimage.com/300x180/000/fff&text=Silksong"
        }
        res_put = requests.put(f"{BASE_URL}/{game_id}", json=datos_editados, headers=HEADERS)
        self.assertEqual(res_put.status_code, 200)
        self.assertEqual(res_put.json()["title"], "Hollow Knight: Silksong")

        # 4. Eliminar juego
        res_del = requests.delete(f"{BASE_URL}/{game_id}", headers=HEADERS)
        self.assertEqual(res_del.status_code, 200)

        # 5. Confirmar que ya no existe (404)
        res_verify = requests.get(f"{BASE_URL}/{game_id}")
        self.assertEqual(res_verify.status_code, 404)

if __name__ == "__main__":
    unittest.main(verbosity=2)