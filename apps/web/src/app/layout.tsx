import type { Metadata } from "next";
import { Providers } from "./providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Pulse",
  description: "Create a poll, share it, watch the results roll in.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <Providers>
          <main className="mx-auto max-w-2xl px-4 py-10">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
