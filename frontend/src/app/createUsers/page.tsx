// src/app/createUsers/page.tsx
"use client";
import React, { useState } from "react";
import { showAlert } from "../../utils/swal";
import { jwtDecode } from "jwt-decode";

// --- INTERFAZ PARA JWT ---
interface JwtPayloadWithRole {
  role?: string;
  [key: string]: any;
}

// ALERTA 403 PARA ACCIONES DE ADMIN
const show403Alert = async () => {
  await showAlert({
    position: "center",
    icon: "warning",
    title: "Permiso denegado",
    text: "No tienes permisos para realizar esta acción. Si crees que es un error, contacta al administrador.",
    showConfirmButton: true,
    confirmButtonText: "OK",
  });
};

// Función para validar el rol de administrador
function checkAdminRole(): boolean {
  if (typeof window === "undefined") return false;
  const token = localStorage.getItem("token");
  if (!token) return false;
  try {
    const payload = jwtDecode<JwtPayloadWithRole>(token);
    return payload.role === "admin";
  } catch {
    return false;
  }
}

const roles = [
  { value: "user", label: "Regular" },
  { value: "admin", label: "Administrador" },
];

export default function CreateUsersPage() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL!;
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: roles[0].value,
  });
  const [saving, setSaving] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // 1. Validar rol de admin antes de llamar al endpoint
    if (!checkAdminRole()) {
      await show403Alert();
      return;
    }

    setSaving(true);
    try {
      const token = localStorage.getItem("token") || "";
      const headers: Record<string,string> = {
        "Content-Type": "application/json",
      };
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers,
        body: JSON.stringify(form),
      });
      const data = await res.json();

      if (res.status === 201) {
        await showAlert({
          position: "center",
          icon: "success",
          title: "Usuario creado",
          text: `El usuario "${data.username}" fue registrado exitosamente.`,
          showConfirmButton: true,
          confirmButtonText: "OK",
        });
        setForm({
          username: "",
          email: "",
          password: "",
          role: roles[0].value,
        });
      } else if (res.status === 401 || res.status === 403) {
        await show403Alert();
      } else {
        throw new Error(data.detail || "Error al crear usuario");
      }
    } catch (err: any) {
      await showAlert({ position: "center", icon: "error", title: "Error", text: err.message, showConfirmButton: true, confirmButtonText: "OK" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white dark:bg-[#2c3e64] rounded-lg shadow">
      <h1 className="text-2xl font-bold mb-6 text-center">
        Crear Nuevo Usuario
      </h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Username */}
        <div>
          <label htmlFor="username" className="block mb-1 font-medium">
            Usuario
          </label>
          <input
            id="username"
            name="username"
            type="text"
            value={form.username}
            onChange={handleChange}
            required
            placeholder="ej: usuario.ejemplo"
            className="w-full px-3 py-2 border rounded focus:outline-none"
          />
        </div>

        {/* Email */}
        <div>
          <label htmlFor="email" className="block mb-1 font-medium">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            required
            placeholder="ej: usuario@empresa.com"
            className="w-full px-3 py-2 border rounded focus:outline-none"
          />
        </div>

        {/* Contraseña */}
        <div>
          <label htmlFor="password" className="block mb-1 font-medium">
            Contraseña
          </label>
          <input
            id="password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
            placeholder="mínimo 8 caracteres"
            className="w-full px-3 py-2 border rounded focus:outline-none"
          />
        </div>

        {/* Rol */}
        <div>
          <label htmlFor="role" className="block mb-1 font-medium">
            Rol
          </label>
          <select
            id="role"
            name="role"
            value={form.role}
            onChange={handleChange}
            className="
              w-full 
              px-4        
              py-3        
              text-lg     
              h-12        
              border 
              rounded 
              focus:outline-none 
              focus:ring-2 
              focus:ring-skyBlue 
              bg-white dark:bg-[#2c3e64] 
              text-gray-800 dark:text-gray-200
            "
          >
            {roles.map((r) => (
              <option key={r.value} value={r.value}>
                {r.label}
              </option>
            ))}
          </select>
        </div>

        {/* Botón */}
        <div className="flex justify-center">
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-8 py-3 bg-skyBlue hover:bg-[#4278FA]/80 dark:bg-bone dark:hover:bg-bone/80 text-white dark:text-black font-semibold rounded-lg shadow transition-colors duration-200 text-xl"
          >
            {saving && (
              <svg
                className="animate-spin h-5 w-5 text-white dark:text-black"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                ></path>
              </svg>
            )}
            {saving ? "Creando..." : "Crear Usuario"}
          </button>
        </div>
      </form>
    </div>
  );
}
