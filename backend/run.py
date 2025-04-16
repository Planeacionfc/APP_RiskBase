import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

if __name__ == "__main__":
    # Obtener configuración del servidor desde variables de entorno o usar valores predeterminados
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    
    # Configurar el directorio temporal para archivos
    temp_dir = os.getenv("TEMP_DIR", "./temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Iniciando servidor en http://{host}:{port}")
    print(f"Documentación disponible en http://{host}:{port}/docs")
    
    # Iniciar el servidor
    uvicorn.run("riskbase.main:app", host=host, port=port, reload=True)
