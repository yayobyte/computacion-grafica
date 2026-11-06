import { Suspense } from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { ThemeProvider } from "./theme/ThemeProvider";
import { HomePage } from "./home/HomePage";
import { PROYECTOS } from "./proyectos/registro";

function NoEncontrada() {
  return (
    <main className="home">
      <h1>Página no encontrada</h1>
      <p>
        Esta dirección no corresponde a ningún proyecto. <Link to="/">Volver al inicio</Link>.
      </p>
    </main>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Suspense fallback={<p className="suave" style={{ padding: 24 }}>Cargando…</p>}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            {PROYECTOS.map(({ id, pagina: Pagina }) => (
              <Route key={id} path={`/${id}`} element={<Pagina />} />
            ))}
            <Route path="*" element={<NoEncontrada />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ThemeProvider>
  );
}
