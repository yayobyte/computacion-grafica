import { useEffect } from "react";
import { Link } from "react-router-dom";
import { Trazo } from "../sketch/Trazo";
import { PROYECTOS } from "../proyectos/registro";
import "./home.css";

/** Menú inicial: una tarjeta por proyecto del registro. */
export function HomePage() {
  useEffect(() => {
    document.title = "Computación Gráfica · UTP";
  }, []);

  return (
    <main className="home">
      <header className="home-cabecera">
        <h1>
          Computación Gráfica
          <span className="home-subrayado" aria-hidden="true">
            <Trazo forma="lineaInferior" trazo="var(--acento)" grosor={3} margen={2} />
          </span>
        </h1>
        <p className="suave">Universidad Tecnológica de Pereira · proyectos del curso</p>
      </header>

      <section className="home-proyectos" aria-label="Proyectos">
        {PROYECTOS.map((p) => (
          <Link key={p.id} to={`/${p.id}`} className="home-tarjeta">
            <Trazo relleno="var(--acento-suave)" estiloRelleno="hachure" />
            <span className="home-unidad">{p.unidad}</span>
            <h2>{p.titulo}</h2>
            <p>{p.descripcion}</p>
            <span className="home-temas suave">{p.temas.join(" · ")}</span>
            <span className="home-abrir">Abrir →</span>
          </Link>
        ))}
      </section>
    </main>
  );
}
