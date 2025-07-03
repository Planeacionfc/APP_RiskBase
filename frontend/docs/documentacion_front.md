# Documentación del Frontend

## Descripción del Proyecto

Esta es una aplicación Next.js que sirve como interfaz de usuario para la aplicación RiskBase. Proporciona una interfaz para gestionar procesos de riesgo y operaciones relacionadas.

## Estructura del Proyecto

```
frontend/
├── public/                # Archivos estáticos
│   └── image/             # Imágenes
├── src/
│   ├── app/               # Directorio de la aplicación de Next.js
│   ├── components/        # Componentes de interfaz de usuario reutilizables
│   │   └── theme/         # Componentes del tema
│   ├── hooks/             # Ganchos (hooks) de React personalizados
│   └── utils/             # Funciones de utilidad
├── .env.local            # Variables de entorno
├── next.config.mjs       # Configuración de Next.js
├── package.json          # Dependencias del proyecto
└── tsconfig.json         # Configuración de TypeScript
```

## Comenzando

### Requisitos Previos
- Node.js 16.8 o superior
- npm

### Instalación

1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   npm install
   ```
3. Crear un archivo `.env.local` en el directorio raíz con las siguientes variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_APP_CMI= URL de la aplicacion de CMI
   NEXT_PUBLIC_APP_MED= URL de la aplicacion de Medicion de inventarios
   ```

4. Iniciar el servidor de desarrollo:
   ```bash
   npm run dev
   ```
5. Abrir [http://localhost:3000](http://localhost:3000) en tu navegador

## Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye la aplicación para producción
- `npm start` - Inicia el servidor de producción
- `npm run lint` - Ejecuta ESLint
- `npm run test` - Ejecuta las pruebas

## Características Principales

- **Autenticación**: Inicio de sesión y registro de usuarios
- **Panel de control**: Vista general de los procesos de riesgo
- **Gestión de Riesgos**: Crear, leer, actualizar y eliminar procesos de riesgo

### Componentes Principales

- `Layout`: Diseño principal de la aplicación
- `Navbar`: Barra de navegación superior
- `ThemeProvider`: Gestión de temas

### Páginas

- `/` - Panel de control
- `/login` - Inicio de sesión de usuario
- `/createUsers` - Registro de usuario
- `/riskbase` - Gestión de procesos de riesgo
- `/matrices` - Interfaz de matrices

## Variables de Entorno

- `NEXT_PUBLIC_API_URL`: URL base para las peticiones a la API
- `NEXT_PUBLIC_APP_CMI`: URL de la aplicacion de CMI
- `NEXT_PUBLIC_APP_MED`: URL de la aplicacion de Medicion de inventarios

## Despliegue

Para el despliegue en producción:

1. Construir la aplicación:
   ```bash
   npm run build
   ```
2. Iniciar el servidor de producción:
   ```bash
   npm start
   ```
