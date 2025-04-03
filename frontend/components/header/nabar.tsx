import Link from "next/link";
import ToggleTheme from "../theme/toggleTheme";

export const Navbar = () => {
  return (
    <section className="flex items-center w-full ">
      <nav className="w-full">
        <ul className="flex gap-4 justify-center">
          <li>
            <Link
              href="/login"
              className="border-b-4 hover:border-current border-transparent flex gap-1 items-center"
            >
              Cerrar sesión
            </Link>
          </li>
          <li>
            <Link
              href="/"
              className="border-b-4 hover:border-current border-transparent flex gap-1 items-center"
            >
<<<<<<< HEAD
              Inicio <HomeIcon className="w-6 h-6 fill-cyan dark:fill-bone" />
=======
              Inicio 
>>>>>>> 24d0f0cb67a48cc001f914358322380b28cca599
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
