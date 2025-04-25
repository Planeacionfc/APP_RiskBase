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
    title="RiskBase API",
    description="API para la gestión de la base de riesgo",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",  # Cambia esto por el dominio real si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejo global de errores
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error interno del servidor: {str(exc)}"}
    )

# Incluir las rutas de la API
app.include_router(api_router)

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de del proyecto APP_RiskBase",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0",
        "status": "OK",
    }
