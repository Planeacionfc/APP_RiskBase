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
   # --- Credenciales de la base de datos ---
   DB_SERVER=TU_SERVIDOR_SQL           # Nombre o IP del servidor SQL
   DATABASE=TU_BASE_DE_DATOS           # Nombre de la base de datos
   DB_USER=TU_USUARIO_SQL              # Usuario de la base de datos SQL
   DB_PASSWORD=TU_PASSWORD_SQL         # Contraseña del usuario de la base de datos SQL

   # --- Credenciales de SAP BI ---
   ASHOST=TU_HOST_SAP                  # Host o dirección del servidor SAP
   SYSNR=00                            # Número de sistema SAP 
   CLIENT=000                          # Número de cliente SAP 
   USER_SAP=TU_USUARIO_SAP             # Usuario de SAP
   PASSWORD_SAP=TU_PASSWORD_SAP        # Contraseña del usuario SAP

   # --- Configuración del API ---
   API_HOST=tu_host                    # Host donde se ejecuta la API (por ejemplo, localhost)
   API_PORT=tu_puerto                  # Puerto donde se ejecuta la API (por ejemplo, 8000)
   TEMP_DIR=./temp                     # Ruta de la carpeta temporal donde se alojan los archivos de Excel

   # --- Credenciales de autenticación JWT ---
   SECRET_KEY=tu_clave_secreta_segura  # Clave secreta para firmar los tokens JWT
   ALGORITHM=HS256                     # Algoritmo de cifrado para JWT (por ejemplo, HS256)
   ACCESS_TOKEN_EXPIRE_MINUTES=30      # Tiempo de expiración del token de acceso en minutos
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

1. Cambiar el archivo .env con las siguientes variables en el backend:

   ```
      API_HOST=0.0.0.0 o IP del servidor
      API_PORT=puerto del backend
   ```

2. Configurar CORS en FastAPI:
   En el archivo principal (main.py), asegurarse de que los orígenes permitidos incluyan la IP y puerto del frontend:

   ```
   app.add_middleware(
      CORSMiddleware,
      allow_origins=[
         "http://<IP del servidor>:<puerto del frontend>",
      ],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
   )
   ```

3. Iniciar el servidor de producción:
   ```bash
   uvicorn riskbase.main:app --host <IP del servidor> --port <puerto del backend>
   ```


