"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

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
        <div className="bg-white/80 dark:bg-[#232836] border border-gray-300 dark:border-gray-500 rounded-xl shadow-lg p-6 flex flex-col items-center opacity-70 cursor-not-allowed">
          <h2 className="text-2xl font-semibold mb-2 text-gray-400 dark:text-gray-500">Medición de Inventario</h2>
          <span className="text-xs ml-2 bg-yellow-200 text-yellow-800 px-2 py-0.5 rounded">Próximamente</span>
          <p className="text-gray-500 dark:text-gray-500 mb-4 text-center">Este módulo permitirá gestionar y analizar el inventario del área financiera. Disponible en una próxima actualización.</p>
          <button className="w-full py-2 px-4 bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 font-semibold rounded-lg shadow" disabled>
            Próximamente
          </button>
        </div>

        {/* Sección CMI */}
        <div className="bg-white/80 dark:bg-[#232836] border border-gray-300 dark:border-gray-500 rounded-xl shadow-lg p-6 flex flex-col items-center opacity-70 cursor-not-allowed">
          <h2 className="text-2xl font-semibold mb-2 text-gray-400 dark:text-gray-500">CMI</h2>
          <span className="text-xs ml-2 bg-yellow-200 text-yellow-800 px-2 py-0.5 rounded">Próximamente</span>
          <p className="text-gray-500 dark:text-gray-500 mb-4 text-center">Este módulo permitirá gestionar y analizar el inventario del área financiera. Disponible en una próxima actualización.</p>
          <button className="w-full py-2 px-4 bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 font-semibold rounded-lg shadow" disabled>
            Próximamente
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
