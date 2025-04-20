# APP_RiskBase - Aplicativo Web para la Gestión de la Base de Riesgo

## Descripción General del Proyecto
El aplicativo web tiene como finalidad optimizar la gestión de la base de riesgo, facilitando la extracción, almacenamiento, consulta, modificación y visualización de la información. Este sistema está diseñado para reducir la carga operativa y mejorar la eficiencia en la actualización y administración de datos.

## Objetivo General y Alcance
### Objetivo General
Desarrollar un aplicativo web sostenible y escalable que permita la gestión eficiente de la base de riesgo, garantizando la accesibilidad y actualización de la información en tiempo real.

### Alcance
- Reducir el proceso operativo para la generación del informe de la base de riesgo.
- Facilitar la visualización de la información de manera estructurada e intuitiva.
- Permitir la modificación eficiente de los parámetros de la política de la base de riesgo.

## Requisitos Funcionales y No Funcionales
### Funcionales
- Gestión de usuarios y permisos.
- Creación, actualización y eliminación de registros de riesgo.
- Visualización dinámica de datos a través de gráficos y reportes.
- Configuración de parámetros para la gestión de la base de riesgo.

### No Funcionales
- Seguridad en el acceso y protección de datos.
- Rendimiento y escalabilidad del sistema.
- Interfaz amigable y adaptable a distintos dispositivos.

## Criterios de Aceptación
- El sistema debe permitir la consulta y modificación de datos en tiempo real.
- La plataforma debe garantizar un acceso seguro con autenticación y control de permisos.
- La interfaz debe ser intuitiva y permitir la interacción fluida con los datos.

## Especificaciones del Entorno de Desarrollo
- **Backend:** Python, Django, Django Rest Framework
- **Base de Datos:** SQL Server
- **Frontend:** React, Node.js

## Instalación y Configuración

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

> Si necesitas configurar variables de entorno para el frontend (por ejemplo, la URL del backend), crea un archivo `.env.local` en la carpeta `frontend` con las variables necesarias. Consulta la documentación de tu equipo para más detalles.

---

## Código Fuente en GitHub
- Repositorio Backend: [https://github.com/Planeacionfc/APP_RiskBase/tree/master/backend](https://github.com/Planeacionfc/APP_RiskBase/tree/master/backend)
- Repositorio Frontend: [https://github.com/Planeacionfc/APP_RiskBase/tree/master/frontend](https://github.com/Planeacionfc/APP_RiskBase/tree/master/frontend)

## Plan de Soporte
- Revisiones periódicas para garantizar la estabilidad del sistema backend.
- Mantenimiento preventivo y correctivo del código y dependencias.
- Actualización de librerías y parches de seguridad.
- Soporte técnico a usuarios y desarrolladores mediante canales definidos (correo, tickets, etc).
- Documentación actualizada para facilitar la transferencia de conocimiento y onboarding de nuevos desarrolladores.

## Monitorización y Logs
- El backend implementa manejo global de errores y respuestas estructuradas para una mejor trazabilidad.
- Se recomienda activar y centralizar logs usando herramientas como [Uvicorn logging], [Loguru], o integración con sistemas de monitoreo como ELK Stack (Elasticsearch, Logstash, Kibana) o Grafana Loki.
- Monitoreo de la salud del backend mediante endpoints de status y alertas automáticas ante caídas o errores críticos.
- Revisión periódica de los archivos de log y métricas de uso para detectar patrones anómalos o cuellos de botella.

## Estrategias de Mantenimiento y Actualizaciones
- Realizar backups regulares de la base de datos y de los archivos de configuración.
- Probar las actualizaciones en un entorno de staging antes de desplegarlas en producción.
- Automatizar los despliegues y actualizaciones usando herramientas como Docker, CI/CD (GitHub Actions, GitLab CI, etc).
- Mantener actualizado el archivo `.env` y nunca exponerlo en repositorios públicos.
- Documentar cada cambio relevante en el backend en el historial de versiones (changelog).
- Revisar y actualizar las políticas de CORS y seguridad conforme evolucionen los requisitos del frontend.

## Plan de Seguridad Técnica
- Implementación de autenticación y control de accesos.
- Protección de datos sensibles mediante cifrado.

## Arquitectura y Patrones
- Arquitectura basada en API REST.
- Uso de patrones de diseño como MVC.

## Descripción de Usuarios y Roles
- **Administrador:** Acceso total al sistema.
- **Usuario Operativo:** Consulta de datos.

## Plan de Despliegue e Instalación
- Despliegue en entornos de prueba y producción.
- Uso de contenedores para facilitar la escalabilidad.

## Requisitos de Seguridad
- Control de accesos mediante roles y permisos.
- Registro de auditoría para seguimiento de cambios en la base de datos.

---
**Tecnologías utilizadas:** Python (backend), SQL Server (base de datos) y React (frontend).
