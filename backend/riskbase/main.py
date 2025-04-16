from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
