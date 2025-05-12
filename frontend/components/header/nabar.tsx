import Link from "next/link";
import ToggleTheme from "../theme/toggleTheme";
import HomeIcon from "@/icons/homeIcon";

export const Navbar = () => {
  // Función para cerrar sesión
  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('token_type');
    }
  };

  return (
    <section className="flex items-center w-full ">
      <nav className="w-full">
        <ul className="flex gap-4 justify-center">
          <li>
            <Link
              href="/login"
              className="border-b-4 hover:border-current border-transparent flex gap-1 items-center"
              onClick={handleLogout}
            >
              Cerrar sesión
            </Link>
          </li>
          <li>
            <Link
              href="/createUsers"
              className="border-b-4 hover:border-current border-transparent flex gap-1 items-center"
            >
              Crear usuarios
            </Link>
          </li>
          <li>
            <Link
              href="/"
              className="border-b-4 hover:border-current border-transparent flex gap-1 items-center"
            >
              Inicio <HomeIcon className="w-6 h-6 fill-cyan dark:fill-bone" />
            </Link>
          </li>
          <li>
            <ToggleTheme />
          </li>
        </ul>
      </nav>
    </section>
  );
};
