# Lab03 — Django Quiz: Entregables

Proyecto Django (Laboratorio 03, Aplicaciones Empresariales) con la aplicación `quiz` (examnes, preguntas y opciones). Aquí se agrupan los archivos de entrega final.

## Requisitos

- Python 3.14+
- Django 5.2.17 (ver `requirements.txt`)

## Cómo levantar el proyecto

```bash
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activar el entorno virtual
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ubicarse en el directorio del proyecto
cd src

# 5. Aplicar migraciones
python manage.py migrate

# 6. Cargar datos de ejemplo
python manage.py seed

# 7. Ejecutar el servidor de desarrollo
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Acceso al panel de administración

- URL: `http://127.0.0.1:8000/admin/`
- Credenciales de ejemplo: usuario `admin`, contraseña `admin12345`

## Archivos incluidos

| Archivo | Descripción |
| --- | --- |
| `EVIDENCIA.md` | Documento de evidencia: justificación de tipos de campo, capturas/logs y casos de prueba |
| `requirements.txt` | Dependencias del proyecto |
| `README.md` | Este documento |