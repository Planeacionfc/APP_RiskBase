"use client";

import { Navbar } from "./nabar";
import { LogoPrebel } from "./logoPrebel";

export const Header = () => {
  return (
    <header className="grid grid-cols-3 h-full items-center p-4 text-cyan dark:text-bone bg-lightBlue/20 dark:bg-gray-400/10 backdrop-filter backdrop-blur-lg sticky top-0">
      <h1 className="text-2xl font-bold">Gestión de Proyectos PF</h1>
      <Navbar />
      <LogoPrebel />
    </header>
  );
};
