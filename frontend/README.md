# Frontend Django - Sistema de Gestión de Inventario

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
```

2. Activar el entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar las migraciones:
```bash
python manage.py migrate
```

5. Ejecutar la aplicación:
```bash
python manage.py runserver
```

La aplicación estará disponible en: http://localhost:8000

## Nota Importante

Asegúrate de que la API Flask esté corriendo en http://localhost:5000 antes de usar la aplicación Django.
