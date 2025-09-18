export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-dvh antialiased">
        <div className="mx-auto max-w-5xl p-4 md:p-8">{children}</div>
      </body>
    </html>
  );
}
