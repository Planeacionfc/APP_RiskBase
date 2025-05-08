# 🚀 APP_RiskBase

## 📋 Descripción general  
APP_RiskBase es una aplicación web diseñada para facilitar la gestión, el análisis y la generación de informes de la base de riesgo de la organización. Integra datos desde SAP, aplica reglas de negocio para calcular factores provisionales y clasificaciones de riesgo, y ofrece interfaces diferenciadas para usuarios regulares y administradores, permitiendo procesamiento, visualización y actualización de políticas de la base de riesgo.

## 🎯 Objetivo general y alcance  
- **Objetivo general**: Desarrollar un aplicativo web sostenible y escalable que permita la gestión eficiente de la base de riesgo, garantizando la accesibilidad, almacenamiento y actualización de la información en tiempo real.   
- **Alcance**:  
  - Reducir el proceso operativo para la generación del informe de la base de riesgo.  
  - Facilitar la visualización de la información de manera estructurada e intuitiva.  
  - Permitir la modificación eficiente de los parámetros de la política de la base de riesgo.  
  - Almacenar la información procesada de la base de riesgo en una base de datos.  
  - Generar trazabilidad de los cambios realizados a la política de la base de riesgo.

## 🛠️ Requisitos  
### ✅ Funcionales  
- Extracción de datos SAP.  
- Transformación y ETL con pandas.  
- Lógica de negocio para factor provisional y clasificación (Patrón Strategy).  
- Autenticación JWT y autorización por roles.  
- Generación de archivos Excel y almacenamiento temporal.  
- Extracción, almacenamiento y actualización de datos.  
- Creación de usuarios y asignación de roles. 

### ⚠️ No funcionales  
- Solo integración con SAP; no otros ERP.  
- Sin análisis predictivo ni Machine Learning.  
- Historial básico sin auditoría avanzada.  
- Informes limitados a plantillas Excel predefinidas.

## ✔️ Criterios de aceptación  
1. Modelo de base de datos funcional.  
2. Creación de usuarios por roles (USER, ADMIN).  
3. Procesamiento de datos aplicando reglas de negocio (Patrón Strategy).  
4. Consulta y almacenamiento de datos.  
5. Descarga de archivos Excel con información procesada.  
6. Actualización y trazabilidad de la política de la base de riesgo.

## 🖥️ Entorno de desarrollo  
### 🐍 Backend  
- **Lenguaje**: Python 3.11.8  
- **Frameworks**: FastAPI (0.115.12), Django (5.1.7)  
- **ORM / DB**: SQLAlchemy, pyodbc (SQL Server)  
- **SAP**: pyrfc (3.3.1), sap_library  
- **Auth**: JWT (python‑jose v3.4.0), passlib v1.7.4  
- **Librerías**: pandas v2.2.3, numpy v2.2.4, openpyxl v3.1.5, python‑dotenv v1.1.0, requests, cryptography, bcrypt…  
- **Servidor**: Uvicorn  
- **Dependencias**: requirements.txt :contentReference 

### 💻 Frontend  
- **Lenguaje**: TypeScript  
- **Framework**: Next.js (15.2.2)  
- **UI**: React (19.1.0), Material UI (7.0.2), @mui/x-data-grid (8.1.0), SweetAlert2 (11.19.1)  
- **Estilos**: TailwindCSS (4.0.14), PostCSS (8.5.3)  
- **Auth**: jwt‑decode (4.0.0)  
- **Utilidades**: xlsx (0.18.5), next-themes (0.4.6)  
- **Dependencias**: package.json, package-lock.json

## 📦 Instalación y Configuración

Sigue estos pasos para instalar y configurar el proyecto **APP_RiskBase** (Backend y Frontend):

### Backend

1. Clonar el repositorio
```bash
git clone https://github.com/Planeacionfc/APP_RiskBase.git
cd APP_RiskBase/backend
```

2. Crear y activar un entorno virtual (recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus credenciales de base de datos, SAP, API, etc.
```

5. Iniciar el backend
```bash
python run.py
```
El backend estará disponible en la URL y puerto configurados en tu archivo `.env` (por defecto http://127.0.0.1:8000).

6. Acceder a la documentación interactiva
Abre tu navegador en:
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Frontend

1. Ir a la carpeta del frontend
```bash
cd ../frontend
```

2. Instalar dependencias
```bash
npm install
```

3. Iniciar el frontend en modo desarrollo
```bash
npm run dev
```
El frontend estará disponible por defecto en [http://localhost:3000](http://localhost:3000)

> Si necesitas configurar variables de entorno, crea un archivo `.env` en la carpeta `frontend` y la carpeta `backend` con las variables necesarias. En el archivo `.env.example` puedes ver el ejemplo.

---

## 🔗 Código Fuente en GitHub
- Repositorio [https://github.com/Planeacionfc/APP_RiskBase](https://github.com/Planeacionfc/APP_RiskBase)
- Repositorio Backend: [https://github.com/Planeacionfc/APP_RiskBase/tree/master/backend](https://github.com/Planeacionfc/APP_RiskBase/tree/master/backend)
- Repositorio Frontend: [https://github.com/Planeacionfc/APP_RiskBase/tree/master/frontend](https://github.com/Planeacionfc/APP_RiskBase/tree/master/frontend)

---

📋 **Para más información visita:**  [![Doc DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Planeacionfc/APP_RiskBase)

