# 🚀 App RiskBase - Aplicativo web para la gestión de base riesgo

## 📋 Descripción general  
APP_RiskBase es una aplicación web especializada en la gestión integral de la base de riesgo de la organización. Su propósito es optimizar la extracción, transformación, análisis y reporte de datos provenientes de sistemas ERP, específicamente SAP BW. La aplicación permite calcular factores provisionales y clasificaciones de riesgo mediante reglas de negocio definidas, ofreciendo interfaces diferenciadas para usuarios regulares y administradores.

**Características Principales**:
  - **Integración con SAP BW**: Utiliza la librería pyrfc para la conexión y extracción de datos desde SAP BW.
  -	**Procesamiento de Datos**: Implementa un pipeline ETL utilizando pandas y numpy para la transformación y análisis de los datos extraídos.
  -	**Cálculo de Riesgos**: Aplica reglas de negocio específicas para determinar factores provisionales y clasificaciones de riesgo.
  -	**Interfaz de Usuario**: Desarrollada con React y Next.js, proporcionando una experiencia de usuario intuitiva y responsiva.
  -	**Gestión de Usuarios**: Implementa autenticación basada en JWT y control de acceso por roles (user, admin).
  -	**Trazabilidad**: Registra y almacena los cambios realizados en las políticas de riesgo para auditoría y seguimiento.

## 🎯 Objetivo general y alcance  
**Objetivo general**: Desarrollar e implementar una aplicación web robusta, sostenible y escalable que optimice la gestión integral de la base de riesgo de la organización. Esta herramienta debe permitir:
  -	**Integración eficiente con SAP BW**: Facilitar la extracción automatizada de datos relevantes mediante la librería pyrfc, asegurando una conexión segura y confiable con el sistema SAP BW.
  -	**Procesamiento avanzado de datos**: Aplicar un pipeline ETL utilizando pandas y numpy para transformar y analizar los datos extraídos, permitiendo el cálculo preciso de factores provisionales y clasificaciones de riesgo.
  -	**Aplicación de reglas de negocio dinámicas**: Implementar reglas de negocio específicas para el cálculo de riesgos, utilizando el patrón de diseño Strategy para permitir flexibilidad y escalabilidad en la lógica de negocio.
  -	**Interfaz de usuario intuitiva y responsiva**: Desarrollar una interfaz de usuario con React y Next.js que proporcione una experiencia de usuario amigable, adaptada a diferentes dispositivos y resoluciones de pantalla.
  -	**Gestión de usuarios y control de acceso**: Implementar un sistema de autenticación basado en JWT y control de acceso por roles (user, admin), garantizando la seguridad y confidencialidad de la información.
  -	**Trazabilidad y auditoría de cambios**: Registrar y almacenar los cambios realizados en las políticas de riesgo, permitiendo una auditoría completa y seguimiento de las modificaciones.
   
**Alcance**:  
  -	**Automatización de Informes**: Reducción significativa del esfuerzo operativo necesario para la generación de informes de la base de riesgo, mediante la automatización de procesos y generación de archivos Excel con la información procesada.
  -	**Visualización de Datos**: Facilitar la interpretación de la información mediante representaciones gráficas y estructuradas, proporcionando dashboards interactivos y visualizaciones dinámicas.
  -	**Gestión de Políticas de Riesgo**: Permitir la modificación eficiente de los parámetros de las políticas de riesgo por parte de usuarios con rol de administrador, con registro de los cambios para auditoría.
  -	**Almacenamiento Seguro de Información**: Garantizar el almacenamiento seguro de la información procesada en una base de datos relacional (SQL Server), utilizando SQLAlchemy como ORM para la gestión de datos.
  -	**Integración con SAP BW**: Implementar una conexión segura y eficiente con SAP BW para la extracción de datos relevantes, utilizando la librería pyrfc.
  -	**Procesamiento y Análisis de Datos**: Aplicar un pipeline ETL utilizando pandas y numpy para la transformación y análisis de los datos extraídos, permitiendo el cálculo preciso de factores provisionales y clasificaciones de riesgo.
  -	**Aplicación de Reglas de Negocio**: Implementar reglas de negocio específicas para el cálculo de riesgos, utilizando el patrón de diseño Strategy para permitir flexibilidad y escalabilidad en la lógica de negocio.
  -	**Gestión de Usuarios y Control de Acceso**: Implementar un sistema de autenticación basado en JWT y control de acceso por roles (user, admin), garantizando la seguridad y confidencialidad de la información.
  -	**Trazabilidad y Auditoría de Cambios**: Registrar y almacenar los cambios realizados en las políticas de riesgo, permitiendo una auditoría completa y seguimiento de las modificaciones.
  -	**Interfaz de Usuario Intuitiva y Responsiva**: Desarrollar una interfaz de usuario con React y Next.js que proporcione una experiencia de usuario amigable, adaptada a diferentes dispositivos y resoluciones de pantalla.

## 🛠️ Requisitos  
### ✅ Funcionales  
**Extracción de datos SAP BW**
  -	Establecer una conexión segura con SAP BW mediante la librería pyrfc.
  -	Permitir la configuración dinámica de consultas RFC para extraer datos específicos según necesidades operativas.
  -	Validar la integridad y consistencia de los datos extraídos antes del procesamiento.

**Procesamiento ETL de datos**
  -	Implementar pipelines de transformación y carga (ETL) usando bibliotecas avanzadas como pandas y numpy.
  -	Transformar datos brutos extraídos de SAP BW en formatos normalizados aptos para análisis posterior.
  -	Automatizar el manejo de excepciones y errores en el pipeline de procesamiento.

