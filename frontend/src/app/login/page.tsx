"use client";
import React, { useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { showAlert } from "../../utils/swal";;

// Interfaz para tipar el payload del JWT
interface JwtPayload {
  role?: string; // El rol es importante para la autorización
  [key: string]: any; // Permite otras propiedades en el token
}

export default function LoginPage() {
  // Estados para manejar el formulario y el proceso de login
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // Almacena mensajes de error
  const [loading, setLoading] = useState(false); // Controla estado de carga
  const router = useRouter(); // Hook para navegación programática

  // URL base de la API desde variables de entorno
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  /**
   * Maneja el proceso de autenticación del usuario
   * Realiza la petición al backend, procesa la respuesta y gestiona
   * el almacenamiento del token JWT y la redirección
   */
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault(); // Previene el comportamiento por defecto del formulario
    setError(''); // Limpia errores previos
    setLoading(true); // Activa indicador de carga
    try {
      // Petición de autenticación al endpoint de login
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      // Manejo de respuesta de error desde el servidor
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Error al iniciar sesión');
        // Mostrar alerta visual de error con SweetAlert
        showAlert({
          position: "center",
          icon: "error",
          title: "Oops...",
          text: "Usuario o contraseña incorrectos",
          showConfirmButton: true,
          confirmButtonText: 'OK'
        });
        setLoading(false);
        return;
      }
      const data = await response.json();
      const token = data.access_token;
      const tokenType = data.token_type;
      if (!token) {
        setError('No se recibió token');
        setLoading(false);
        return;
      }
      // Decodificar JWT para obtener el rol y validar permisos
      const decoded = jwtDecode<JwtPayload>(token);

      // Almacenamiento del token en localStorage para mantener la sesión
      localStorage.setItem('token', token);
      if (tokenType) localStorage.setItem('token_type', tokenType);

      // Validación de seguridad: verificar que el token contiene un rol
      if (!decoded.role) {
        setError('El token recibido no contiene información de rol. Contacta al administrador.');
        setLoading(false);
        return;
      }
      // Feedback visual de éxito para mejorar la experiencia de usuario
      showAlert({
        position: "center",
        icon: "success",
        title: "¡Bienvenido!",
        showConfirmButton: false,
        timer: 800 // Desaparece automáticamente después de 800ms
      });

      // Redirección a la página principal tras autenticación exitosa
      router.push('/');
    } catch (err) {
      // Captura errores de red o excepciones durante la petición
      setError('Error de red o servidor');
      // Feedback visual del error para el usuario
      showAlert({
        position: "center",
        icon: "error",
        title: "Oops...",
        text: "Error de red o servidor, por favor reinicia",
        showConfirmButton: true,
        confirmButtonText: 'OK'
      });
    } finally {
      // Garantiza que el estado de carga se desactive independientemente del resultado
      setLoading(false);
    }
  };

  // Renderizado del componente: formulario de login con diseño responsive
  return (
    <div className="min-h-screen flex items-center justify-center from-skyBlue via-bone to-white dark:from-skyBlue dark:via-none dark:to-[#202020]">
      {/* Contenedor principal del formulario con estilo corporativo */}
      <div className="w-full max-w-sm p-8 rounded-4xl shadow-xl 
        bg-white dark:bg-[#2c3e64] 
        shadow-md flex flex-col items-center
        border border-gray-200 dark:border-none
      ">
        {/* Logo de la empresa */}
        <div className="flex flex-col items-center mb-8">
          {/* Logo dinámico según el modo de color */}
          <Image
            src="/image/Prebel_AzulClaro_SF.webp"
            alt="Logo Prebel Azul"
            width={200}
            height={200}
            className="mb-2 drop-shadow-lg block dark:hidden"
            priority // Carga prioritaria para mejorar LCP
          />
          <Image
            src="/image/Prebel_Blanco.webp"
            alt="Logo Prebel Blanco"
            width={200}
            height={200}
            className="mb-2 drop-shadow-lg hidden dark:block"
            priority // Carga prioritaria para mejorar LCP
          />
        </div>
        <h2 className="text-4xl font-bold text-center mb-8 text-skyBlue dark:text-bone tracking-tight">Iniciar sesión</h2>
        {/* Formulario de login con validación HTML5 */}
        <form onSubmit={handleLogin} className="space-y-6 w-full">
          {/* Campo de email */}
          <div>
            <label className="block text-lg font-semibold text-gray-700 dark:text-gray-200 mb-1 ">Email</label>
            <input
              type="email" // Validación de formato de email
              value={email}
              onChange={e => setEmail(e.target.value)}
              required // Campo obligatorio
              className="w-full px-5 py-3 
                bg-white dark:bg-[#222a3a] 
                border border-gray-300 dark:border-gray-400 
                rounded-lg 
                text-gray-800 dark:text-[var(--color-cloud)] 
                placeholder-gray-400 
                focus:outline-none focus:ring-2 focus:ring-[var(--color-skyBlue)] 
                shadow-[0_1.5px_8px_0_#2225] 
                transition-all duration-200 text-base"
              placeholder="ejemplo@prebel.com"
              autoComplete="username" // Mejora la experiencia de autocompletado
            />
          </div>
          {/* Campo de contraseña */}
          <div>
            <label className="block text-lg font-semibold text-gray-700 dark:text-gray-200 mb-1">Contraseña</label>
            <input
              type="password" // Campo de tipo password para ocultar caracteres
              value={password}
              onChange={e => setPassword(e.target.value)}
              required // Campo obligatorio
              className="w-full px-5 py-3 
                bg-white dark:bg-[#222a3a] 
                border border-gray-300 dark:border-gray-400 
                rounded-lg 
                text-gray-800 dark:text-[var(--color-cloud)] 
                placeholder-gray-400 
                focus:outline-none focus:ring-2 focus:ring-[var(--color-skyBlue)] 
                shadow-[0_1.5px_8px_0_#2225] 
                transition-all duration-200 text-base"
              placeholder="••••••••"
              autoComplete="current-password" // Facilita el autocompletado seguro
            />
          </div>
          {/* Botón de envío con estado de carga */}
          <button
            type="submit"
            disabled={loading} // Deshabilita el botón durante la carga
            className="w-full py-2 px-4 
              bg-skyBlue hover:bg-sky-600 
              dark:bg-bone dark:hover:bg-bone/80 
              text-white dark:text-skyBlue 
              font-semibold rounded-lg shadow-md 
              transition-colors duration-200 disabled:opacity-60"
          >
            {loading ? 'Entrando...' : 'Entrar'} {/* Texto dinámico según estado */}
          </button>
        </form>
      </div>
    </div>
  );
}
