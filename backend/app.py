# Backend Flask - API REST para gestión de productos
# Práctica 3 - Sistema de Gestión de Inventario
# Curso: Introducción a la Programación y Computación 2

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde Django

# Archivo JSON para almacenar los productos
INVENTARIO_FILE = 'inventario.json'

# Función para leer el inventario desde el archivo JSON
def leer_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        return []
    try:
        with open(INVENTARIO_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

# Función para guardar el inventario en el archivo JSON
def guardar_inventario(productos):
    with open(INVENTARIO_FILE, 'w', encoding='utf-8') as file:
        json.dump(productos, file, ensure_ascii=False, indent=4)

# Ruta de prueba
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'mensaje': 'API REST de Gestión de Inventario',
        'version': '1.0',
        'endpoints': {
            'GET /productos': 'Listar todos los productos',
            'GET /productos/<id>': 'Obtener un producto específico',
            'POST /productos': 'Crear un nuevo producto',
            'PUT /productos/<id>': 'Actualizar un producto',
            'DELETE /productos/<id>': 'Eliminar un producto'
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
