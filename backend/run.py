import uvicorn
import os
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler

# Cargar variables de entorno
load_dotenv()

def check_required_env_vars():
    required_vars = [
        "API_HOST", "API_PORT", "DB_SERVER", "DATABASE", "DB_USER", "DB_PASSWORD",
        "ASHOST", "SYSNR", "CLIENT", "USER_SAP", "PASSWORD_SAP",
        "SECRET_KEY", "ALGORITHM", "ACCESS_TOKEN_EXPIRE_MINUTES"
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Faltan variables de entorno obligatorias: {', '.join(missing)}")

if __name__ == "__main__":
    check_required_env_vars()
    # Obtener configuración del servidor desde variables de entorno o usar valores predeterminados
    host = os.getenv("API_HOST")
    port = int(os.getenv("API_PORT"))
    
    # Configurar el directorio temporal para archivos
    temp_dir = os.getenv("TEMP_DIR")
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Iniciando servidor en http://{host}:{port}")
    print(f"Documentación disponible en http://{host}:{port}/docs")
    
    # Iniciar el servidor
    uvicorn.run("riskbase.main:app", host=host, port=port, reload=True)

handler = TimedRotatingFileHandler(
    "app.log", when="midnight", interval=1, backupCount=7, encoding="utf-8"
)  # Rota cada medianoche, guarda 7 días de logs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        handler,  # TimedRotatingFileHandler que ya maneja la escritura al archivo
        logging.StreamHandler(),  # Para mostrar logs en consola
    ]
)