import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { ConditionalHeader } from "../../components/header/ConditionalHeader";
import { ThemeProvider } from "next-themes";

const FFFAcid = localFont({
  src: "./fonts/FFFAcidGroteskVariableTRIALVF.woff",
});

const acidGroteskLight = localFont({ src: "./fonts/acid-grotesk-light.woff" });

export const metadata: Metadata = {
  title: "ManagerPF",
  description: "Aplicativo de Planeación Financiera para gestionar proyectos",
  icons: {
    icon: "/image/prebel_favicon.png"
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body
        className={`${acidGroteskLight.className} ${FFFAcid.className}  antialiased  text-[#202020] dark:text-bone bg-radial from-bone via-bone to-white dark:from-skyBlue dark:via-none dark:to-[#202020] `}
      >
        <ThemeProvider attribute="class" enableSystem defaultTheme="system">
          <ConditionalHeader />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
