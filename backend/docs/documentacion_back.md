# Documentación del Backend

## Estructura del Proyecto

```
backend/
├── core/                  # Configuración principal del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Archivo de configuración principal
│   ├── urls.py           # Configuración principal de URLs
│   └── wsgi.py
├── riskbase/             # Aplicación principal
│   ├── api/
│   │   ├── routes/       # Puntos finales de la API
│   │   │   ├── auth.py
│   │   │   └── risk_process.py
│   │   └── dependencies.py
│   ├── domain/           # Lógica de negocio
│   │   ├── models/       # Modelos de la base de datos
│   │   ├── auth.py       # Lógica de autenticación
│   │   ├── entities.py   # Entidades de negocio
│   │   └── rules.py      # Reglas de negocio
│   ├── services/         # Servicios de la aplicación
│   ├── admin.py         # Configuración del administrador de Django
│   ├── apps.py          # Configuración de la aplicación
│   └── serializers.py   # Serializadores de la API
├── tests/               # Archivos de pruebas
├── manage.py            # Script de gestión de Django
└── requirements.txt     # Dependencias de Python
```

## Comenzando

### Requisitos Previos
- Python 3.8 o superior
- FastAPI
- SQL Server

### Instalación

1. Clonar el repositorio
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows: venv\Scripts\activate
   # En Unix/Mac: source venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar las variables de entorno en el archivo `.env`:
   ```
   DEBUG=True
   SECRET_KEY=tu-clave-secreta
   DATABASE_URL=tu-base-de-datos
   ```

5. Iniciar el servidor de desarrollo:
   ```bash
   python run.py
   ```

## Documentación de la API

### Autenticación
- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Inicio de sesión de usuario

### Gestión de Riesgos
- `POST /risk/process` - Procesar Riskbase
- `POST /risk/consult-riskbase` - Consultar Riskbase
- `GET /risk/data-view` - Obtener datos de riesgo
- `GET /risk/export-excel` - Exportar a Excel
- `POST /risk/save-to-db` - Guardar en base de datos
- `GET /risk/matrices-view` - Obtener matrices
- `PUT /risk/matrices-save` - Actualizar matrices
- `DELETE /risk/delete-temp-file` - Eliminar archivo temporal
- `DELETE /api/risk-process/{id}/` - Eliminar proceso de riesgo

## Despliegue en Producción

1. Crear un archivo .env con las siguientes variables en el backend:
     API_HOST=0.0.0.0 o IP del servidor
     API_PORT=8000
     TEMP_DIR=/ruta/absoluta/a/temp
     DB_USER=usuario
     DB_PASSWORD=contraseña
     DB_SERVER=servidor_sql
     DATABASE=nombre_db

2. Configurar CORS en FastAPI:
En el archivo principal (main.py), asegurarse de que los orígenes permitidos incluyan la IP y puerto del frontend:

   app.add_middleware(
      CORSMiddleware,
      allow_origins=[
         "http://<IP del servidor>:<puerto del frontend>",
      ],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
   )

3. Iniciar el servidor de producción:
   ```bash
   uvicorn riskbase.main:app --host <IP del servidor> --port <puerto del backend>
   ```


