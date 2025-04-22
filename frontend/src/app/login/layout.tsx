"use client";
import { ThemeProvider } from "next-themes";
import localFont from "next/font/local";
import "../globals.css";

const FFFAcid = localFont({
  src: "../fonts/FFFAcidGroteskVariableTRIALVF.woff",
});
const acidGroteskLight = localFont({ src: "../fonts/acid-grotesk-light.woff" });

export default function LoginLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" enableSystem defaultTheme="system">
      <div className={`${acidGroteskLight.className} ${FFFAcid.className} antialiased text-[#202020] dark:text-bone bg-radial from-bone via-bone to-white dark:from-skyBlue dark:via-none dark:to-[#202020] min-h-screen`}>
        {children}
      </div>
    </ThemeProvider>
  );
}