"use client";
import React, { useState, useEffect } from "react";
import Swal from "sweetalert2";
import { DataGrid, GridColDef, GridRowsProp, GridToolbar } from '@mui/x-data-grid';
import { Box } from '@mui/material';

interface MatrizRow {
  id_politica_base_riesgo: number;
  concatenado: string;
  segmento: string;
  permanencia: string;
  factor_prov: number;
  clasificacion: string;
  tipo_matriz: string;
  subsegmento: string;
  estado: string;
  cobertura: string;
  negocio: string;
  [key: string]: any;
}

interface MatrizUpdatePayload {
  id_politica_base_riesgo: number;
  concatenado: string;
  segmento: string;
  permanencia: string;
  factor_prov: number;
  clasificacion: string;
  tipo_matriz: string;
  subsegmento: string;
  estado: string;
  cobertura: string;
  negocio: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Recupera el token JWT almacenado en localStorage
const getToken = () => localStorage.getItem("token");

// Llama al endpoint para obtener las matrices
const fetchMatrices = async (): Promise<{ matrices: MatrizRow[] }> => {
  const token = getToken();
  const res = await fetch(`${API_URL}/risk/matrices-view`, {
    credentials: "include",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error("Error al obtener matrices");
  return res.json();
};

// Llama al endpoint para guardar los cambios
const updateMatrices = async (payload: { rows: MatrizUpdatePayload[] }) => {
  const token = getToken();
  const res = await fetch(`${API_URL}/risk/matrices-save`, {
    method: "PUT",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(payload),
  });
  return res.json();
};

export default function MatricesPage() {
  const [rows, setRows] = useState<MatrizRow[]>([]);
  const [originalRows, setOriginalRows] = useState<MatrizRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorRows, setErrorRows] = useState<number[]>([]);
  const [selectionModel, setSelectionModel] = useState<(number | string)[]>([]);

  // Al montar, traemos las matrices
  useEffect(() => {
    setLoading(true);
    fetchMatrices()
      .then((data) => {
        setRows(data.matrices || []);
        setOriginalRows(data.matrices || []);
      })
      .catch(() =>
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "No se pudieron obtener las matrices.",
        })
      )
      .finally(() => setLoading(false));
  }, []);

  const processRowUpdate = async (newRow: MatrizRow) => {
    const updatedRows = rows.map((row) =>
      row.id_politica_base_riesgo === newRow.id_politica_base_riesgo ? newRow : row
    );
    setRows(updatedRows);
    return newRow;
  };

  // Columnas para MUI DataGrid
  const columns: GridColDef[] = [
    { field: "id_politica_base_riesgo", headerName: "ID Política", width: 120, editable: false },
    { field: "concatenado", headerName: "Concatenado", width: 180, editable: false },
    { field: "segmento", headerName: "Segmento", width: 140, editable: false },
    { field: "permanencia", headerName: "Permanencia", width: 140, editable: false },
    { field: "factor_prov", headerName: "Factor Prov", width: 120, editable: true, type: 'number' },
    { field: "clasificacion", headerName: "Clasificación", width: 140, editable: true },
    { field: "tipo_matriz", headerName: "Tipo Matriz", width: 140, editable: false },
    { field: "subsegmento", headerName: "Subsegmento", width: 140, editable: false },
    { field: "estado", headerName: "Estado", width: 120, editable: false },
    { field: "cobertura", headerName: "Cobertura", width: 120, editable: false },
    { field: "negocio", headerName: "Negocio", width: 120, editable: false },
  ];

  // Guarda los cambios al backend
  const handleSave = async () => {
    setLoading(true);
    try {
      // Solo filas modificadas en cualquier campo editable excepto el id
      const modifiedRows = rows.filter(row => {
        const original = originalRows.find(r => r.id_politica_base_riesgo === row.id_politica_base_riesgo);
        if (!original) return false;
        // Compara TODOS los campos editables excepto el id
        return (
          row.concatenado !== original.concatenado ||
          row.segmento !== original.segmento ||
          row.permanencia !== original.permanencia ||
          row.factor_prov !== original.factor_prov ||
          row.clasificacion !== original.clasificacion ||
          row.tipo_matriz !== original.tipo_matriz ||
          row.subsegmento !== original.subsegmento ||
          row.estado !== original.estado ||
          row.cobertura !== original.cobertura ||
          row.negocio !== original.negocio
        );
      }).map(row => ({
        id_politica_base_riesgo: row.id_politica_base_riesgo,
        concatenado: row.concatenado,
        segmento: row.segmento,
        permanencia: row.permanencia,
        factor_prov: row.factor_prov,
        clasificacion: row.clasificacion,
        tipo_matriz: row.tipo_matriz,
        subsegmento: row.subsegmento,
        estado: row.estado,
        cobertura: row.cobertura,
        negocio: row.negocio
      }));
      if (modifiedRows.length === 0) {
        Swal.fire({
          icon: "info",
          title: "Sin cambios",
          text: "No hay cambios para guardar.",
        });
        setLoading(false);
        return;
      }
      const result = await updateMatrices({ rows: modifiedRows });
      if (result.success) {
        Swal.fire({
          icon: "success",
          title: "Cambios guardados",
          text: "Los cambios se guardaron correctamente.",
        });
        setErrorRows([]);
        setOriginalRows(rows);
      } else {
        setErrorRows(result.errorRows || []);
        Swal.fire({
          icon: "error",
          title: "Error al guardar",
          text: result.message || "Algunas filas no se pudieron guardar.",
        });
      }
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error inesperado",
        text: "Ocurrió un error al intentar guardar los cambios.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto p-2">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Actualizar políticas de base de riesgo
      </h1>

      <p className="text-center text-gray-700 dark:text-gray-300 mb-8">
        En esta sección se realizan las actualizaciones de la política de la base de riesgo.
        <span className="bg-yellow-100 text-yellow-800 p-2 rounded-lg block mt-4">
          <strong>Nota:</strong> Trata de evitar errores ortográficos o de sintaxis y seguir el mismo formato que ves en la tabla.
          Puedes filtrar, organizar y ocultar columnas para facilitar la edición.
        </span>
      </p>
      <Box className="bg-white dark:bg-[#232836] rounded-lg shadow p-3 mb-6" sx={{ height: 700, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          getRowId={(row) => row.id_politica_base_riesgo}
          loading={loading}
          disableRowSelectionOnClick
          processRowUpdate={processRowUpdate}
          onRowSelectionModelChange={(ids) => setSelectionModel(Array.isArray(ids) ? ids : [])}
          slots={{ toolbar: GridToolbar }}
          sx={{ fontSize: 15 }}
          pageSizeOptions={[10, 25, 50, 100]}
          initialState={{
            pagination: { paginationModel: { pageSize: 25, page: 0 } },
            columns: { columnVisibilityModel: { concatenado: true } }
          }}
        />
      </Box>
      <Box display="flex" justifyContent="space-between" width="100%" mt={2}>
        <button
          className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
          onClick={() => window.location.href = "/riskbase"}
          style={{ minWidth: 180 }}
        >
          Volver a Base de Riesgo
        </button>
        <button
          className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
          onClick={handleSave}
          disabled={loading}
          style={{ minWidth: 180 }}
        >
          {loading && (
            <svg className="animate-spin h-5 w-5 text-white dark:text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
          )}
          {loading ? "Guardando..." : "Guardar cambios"}
        </button>
      </Box>
    </main>
  );
}
