import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "RAG",
  description: "AI-driven enterprise document retrieval",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
