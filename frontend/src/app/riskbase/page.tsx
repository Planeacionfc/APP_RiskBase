"use client";
import React, { useState } from "react";

export default function RiskBasePage() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const [data, setData] = useState<string[][]>([]); // Dataframe
  const [loading, setLoading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  // Recupera el token JWT almacenado en localStorage
  const getToken = () => {
    // Cambia "token" por el nombre real que usas si es diferente
    return localStorage.getItem("token");
  };

  // Procesar: llama a /risk/process y luego obtiene los datos desde /risk/data-view
  const handleProcess = async () => {
    setProcessing(true);
    setError("");
    try {
      const token = getToken();
      const response = await fetch(`${API_URL}/risk/process`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });
      if (!response.ok) throw new Error("Error al procesar datos");
      // Ahora obtenemos el dataframe desde /risk/data-view
      const dfRes = await fetch(`${API_URL}/risk/data-view`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (!dfRes.ok) throw new Error("No se pudo cargar el dataframe procesado");
      const df = await dfRes.json(); // Espera un array de arrays
      setData(df);
    } catch (err: any) {
      setError(err.message || "Error inesperado");
    } finally {
      setProcessing(false);
    }
  };

  // Guardar en BD
  const handleSaveToDB = async () => {
    setLoading(true);
    setError("");
    try {
      const token = getToken();
      const response = await fetch(`${API_URL}/risk/save-to-db`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });
      if (!response.ok) throw new Error("Error al guardar en BD");
      // Puedes mostrar un mensaje de éxito si lo deseas
    } catch (err: any) {
      setError(err.message || "Error inesperado");
    } finally {
      setLoading(false);
    }
  };

  // Exportar Excel
  const handleExportExcel = async () => {
    setLoading(true);
    setError("");
    try {
      const token = getToken();
      const response = await fetch(`${API_URL}/risk/export-excel`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error("Error al exportar Excel");
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "base_riesgo.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.message || "Error inesperado");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-white dark:bg-[#232836] px-4 py-8">
      <h1 className="text-3xl md:text-4xl font-bold mb-8 mt-2 text-center text-skyBlue dark:text-bone">Base de Riesgo</h1>
      <div className="w-full max-w-5xl flex flex-col items-center bg-white/80 dark:bg-[#232836] rounded-xl shadow-lg p-8 border border-skyBlue dark:border-bone">
        <div className="flex justify-center mb-6 w-full">
          <button
            className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
            onClick={handleProcess}
            disabled={processing}
          >
            {processing && (
              <svg className="animate-spin h-5 w-5 text-white dark:text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
            )}
            {processing ? "Procesando..." : "Procesar"}
          </button>
        </div>
        {/* Tabla dinámica renderizada */}
        <div className="overflow-x-auto w-full flex justify-center mb-8">
          <table className="min-w-[600px] max-w-3xl w-full border border-gray-300 dark:border-gray-700 bg-white dark:bg-[#232836] rounded-lg">
            <thead>
              <tr>
                {data.length > 0 && data[0].map((_, i) => (
                  <th key={i} className="border border-gray-300 dark:border-gray-700 px-4 py-2 bg-gray-100 dark:bg-[#32394a] text-gray-700 dark:text-gray-200 font-semibold">Col {i+1}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.length > 0 ? (
                data.map((row, rowIdx) => (
                  <tr key={rowIdx}>
                    {row.map((cell, colIdx) => (
                      <td key={colIdx} className="border border-gray-300 dark:border-gray-700 px-4 py-3 text-center text-gray-800 dark:text-gray-100">{cell}</td>
                    ))}
                  </tr>
                ))
              ) : (
                Array.from({ length: 7 }).map((_, rowIdx) => (
                  <tr key={rowIdx}>
                    {Array.from({ length: 7 }).map((_, colIdx) => (
                      <td key={colIdx} className="border border-gray-300 dark:border-gray-700 px-4 py-3 text-center text-gray-800 dark:text-gray-100"> </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        {error && <div className="text-red-500 mb-4">{error}</div>}
        <div className="flex flex-col md:flex-row gap-6 w-full justify-center mt-2">
          <button
            className="w-full md:w-auto py-3 px-8 bg-white dark:bg-[#32394a] border border-skyBlue dark:border-bone text-skyBlue dark:text-bone font-semibold rounded-lg shadow transition-colors duration-200 text-lg hover:bg-skyBlue/10 dark:hover:bg-bone/10"
            onClick={handleExportExcel}
            disabled={loading}
          >
            Exportar Excel
          </button>
          <button
            className="w-full md:w-auto py-3 px-8 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-lg"
            onClick={handleSaveToDB}
            disabled={loading}
          >
            Guardar en BD
          </button>
        </div>
      </div>
    </div>
  );
}
