from django.shortcuts import render, redirect
from django.contrib import messages
import requests

API_URL = 'http://127.0.0.1:5000/productos'

def listar_productos(request):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            productos = response.json()
        else:
            productos = []
            messages.error(request, 'Error al obtener los productos')
    except requests.exceptions.RequestException:
        productos = []
        messages.error(request, 'No se pudo conectar con la API')
    
    return render(request, 'inventario/listar.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        producto = {
            'nombre': request.POST.get('nombre'),
            'categoria': request.POST.get('categoria'),
            'descripcion': request.POST.get('descripcion'),
            'precio': request.POST.get('precio'),
            'stock': request.POST.get('stock'),
            'fecha_vencimiento': request.POST.get('fecha_vencimiento', '')
        }
        
        try:
            response = requests.post(API_URL, json=producto)
            if response.status_code == 201:
                messages.success(request, 'Producto creado exitosamente')
                return redirect('listar_productos')
            else:
                error = response.json().get('error', 'Error al crear el producto')
                messages.error(request, error)
        except requests.exceptions.RequestException:
            messages.error(request, 'No se pudo conectar con la API')
    
    return render(request, 'inventario/crear.html')

def editar_producto(request, producto_id):
    if request.method == 'GET':
        try:
            response = requests.get(f'{API_URL}/{producto_id}')
            if response.status_code == 200:
                producto = response.json()
            else:
                messages.error(request, 'Producto no encontrado')
                return redirect('listar_productos')
        except requests.exceptions.RequestException:
            messages.error(request, 'No se pudo conectar con la API')
            return redirect('listar_productos')
        
        return render(request, 'inventario/editar.html', {'producto': producto})
    
    elif request.method == 'POST':
        producto = {
            'nombre': request.POST.get('nombre'),
            'categoria': request.POST.get('categoria'),
            'descripcion': request.POST.get('descripcion'),
            'precio': request.POST.get('precio'),
            'stock': request.POST.get('stock'),
            'fecha_vencimiento': request.POST.get('fecha_vencimiento', '')
        }
        
        try:
            response = requests.put(f'{API_URL}/{producto_id}', json=producto)
            if response.status_code == 200:
                messages.success(request, 'Producto actualizado exitosamente')
                return redirect('listar_productos')
            else:
                error = response.json().get('error', 'Error al actualizar el producto')
                messages.error(request, error)
        except requests.exceptions.RequestException:
            messages.error(request, 'No se pudo conectar con la API')
        
        return redirect('editar_producto', producto_id=producto_id)

def eliminar_producto(request, producto_id):
    try:
        response = requests.delete(f'{API_URL}/{producto_id}')
        if response.status_code == 200:
            messages.success(request, 'Producto eliminado exitosamente')
        else:
            messages.error(request, 'Error al eliminar el producto')
    except requests.exceptions.RequestException:
        messages.error(request, 'No se pudo conectar con la API')
    
    return redirect('listar_productos')

def detalle_producto(request, producto_id):
    try:
        response = requests.get(f'{API_URL}/{producto_id}')
        if response.status_code == 200:
            producto = response.json()
        else:
            messages.error(request, 'Producto no encontrado')
            return redirect('listar_productos')
    except requests.exceptions.RequestException:
        messages.error(request, 'No se pudo conectar con la API')
        return redirect('listar_productos')
    
    return render(request, 'inventario/detalle.html', {'producto': producto})
