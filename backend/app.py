from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

INVENTARIO_FILE = 'inventario.json'

def leer_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        return []
    try:
        with open(INVENTARIO_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def guardar_inventario(productos):
    with open(INVENTARIO_FILE, 'w', encoding='utf-8') as file:
        json.dump(productos, file, ensure_ascii=False, indent=4)

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

@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = leer_inventario()
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    try:
        productos = leer_inventario()
        producto = next((p for p in productos if p['id'] == producto_id), None)
        
        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        datos = request.get_json()
        
        campos_requeridos = ['nombre', 'categoria', 'descripcion', 'precio', 'stock']
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                return jsonify({'error': f'El campo {campo} es requerido'}), 400
        
        try:
            precio = float(datos['precio'])
            stock = int(datos['stock'])
            if precio < 0 or stock < 0:
                return jsonify({'error': 'El precio y stock deben ser valores positivos'}), 400
        except ValueError:
            return jsonify({'error': 'Precio y stock deben ser valores numéricos'}), 400
        
        productos = leer_inventario()
        nuevo_id = max([p['id'] for p in productos], default=0) + 1
        
        nuevo_producto = {
            'id': nuevo_id,
            'nombre': datos['nombre'].strip(),
            'categoria': datos['categoria'].strip(),
            'descripcion': datos['descripcion'].strip(),
            'precio': precio,
            'stock': stock,
            'fecha_vencimiento': datos.get('fecha_vencimiento', '').strip()
        }
        
        productos.append(nuevo_producto)
        guardar_inventario(productos)
        
        return jsonify({'mensaje': 'Producto creado exitosamente', 'producto': nuevo_producto}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    try:
        datos = request.get_json()
        productos = leer_inventario()
        
        indice = next((i for i, p in enumerate(productos) if p['id'] == producto_id), None)
        
        if indice is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        if 'precio' in datos:
            try:
                precio = float(datos['precio'])
                if precio < 0:
                    return jsonify({'error': 'El precio debe ser un valor positivo'}), 400
                datos['precio'] = precio
            except ValueError:
                return jsonify({'error': 'El precio debe ser un valor numérico'}), 400
        
        if 'stock' in datos:
            try:
                stock = int(datos['stock'])
                if stock < 0:
                    return jsonify({'error': 'El stock debe ser un valor positivo'}), 400
                datos['stock'] = stock
            except ValueError:
                return jsonify({'error': 'El stock debe ser un valor numérico'}), 400
        
        if 'nombre' in datos:
            productos[indice]['nombre'] = datos['nombre'].strip()
        if 'categoria' in datos:
            productos[indice]['categoria'] = datos['categoria'].strip()
        if 'descripcion' in datos:
            productos[indice]['descripcion'] = datos['descripcion'].strip()
        if 'precio' in datos:
            productos[indice]['precio'] = datos['precio']
        if 'stock' in datos:
            productos[indice]['stock'] = datos['stock']
        if 'fecha_vencimiento' in datos:
            productos[indice]['fecha_vencimiento'] = datos['fecha_vencimiento'].strip()
        
        guardar_inventario(productos)
        
        return jsonify({'mensaje': 'Producto actualizado exitosamente', 'producto': productos[indice]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    try:
        productos = leer_inventario()
        producto = next((p for p in productos if p['id'] == producto_id), None)
        
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        productos = [p for p in productos if p['id'] != producto_id]
        guardar_inventario(productos)
        
        return jsonify({'mensaje': 'Producto eliminado exitosamente', 'producto': producto}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
