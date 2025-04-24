"use client";
import React, { useEffect, useState } from "react";
import type { ReactNode } from "react";
import Swal from "sweetalert2";
import { DataGrid, type Column } from "react-data-grid";
import "react-data-grid/lib/styles.css";

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
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Recupera el token JWT almacenado en localStorage
const getToken = () => {
  return localStorage.getItem("token");
};

const fetchMatrices = async (): Promise<{ matrices: MatrizRow[] }> => {
  const token = getToken();
  const res = await fetch(`${API_URL}/risk/matrices-view`, {
    credentials: "include",
    headers: token ? { "Authorization": `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error("Error al obtener matrices");
  return res.json();
};

const updateMatrices = async (rows: MatrizRow[]) => {
  const token = getToken();
  const res = await fetch(`${API_URL}/risk/matrices-save`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { "Authorization": `Bearer ${token}` } : {})
    },
    body: JSON.stringify({ rows }),
    credentials: "include"
  });
  return res.json();
};

export default function MatricesPage() {
  const [rows, setRows] = useState<MatrizRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorRows, setErrorRows] = useState<number[]>([]);

  useEffect(() => {
    setLoading(true);
    fetchMatrices()
      .then((data) => setRows(data.matrices || []))
      .catch(() =>
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "No se pudieron obtener las matrices.",
        })
      )
      .finally(() => setLoading(false));
  }, []);

  const columns: Column<MatrizRow>[] = [
    { key: "id_politica_base_riesgo", name: "ID Política", editable: true },
    { key: "concatenado", name: "Concatenado", editable: true },
    { key: "segmento", name: "Segmento", editable: true },
    { key: "permanencia", name: "Permanencia", editable: true },
    { key: "factor_prov", name: "Factor Prov", editable: true },
    { key: "clasificacion", name: "Clasificación", editable: true },
    { key: "tipo_matriz", name: "Tipo Matriz", editable: true },
    { key: "subsegmento", name: "Subsegmento", editable: true },
    { key: "estado", name: "Estado", editable: true },
    { key: "cobertura", name: "Cobertura", editable: true },
    { key: "negocio", name: "Negocio", editable: true },
  ];

  const onRowsChange = (newRows: MatrizRow[], { indexes }: { indexes: number[] }) => {
    setRows(newRows);
    setErrorRows((prev) => prev.filter((i) => !indexes.includes(i)));
  };

  const handleSave = async () => {
    setLoading(true);
    // Solo enviar filas modificadas (por ahora, enviar todas)
    try {
      const result = await updateMatrices(rows);
      if (result.success) {
        Swal.fire({
          icon: "success",
          title: "Cambios guardados",
          text: result.message || "Los cambios se guardaron correctamente.",
        });
        setErrorRows([]);
      } else {
        setErrorRows(result.errorRows || []);
        Swal.fire({
          icon: "error",
          title: "Error al guardar",
          text: result.message || "Algunas filas no se pudieron guardar.",
        });
      }
    } catch (e) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "No se pudo guardar los cambios.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Editar Matrices de Política de Riesgo</h1>
      <div className="bg-white dark:bg-bone rounded-lg shadow p-4 mb-6">
        <DataGrid
          columns={columns}
          rows={rows}
          onRowsChange={onRowsChange}
          rowKeyGetter={row => row.id_politica_base_riesgo}
          className="rdg-light"
          rowClass={(row: MatrizRow) =>
            errorRows.includes(row.id_politica_base_riesgo)
              ? "bg-red-100 dark:bg-red-200"
              : ""
          }
          style={{ minHeight: 500 }}
        />
      </div>
      <button
        className="px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl flex items-center justify-center gap-2"
        onClick={handleSave}
        disabled={loading}
      >
        Guardar cambios
      </button>
    </main>
  );
}
