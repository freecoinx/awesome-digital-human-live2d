import type { Metadata } from "next";
// import { Inter } from "next/font/google";
import { PROJ_NAME, PROJ_DESC } from "@/app/lib/constants";
import { HeroUIProvider } from "@heroui/react";
import Header from "@/app/ui/common/header/header";
import "./globals.css";
// const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: PROJ_NAME,
  description: PROJ_DESC,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        {/* <script src="https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js" /> */}
        {/* use local */}
        <script src="/live2d/live2dcubismcore.min.js" />
      </head>
      <body>
        <HeroUIProvider>
          {/* <div className={`${inter.className} flex flex-col h-screen`}> */}
          <div className="flex flex-col h-screen">
            <Header />
            {children}
          </div>
        </HeroUIProvider>
      </body>
    </html>
  );
}
