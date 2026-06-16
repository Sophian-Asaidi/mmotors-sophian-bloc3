import { Link } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export default function CustomerDashboard() {
  const { user } = useAuth();

  return (
    <section>
      <div className="section-header">
        <div>
          <p className="eyebrow">Espace client</p>
          <h1>Bonjour {user?.email}</h1>
        </div>
      </div>
      <div className="dashboard-grid">
        <article className="panel">
          <h2>Rechercher</h2>
          <p>Trouver un véhicule disponible à l'achat ou en location longue durée.</p>
          <Link className="button" to="/search">
            Voir les véhicules
          </Link>
        </article>
        <article className="panel">
          <h2>Déposer un dossier</h2>
          <p>Joindre les justificatifs et transmettre la demande à M-Motors.</p>
          <Link className="button secondary" to="/applications/new">
            Nouveau dossier
          </Link>
        </article>
        <article className="panel">
          <h2>Suivi</h2>
          <p>Consulter les décisions et commentaires de l'administration.</p>
          <Link className="button secondary" to="/applications">
            Mes dossiers
          </Link>
        </article>
      </div>
    </section>
  );
}

