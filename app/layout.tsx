import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import { mantineTheme } from "./theme";




export const metadata: Metadata = {
  title: "TableauLab",
  description: "Tableau Tool",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
    >
      
      <body>
        <MantineProvider
        theme={mantineTheme}>{children}</MantineProvider>
        
        </body>

    </html>
  );
}