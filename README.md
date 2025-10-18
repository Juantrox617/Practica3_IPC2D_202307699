# Practica3_IPC2D_202307699

Sistema de Gestión de Inventario con Django y Flask

## Descripción

Aplicación web completa para gestionar el inventario de un supermercado. El sistema está dividido en dos partes:

- **Backend (Flask)**: API REST que gestiona los productos en un archivo JSON
- **Frontend (Django)**: Interfaz web que consume la API y permite realizar operaciones CRUD


## Instalación y Ejecución

### 1. Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```



### 2. Frontend (Django)

```bash
cd frontend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```



## Endpoints de la API

- `GET /productos` - Listar todos los productos
- `GET /productos/<id>` - Obtener un producto específico
- `POST /productos` - Crear un nuevo producto
- `PUT /productos/<id>` - Actualizar un producto
- `DELETE /productos/<id>` - Eliminar un producto

## Tecnologías Utilizadas

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: Python, Django, Requests
- **Base de Datos**: JSON (inventario.json)

## Autor

Juan - 202307699  
Universidad San Carlos de Guatemala  
Facultad de Ingeniería  
Ingeniería en Ciencias y Sistemas
