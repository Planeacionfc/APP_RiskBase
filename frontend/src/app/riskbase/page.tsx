"use client";
import React, { useState } from "react";
import Swal from "sweetalert2";

export default function RiskBasePage() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const [data, setData] = useState<any[]>([]); // Dataframe dinámico
  const [columns, setColumns] = useState<string[]>([]); // Columnas dinámicas
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");
  const [excelFile, setExcelFile] = useState<string>("");

  // Estado para paginación de columnas
  const [columnPage, setColumnPage] = useState(0);
  const columnsPerPage = 8; // Número de columnas visibles por página
  const totalColumnPages = Math.ceil(columns.length / columnsPerPage);

  // Columnas a mostrar según la página
  const paginatedColumns = columns.slice(columnPage * columnsPerPage, (columnPage + 1) * columnsPerPage);

  // Recupera el token JWT almacenado en localStorage
  const getToken = () => {
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
      const result = await response.json();
      const excelFileName = result.excel_file;
      if (!excelFileName) throw new Error("No se recibió el archivo Excel generado");
      setExcelFile(excelFileName);
      // Obtener los datos procesados desde /risk/data-view
      const dfRes = await fetch(`${API_URL}/risk/data-view?temp_file=${excelFileName}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (dfRes.status === 401) {
        Swal.fire({
          icon: 'error',
          title: 'No autorizado',
          text: 'No estás autorizado o tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
        });
        setProcessing(false);
        return;
      }
      if (!dfRes.ok) throw new Error("Error al obtener los datos procesados");
      const df = await dfRes.json();
      setColumns(df.columns || []);
      setData((df.data || []).map((row: any) => {
        const rowObj: any = {};
        (df.columns || []).forEach((col: string) => {
          rowObj[col] = row[col];
        });
        return rowObj;
      }));
      Swal.fire({
        icon: 'success',
        title: '¡Proceso finalizado!',
        text: 'El proceso ha terminado exitosamente.'
      });
    } catch (err: any) {
      setError(err.message || "Error inesperado");
    } finally {
      setProcessing(false);
    }
  };

  // Guardar en BD con confirmación
  const handleSaveToDB = async () => {
    const confirm = await Swal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas guardar los datos en la base de datos? Esta acción eliminará el archivo temporal.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sí, guardar',
      cancelButtonText: 'Cancelar',
      reverseButtons: true
    });
    if (!confirm.isConfirmed) return;

    setSaving(true);
    setError("");
    try {
      const token = getToken();
      if (!excelFile) throw new Error("No hay archivo Excel generado para guardar en BD");
      const response = await fetch(`${API_URL}/risk/save-to-db`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ filename: excelFile })
      });
      if (response.status === 401) {
        Swal.fire({
          icon: 'error',
          title: 'No autorizado',
          text: 'No estás autorizado o tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
        });
        setSaving(false);
        return;
      }
      if (!response.ok) throw new Error("Error al guardar en BD");
      // Eliminar el archivo temporal después de guardar en BD
      await fetch(`${API_URL}/risk/delete-temp-file?filename=${excelFile}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      Swal.fire({
        icon: 'success',
        title: '¡Proceso finalizado!',
        text: 'Datos guardados exitosamente.'
      });
    } catch (err: any) {
      setError(err.message || "Error inesperado");
    } finally {
      setSaving(false);
    }
  };

  // Exportar Excel
  const handleExportExcel = async () => {
    setLoading(true);
    setError("");
    try {
      const token = getToken();
      if (!excelFile) throw new Error("No hay archivo Excel generado para exportar");
      const response = await fetch(`${API_URL}/risk/export-excel?filename=${excelFile}`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (response.status === 401) {
        Swal.fire({
          icon: 'error',
          title: 'No autorizado',
          text: 'No estás autorizado o tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
        });
        setLoading(false);
        return;
      }
      if (!response.ok) throw new Error("Error al exportar Excel");
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "Análisis_BaseRiesgo_Final.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.message || "Error inesperado");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-white dark:bg-[#232836] px-15 py-10">
      <h1 className="text-3xl md:text-4xl font-bold mb-8 mt-2 text-center text-skyBlue dark:text-bone">Base de Riesgo</h1>
      <div className="w-full max-w-9xl flex flex-col items-center bg-white/80 dark:bg-[#2c3e64] rounded-xl shadow-black shadow-md p-12">
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
        <div className="overflow-x-auto w-full flex justify-center mb-8 px-4" style={{ maxHeight: 500, overflowY: 'auto' }}>
          <table className="w-max border border-gray-300 dark:border-gray-700 bg-white dark:bg-[#232836] rounded-lg">
            <thead>
              <tr>
                {paginatedColumns.length > 0 && paginatedColumns.map((col, i) => (
                  <th key={i} className="border border-gray-300 dark:border-gray-700 px-4 py-2 bg-gray-100 dark:bg-[#32394a] text-gray-700 dark:text-gray-200 font-semibold">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.length > 0 ? (
                data.map((row, rowIdx) => (
                  <tr key={rowIdx}>
                    {paginatedColumns.map((col, colIdx) => (
                      <td key={colIdx} className="border border-gray-300 dark:border-gray-700 px-4 py-3 text-center text-gray-800 dark:text-gray-100">{row[col]}</td>
                    ))}
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={paginatedColumns.length || 1} className="border border-gray-300 dark:border-gray-700 px-4 py-3 text-center text-gray-800 dark:text-gray-100 shadow-md">No hay datos</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {/* Paginación de columnas */}
        {totalColumnPages > 1 && (
          <div className="flex justify-center items-center gap-2 mb-6">
            <button
              onClick={() => setColumnPage((prev) => Math.max(prev - 1, 0))}
              disabled={columnPage === 0}
              className="px-3 py-1 bg-skyBlue text-white rounded disabled:opacity-50"
            >
              Anterior
            </button>
            <span className="text-md text-gray-700 dark:text-gray-200">Página columnas {columnPage + 1} de {totalColumnPages}</span>
            <button
              onClick={() => setColumnPage((prev) => Math.min(prev + 1, totalColumnPages - 1))}
              disabled={columnPage === totalColumnPages - 1}
              className="px-3 py-1 bg-skyBlue text-white rounded disabled:opacity-50"
            >
              Siguiente
            </button>
          </div>
        )}
        {error && <div className="text-red-500 mb-4">{error}</div>}
        <div className="flex flex-col md:flex-row gap-6 w-full justify-center mt-2">
          <button
            className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
            onClick={handleExportExcel}
            disabled={loading}
          >
            {loading && (
              <svg className="animate-spin h-5 w-5 text-white dark:text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
            )}
            {loading ? "Exportando datos..." : "Exportar Excel"}
          </button>
          <button
            className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
            onClick={handleSaveToDB}
            disabled={saving}
          >
            {saving && (
              <svg className="animate-spin h-5 w-5 text-white dark:text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
            )}
            {saving ? "Guardando datos..." : "Guardar en BD"}
          </button>
          <button
            className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
            onClick={handleSaveToDB}
            disabled={loading}
          >
            Actualizar política
          </button>
        </div>
      </div>
    </div>
  );
}
