"use client";
import React, { useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { showAlert } from "../../utils/swal";;

interface JwtPayload {
  role?: string;
  [key: string]: any;
}

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Error al iniciar sesión');
        // Mostrar alerta SweetAlert de error
        showAlert({
          icon: "error",
          title: "Oops...",
          text: "Usuario o contraseña incorrectos"
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
      // Decodificar JWT para obtener el rol
      const decoded = jwtDecode<JwtPayload>(token);
      // Guardar el token y el tipo de token (opcional)
      localStorage.setItem('token', token);
      if (tokenType) localStorage.setItem('token_type', tokenType);
      // Validar si el rol existe en el JWT
      if (!decoded.role) {
        setError('El token recibido no contiene información de rol. Contacta al administrador.');
        setLoading(false);
        return;
      }
      // Mostrar animación SweetAlert antes de redirigir
      showAlert({
        position: "center",
        icon: "success",
        title: "¡Bienvenido!",
        showConfirmButton: false,
        timer: 800
      });

      // Redirigir a la página de inicio (Home) después del login exitoso
      router.push('/');
    } catch (err) {
      setError('Error de red o servidor');
      // Mostrar animación SweetAlert de error
      showAlert({
        icon: "error",
        title: "Oops...",
        text: "Error de red o servidor"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center from-skyBlue via-bone to-white dark:from-skyBlue dark:via-none dark:to-[#202020]">
      <div className="w-full max-w-sm p-8 rounded-4xl shadow-xl bg-[#2c3e64] shadow-md flex flex-col items-center">
        <div className="flex flex-col items-center mb-8" >
          <Image
            src="/image/Prebel_Blanco.webp"
            alt="Logo Prebel Blanco"
            width={200}
            height={200}
            className="mb-2 drop-shadow-lg"
            priority
          />
        </div>
        <h2 className="text-4xl font-bold text-center mb-8 text-skyBlue dark:text-bone tracking-tight">Iniciar sesión</h2>
        <form onSubmit={handleLogin} className="space-y-6 w-full">
          <div>
            <label className="block text-lg font-semibold text-gray-200 mb-1 ">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              className="w-full px-5 py-3 bg-[#222a3a] border border-gray-400 rounded-lg text-[var(--color-cloud)] placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[var(--color-skyBlue)] shadow-[0_1.5px_8px_0_#2225] transition-all duration-200 text-base"
              placeholder="example@example.com"
              autoComplete="username"
            />
          </div>
          <div>
            <label className="block text-lg font-semibold text-gray-200 mb-1">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              className="w-full px-5 py-3 bg-[#222a3a] border border-gray-400 rounded-lg text-[var(--color-cloud)] placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[var(--color-skyBlue)] shadow-[0_1.5px_8px_0_#2225] transition-all duration-200 text-base"
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 px-4 bg-skyBlue hover:bg-sky-600 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-skyBlue font-semibold rounded-lg shadow-md transition-colors duration-200 disabled:opacity-60"
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </div>
    </div>
  );
}