**Aplicación de reglas de negocio (Patrón Strategy)**
  -	Implementar el patrón de diseño Strategy para gestionar distintas políticas y reglas de negocio: https://refactoring.guru/es/design-patterns/strategy.
  -	Permitir la creación, modificación y activación dinámica de distintas estrategias de cálculo de factores provisionales.
  -	Realizar la clasificación automática del riesgo (bajo, medio, alto) según reglas de negocio definidas.

**Autenticación JWT y autorización por roles**
  -	Implementar un sistema robusto de autenticación basado en JSON Web Tokens (JWT).
  -	Gestionar roles específicos (user, admin), restringiendo funcionalidades y acceso a datos según perfiles autorizados.
  -	Mantener sesiones seguras y persistentes mientras se garantizan las mejores prácticas de seguridad.

**Generación y manejo de informes Excel**
  -	Generar automáticamente archivos Excel.
  -	Permitir almacenamiento temporal seguro de los archivos generados antes de la descarga por parte del usuario.

**Gestión de Usuarios y Roles**
  -	Permitir la creación de usuarios mediante interfaz administrativa.
  -	Asignar roles específicos con distintos niveles de acceso a funcionalidades y datos.
  -	Implementar validaciones en la gestión de usuarios para evitar inconsistencias o duplicidades.

**Gestión y Trazabilidad de Políticas de Riesgo**
  -	Permitir modificaciones ágiles y seguras en los parámetros que conforman las políticas de riesgo.
  -	Registrar cada cambio realizado por los usuarios, con información detallada de, cuándo y qué se modificó.
  -	Proporcionar una interfaz que permita modificar fácilmente la política de la base de riesgo.
 
### ⚠️ No funcionales  
**Rendimiento**
  -	Los tiempos de respuesta para la extracción y procesamiento de datos deben ser óptimos.
  -	La interfaz de usuario debe cargar rápidamente, idealmente menos de 3 segundos en condiciones normales de red.

**Escalabilidad**
  -	Capacidad para gestionar el aumento en el volumen de datos extraídos y procesados sin degradar significativamente el rendimiento.
  -	Arquitectura modular que permita agregar nuevas funcionalidades sin afectar las existentes.

**Seguridad**
  -	Aplicar estándares modernos de seguridad para proteger datos sensibles.
  -	Autenticación robusta mediante JWT y autorización precisa basada en roles definidos.
  -	Protección contra vulnerabilidades comunes.

**Usabilidad**
  -	Interfaz intuitiva y amigable desarrollada con Next.js y React, compatible con dispositivos móviles y distintos navegadores.
  -	Documentación clara y accesible que facilite a los usuarios la operación cotidiana del sistema.

**Mantenibilidad**
  -	Código estructurado, modular y debidamente documentado.
  -	Uso de metodologías y patrones estándar como MVC, Strategy, y ETL.
  -	Facilitar la aplicación ágil de cambios futuros mediante documentación técnica clara.

**Disponibilidad**
  -	Garantizar una disponibilidad del sistema durante el horario laboral.
  -	Implementar procedimientos de recuperación en caso de fallas (backup, restore, tolerancia a fallos).

**Compatibilidad**
  -	Asegurar compatibilidad total con SAP BW y las versiones actuales y futuras cercanas.
  -	Garantizar la compatibilidad con navegadores modernos y más utilizados (Chrome, Edge, Firefox).

## ✔️ Criterios de aceptación  
**Modelo de Base de Datos**
  -	Se validará mediante pruebas unitarias y de integración que el modelo soporte todas las operaciones necesarias (CRUD, consultas complejas y auditoría de cambios).

**Extracción de Datos desde SAP**
  -	La aplicación deberá establecer exitosamente conexiones RFC a SAP BW y extraer correctamente los datos necesarios según consultas dinámicas.

**Procesamiento y Aplicación de Reglas de Negocio**
  -	Se verificará mediante pruebas automatizadas que las reglas de negocio se aplican correctamente, utilizando distintas estrategias y escenarios predefinidos.
  -	Validar que los cálculos realizados coinciden con las reglas de negocio especificadas por la persona encargada de la base de riesgo.

**Autenticación y Autorización**
  -	La autenticación JWT funcionará correctamente, gestionando sesiones y tokens seguros.
  -	Las pruebas demostrarán que los permisos y accesos según roles (user, admin) funcionan correctamente.

**Gestión de Informes Excel**
  -	La aplicación generará correctamente los informes en formato Excel permitiendo la descarga ágil y segura por parte del usuario.

**Interfaz de Usuario (Frontend)**
  -	Realizar pruebas de usuario que demuestren la usabilidad e intuición de la interfaz, validando el correcto funcionamiento del aplicativo.

**Trazabilidad y Gestión de Cambios**
  -	El sistema mantendrá una bitácora clara y accesible de todos los cambios realizados en las políticas de riesgo, mostrando, fecha/hora y detalle exacto de modificaciones.

**Rendimiento y Carga**
  -	Realizar pruebas de estrés y rendimiento que confirmen tiempos aceptables de carga y respuesta incluso bajo grandes volúmenes de datos.

**Seguridad del Sistema**
  -	Realización de pruebas de seguridad que garanticen protección frente a vulnerabilidades comunes y validen el cumplimiento de estándares de seguridad.

## 🖥️ Entorno de desarrollo  
### 🐍 Backend  
- **Lenguaje**: Python 3.11.8  
- **Frameworks**: FastAPI (0.115.12), Django (5.1.7)  
- **ORM / DB**: SQLAlchemy, pyodbc (SQL Server)  
- **SAP**: pyrfc (3.3.1) 
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

Sigue estos pasos para instalar y configurar el proyecto **APP_RiskBase** (Backend y Frontend) en un entorno local:

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

📋 **Para más información detallada sobre el proceso del aplicativo visita:**  [![Doc DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Planeacionfc/APP_RiskBase)

