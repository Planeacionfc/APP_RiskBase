"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from 'jwt-decode';
import { showAlert } from "../utils/swal";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.replace("/login");
    } else {
      setIsAuthenticated(true);
      setLoading(false);
    }
  }, [router]);

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center">
        <h1 className="text-3xl font-bold">Cargando contenido...</h1>
      </div>
    );
  }

  // --- INTERFAZ PARA JWT ---
  interface JwtPayloadWithRole {
    role?: string;
    [key: string]: any;
  }

  const checkAdminRole = () => {
    if (typeof window === 'undefined') return false;
    const token = localStorage.getItem('token');
    if (!token) return false;
    try {
      const payload = jwtDecode<JwtPayloadWithRole>(token);
      return payload.role === 'admin';
    } catch {
      return false;
    }
  };

  const show403Alert = async () => {
    await showAlert({
      position: "center",
      icon: 'warning',
      title: 'Permiso denegado',
      text: 'No tienes permisos para realizar esta acción. Si crees que es un error, contacta al administrador.',
      showConfirmButton: true,
      confirmButtonText: 'OK'
    });
  };

  const handleGoToCMI = () => {
    if (checkAdminRole()) {
      window.open(process.env.NEXT_PUBLIC_URL_CMI, '_blank', 'noopener,noreferrer');
    } else {
      show403Alert();
    }
  };

  const handleGoToMedicion = () => {
    if (checkAdminRole()) {
      window.open(process.env.NEXT_PUBLIC_URL_MED, '_blank', 'noopener,noreferrer');
    } else {
      show403Alert();
    }
  };

  // Aquí va el contenido real del home para usuarios autenticados
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-white to-bone dark:from-[#232836] dark:to-[#32394a] px-4 py-8">
      <h1 className="text-3xl md:text-4xl font-bold mb-4 text-center">Bienvenido a <span className="text-skyBlue">ManagerPf</span> </h1>
      <p className="max-w-2xl text-center text-lg text-gray-700 dark:text-gray-300 mb-10">
        Esta es la página principal para la gestión de proyectos de planeación financiera. Aquí se alojarán todos los proyectos destinados al área, facilitando el acceso y administración centralizada. Actualmente, tienes disponibles los siguientes módulos:
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-3xl">

        {/* Sección Base de Riesgo */}
        <div className="bg-white/80 dark:bg-[#232836] border border-skyBlue dark:border-bone rounded-xl shadow-lg p-6 flex flex-col items-center">
          <h2 className="text-2xl font-semibold mb-2 text-skyBlue dark:text-bone">Base de Riesgo</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4 text-center">Gestiona y consulta la base de riesgo del área financiera. Accede a descargas, consultas y actualizaciones de la base de riesgo.</p>
          <a href="/riskbase" className="mt-auto w-full">
            <button className="w-full py-2 px-4 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200">
              Ir a Base de Riesgo
            </button>
          </a>
        </div>

        {/* Sección Medición de Inventario */}
        <div className="bg-white/80 dark:bg-[#232836] border border-skyBlue dark:border-bone rounded-xl shadow-lg p-6 flex flex-col items-center">
          <h2 className="text-2xl font-semibold mb-2 text-skyBlue dark:text-bone">Medición de Inventario</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4 text-center">Es el proceso mensual que consolida y valora materiales usando datos SAP y proyecciones de ventas para generar informes.</p>
          <button
            onClick={handleGoToMedicion}
            className="mt-auto w-full py-2 px-4 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200"
          >
            Ir a Medición de Inventario
          </button>
        </div>

        {/* Sección CMI */}
        <div className="bg-white/80 dark:bg-[#232836] border border-skyBlue dark:border-bone rounded-xl shadow-lg p-6 flex flex-col items-center">
          <h2 className="text-2xl font-semibold mb-2 text-skyBlue dark:text-bone">CMI</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4 text-center">La transformación del CMI busca optimizar la gestión y toma de decisiones mediante el análisis en tiempo real de métricas clave.</p>
          <button
            onClick={handleGoToCMI}
            className="mt-auto w-full py-2 px-4 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200"
          >
            Ir a CMI
          </button>
        </div>

        {/* Sección Modelo financiero */}
        <div className="bg-white/80 dark:bg-[#232836] border border-gray-300 dark:border-gray-500 rounded-xl shadow-lg p-6 flex flex-col items-center opacity-70 cursor-not-allowed">
          <h2 className="text-2xl font-semibold mb-2 text-gray-400 dark:text-gray-500">Modelo financiero </h2>
          <span className="text-xs ml-2 bg-yellow-200 text-yellow-800 px-2 py-0.5 rounded">Próximamente</span>
          <p className="text-gray-500 dark:text-gray-500 mb-4 text-center">Este módulo permitirá gestionar y analizar el inventario del área financiera. Disponible en una próxima actualización.</p>
          <button className="w-full py-2 px-4 bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 font-semibold rounded-lg shadow" disabled>
            Próximamente
          </button>
        </div>
      </div>
    </div>
  );
}
