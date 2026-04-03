export default function TorusLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // No padding wrapper — torus page manages its own full-screen layout
  return <>{children}</>;
}
