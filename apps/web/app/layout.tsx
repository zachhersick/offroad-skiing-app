import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TerrainPilot",
  description: "Workspace-first trip planning for off-road and ski enthusiasts."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

