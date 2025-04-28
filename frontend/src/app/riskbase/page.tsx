"use client";
import React, { useState } from "react";
import { showAlert } from "../../utils/swal";

export default function RiskBasePage() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const [data, setData] = useState<any[]>([]); // Dataframe dinámico
  const [columns, setColumns] = useState<string[]>([]); // Columnas dinámicas
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [extracting, setExtracting] = useState(false);
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

  // Llama a /risk/process (con o sin mes/anio) y luego obtiene los datos desde /risk/data-view
  const callProcess = async (mes?: number, anio?: number) => {
    setProcessing(true);
    setError("");
    try {
      const token = getToken();
      let url = `${API_URL}/risk/process`;
      if (mes && anio) url += `?mes=${mes}&anio=${anio}`;
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });
      if (response.status === 401) {
        await showAlert({
          icon: 'error',
          title: 'No autorizado',
          text: 'No estás autorizado o tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
        });
        setProcessing(false);
        return;
      }
      if (!response.ok) {
        await showAlert({
          position: "center",
          icon: "error",
          title: "Error al procesar datos",
          text: "Ocurrió un error al procesar los datos. Por favor, inténtalo nuevamente o contacta al administrador.",
          showConfirmButton: true,
          confirmButtonText: "OK"
        });
        setProcessing(false);
        return;
      }
      const result = await response.json();
      const excelFileName = result.excel_file;
      if (!excelFileName) {
        await showAlert({
          position: "center",
          icon: "error",
          title: "Error al procesar datos",
          text: "Ocurrió un error al procesar los datos. Por favor, inténtalo nuevamente o contacta al administrador.",
          showConfirmButton: true,
          confirmButtonText: "OK"
        });
        setProcessing(false);
        return;
      }
      setExcelFile(excelFileName);
      
      // Obtener los datos procesados desde /risk/data-view
      const dfRes = await fetch(`${API_URL}/risk/data-view?temp_file=${excelFileName}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (dfRes.status === 401) {
        await showAlert({
          icon: 'error',
          title: 'No autorizado',
          text: 'No estás autorizado o tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
        });
        setProcessing(false);
        return;
      }
      if (!dfRes.ok) {
        await showAlert({
          position: "center",
          icon: "error",
          title: "Error al obtener los datos procesados",
          text: "Ocurrió un error al obtener los datos procesados. Por favor, inténtalo nuevamente o contacta al administrador.",
          showConfirmButton: true,
          confirmButtonText: "OK"
        });
        setProcessing(false);
        return;
      }
      const df = await dfRes.json();
      setColumns(df.columns || []);
      setData((df.data || []).map((row: any) => {
        const rowObj: any = {};
        (df.columns || []).forEach((col: string) => {
          rowObj[col] = row[col];
        });
        return rowObj;
      }));
      await showAlert({
        position: "center",
        icon: 'success',
        title: '¡Proceso finalizado!',
        text: 'El proceso ha terminado exitosamente.',
        showConfirmButton: true,
        confirmButtonText: 'OK'
      });
    } catch (err: any) {
      setError(err.message || "Error inesperado");
    } finally {
      setProcessing(false);
    }
  };

  // Procesar: llama a callProcess() sin parámetros
  const handleProcess = async () => {
    await callProcess();
  };

  // Consultar por mes y año
  const handleConsult = async () => {
    
    const Swal = (await import('sweetalert2')).default;
    const { value } = await Swal.fire({
      title: "Consultar registros de Base de Riesgo",
      icon: 'info',
      html: `
        <p>Por favor, ingresa el mes y año para consultar los registros.</p>
        <input id="swal-mes"  class="swal2-input" placeholder="Mes"  type="number" min="1" max="12" style="border: 2px solid #4d5461; border-radius: 6px; box-shadow: 0 0 0 1px #4d5461; color: #202020; background: #fff;" />
        <input id="swal-anio" class="swal2-input" placeholder="Año" type="number" style="border: 2px solid #4d5461; border-radius: 6px; box-shadow: 0 0 0 1px #4d5461; color: #202020; background: #fff;" />
        <style>
          #swal-mes::placeholder, #swal-anio::placeholder {
            color: #444 !important;
            opacity: 1 !important;
          }
        </style>
      `,
      preConfirm: () => {
        const mes  = Number((document.getElementById("swal-mes")  as HTMLInputElement).value);
        const anio = Number((document.getElementById("swal-anio") as HTMLInputElement).value);
        if(!mes||mes<1||mes>12||!anio) Swal.showValidationMessage("Por favor ingresa un mes de 1-12 y un año válido");
        return {mes,anio};
      },
      showCancelButton: true, confirmButtonText:"Consultar"
    });
    if(value) await callProcess(value.mes, value.anio);
  };

  // Guardar en BD con confirmación
  const handleSaveToDB = async () => {
    const confirm = await showAlert({
      position: "center",
      title: '¿Estás seguro?',
      text: '¿Deseas guardar los datos en la base de datos? Esta acción eliminará el archivo temporal.',
      icon: 'warning',
      confirmButtonText: 'Sí, guardar',
      cancelButtonText: 'Cancelar',
      showConfirmButton: true,
      showCancelButton: true,
      reverseButtons: true
    });
    if (!confirm.isConfirmed) return;

    setSaving(true);
    setError("");
    try {
      const token = getToken();
      if (!excelFile) {
        await showAlert({
          position: "center",
          icon: "error",
          title: "No hay archivo Excel generado",
          text: "Primero debes procesar los datos y generar el archivo Excel antes de guardar en la base de datos.",
          showConfirmButton: true,
          confirmButtonText: "OK"
        });
        setSaving(false);
        return;
      }
      const response = await fetch(`${API_URL}/risk/save-to-db`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ filename: excelFile })
      });
      if (response.status === 401) {
        await showAlert({
          icon: 'error',
          title: 'No autorizado',
          text: 'No estás autorizado o tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
        });
        setSaving(false);
        return;
      }
      if (!response.ok) {
        await showAlert({
          position: "center",
          icon: "error",
          title: "Error al guardar en BD",
          text: "Ocurrió un error al guardar los datos en la base de datos. Por favor, inténtalo nuevamente o contacta al administrador.",
          showConfirmButton: true,
          confirmButtonText: "OK"
        });
        throw new Error("Error al guardar en BD");
      }
      // Eliminar el archivo temporal después de guardar en BD
      await fetch(`${API_URL}/risk/delete-temp-file?filename=${excelFile}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      await showAlert({
        position: "center",
        icon: 'success',
        title: '¡Proceso finalizado!',
        text: 'Datos guardados exitosamente.',
        showConfirmButton: true,
        confirmButtonText: 'OK',
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
      if (!excelFile) {
        await showAlert({
          position: "center",
          icon: "error",
          title: "No hay archivo Excel generado",
          text: "Primero debes procesar los datos y generar el archivo Excel antes de exportar.",
          showConfirmButton: true,
          confirmButtonText: "OK"
        });
        setLoading(false);
        return;
      }
      const response = await fetch(`${API_URL}/risk/export-excel?filename=${excelFile}`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (response.status === 401) {
        await showAlert({
          icon: 'error',
          title: 'No autorizado',
          text: 'No estás autorizado o tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
        });
        setLoading(false);
        return;
      }
      if (!response.ok) {
        await showAlert({
          position: "center",
          icon: "error",
          title: "Error al exportar Excel",
          text: "Ocurrió un error al exportar los datos a Excel. Por favor, inténtalo nuevamente o contacta al administrador.",
          showConfirmButton: true,
          confirmButtonText: "OK"
        });
        throw new Error("Error al exportar Excel");
      }
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
      <h1 className="text-3xl md:text-4xl font-bold mb-8 mt-2 text-center text-skyBlue dark:text-bone">Procesamiento de Base de Riesgo</h1>
      <p className="text-center text-gray-700 dark:text-gray-300 mb-8">
        En esta sección se realizan los procesos de extracción, transformación y carga de datos de la base de riesgo.
        El proceso completo implica extracción de datos de SAP, procesamiento de columnas y carga en la base de datos.
        Luego, se puede exportar el resultado a un archivo Excel.
        También es posible consultar información de la base de riesgo que ha sido almacenada en la base de datos de meses anteriores
        y actualizar su política.
        <span className="bg-yellow-100 text-yellow-800 p-2 rounded-lg block mt-4">
          <strong>Nota:</strong> Primero debe descargar el archivo Excel y luego guardar la información en la base de datos.
          Al subir la información a la base de datos se elimina el archivo temporal con la información y deberá realizar el proceso nuevamente.
        </span>
      </p>
      

      <div className="w-full max-w-9xl flex flex-col items-center bg-white/80 dark:bg-[#2c3e64] rounded-xl shadow-black shadow-md p-12">
        <div className="flex flex-col md:flex-row gap-6 w-full justify-center mt-2 mb-6">
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
            {processing ? "Procesando..." : "Procesar base riesgo"}
          </button>
          <button
            className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
            onClick={handleConsult}
            disabled={extracting}
          >
            {extracting && (
              <svg className="animate-spin h-5 w-5 text-white dark:text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
              </svg>
            )}
            {extracting ? "Consultando..." : "Consultar base riesgo"}
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
            onClick={() => window.location.href = "/matrices"}
            disabled={loading}
          >
            Actualizar política
          </button>
        </div>
      </div>
    </div>
  );
}
