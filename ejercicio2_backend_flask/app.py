import os
import psycopg
from psycopg.rows import dict_row
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
# Habilita CORS para permitir peticiones desde Vue
CORS(app)

# API Key definida para operaciones protegidas (crear, editar, eliminar)
API_KEY = os.getenv("API_KEY", "secreto_super_seguro_123")

# Configuración directa de PostgreSQL
DB_CONFIG = {
    "dbname": "distribuida_db",
    "user": "postgres",
    "password": "duhengxiao2006",  
    "host": "localhost",
    "port": 5432                     
}

def get_db_connection():
    """Establece conexión con PostgreSQL devolviendo registros como diccionarios."""
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)

def require_api_key(f):
    """Decorador para proteger rutas mediante cabecera X-API-Key."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("X-API-Key")
        if not token or token != API_KEY:
            return jsonify({
                "error": "Acceso no autorizado: X-API-Key ausente o no válida"
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------
# 1. LISTAR JUEGOS (Abierto a cualquier usuario)
# -------------------------------------------------------------
@app.route("/api/games", methods=["GET"])
def get_games():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM games ORDER BY id ASC;")
                games = cur.fetchall()
        return jsonify(games), 200
    except Exception as e:
        return jsonify({"error": f"Error al consultar la base de datos: {str(e)}"}), 500

# -------------------------------------------------------------
# 2. OBTENER UN JUEGO POR ID (Abierto)
# -------------------------------------------------------------
@app.route("/api/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM games WHERE id = %s;", (game_id,))
                game = cur.fetchone()

        if not game:
            return jsonify({"error": "Juego no encontrado"}), 404
        return jsonify(game), 200
    except Exception as e:
        return jsonify({"error": f"Error en la consulta: {str(e)}"}), 500

# -------------------------------------------------------------
# 3. AÑADIR JUEGO (Protegido por API Key)
# -------------------------------------------------------------
@app.route("/api/games", methods=["POST"])
@require_api_key
def create_game():
    data = request.get_json()
    if not data or not data.get("title") or not data.get("genre"):
        return jsonify({"error": "Los campos 'title' y 'genre' son obligatorios"}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    INSERT INTO games (title, genre, platform, rating, image_url)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *;
                """
                cur.execute(query, (
                    data["title"],
                    data["genre"],
                    data.get("platform", "Multiplataforma"),
                    data.get("rating", 0.0),
                    data.get("image_url", "")
                ))
                new_game = cur.fetchone()
                conn.commit()
        return jsonify(new_game), 201
    except Exception as e:
        return jsonify({"error": f"Error al insertar juego: {str(e)}"}), 500

# -------------------------------------------------------------
# 4. EDITAR JUEGO (Protegido por API Key)
# -------------------------------------------------------------
@app.route("/api/games/<int:game_id>", methods=["PUT"])
@require_api_key
def update_game(game_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requieren datos para actualizar"}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    UPDATE games
                    SET title = %s, genre = %s, platform = %s, rating = %s, image_url = %s
                    WHERE id = %s
                    RETURNING *;
                """
                cur.execute(query, (
                    data.get("title"),
                    data.get("genre"),
                    data.get("platform", "Multiplataforma"),
                    data.get("rating", 0.0),
                    data.get("image_url", ""),
                    game_id
                ))
                updated_game = cur.fetchone()
                conn.commit()

        if not updated_game:
            return jsonify({"error": "Juego no encontrado"}), 404
        return jsonify(updated_game), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar juego: {str(e)}"}), 500

# -------------------------------------------------------------
# 5. ELIMINAR JUEGO (Protegido por API Key)
# -------------------------------------------------------------
@app.route("/api/games/<int:game_id>", methods=["DELETE"])
@require_api_key
def delete_game(game_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM games WHERE id = %s RETURNING id;", (game_id,))
                deleted = cur.fetchone()
                conn.commit()

        if not deleted:
            return jsonify({"error": "Juego no encontrado"}), 404
        return jsonify({"message": f"Juego con ID {game_id} eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar juego: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)