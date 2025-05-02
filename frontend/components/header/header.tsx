"use client";

import { Navbar } from "./nabar";
import { LogoPrebel } from "./logoPrebel";

export const Header = () => {
  return (
    <header className="grid grid-cols-3 h-full items-center p-4 text-cyan dark:text-bone bg-lightBlue/20 dark:bg-gray-400/10 backdrop-filter backdrop-blur-lg sticky top-0">
      <p className="text-2xl font-bold">Manager PF</p>
      <Navbar />
      <LogoPrebel />
    </header>
  );
};
