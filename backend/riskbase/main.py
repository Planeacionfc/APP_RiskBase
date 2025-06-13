from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from .api.routes import router as api_router
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="API RiskBase",
    description=(
        "Bienvenido a la API de RiskBase. Esta plataforma te permite consultar, procesar y gestionar "
        "toda la información relacionada con la base de riesgo de inventarios de la compañía. "
        "A través de esta API podrás extraer datos directamente desde SAP, aplicar reglas de negocio "
        "para el cálculo de provisiones y clasificaciones, y exportar los resultados en archivos Excel "
        "para su análisis o integración con otros sistemas. Además, cuenta con mecanismos de autenticación "
        "y control de acceso para garantizar la seguridad de la información. Si tienes dudas sobre cómo "
        "utilizar los diferentes endpoints, consulta la documentación interactiva disponible en /docs."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejo global de errores
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"detail": f"Error interno del servidor: {str(exc)}"}
    )


# Incluir las rutas de la API
app.include_router(api_router)


host = os.getenv("API_HOST")
port = int(os.getenv("API_PORT"))
# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de del proyecto RiskBase",
        "docs": f"http://{host}:{port}/docs",
        "version": "1.0.0",
        "status": "OK",
        "autor": "Practicante planeación financiera",
    }
