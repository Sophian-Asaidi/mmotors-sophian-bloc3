import { Link } from "react-router-dom";

export default function AdminDashboard() {
  return (
    <section>
      <div className="section-header">
        <div>
          <p className="eyebrow">Back-office</p>
          <h1>Administration</h1>
        </div>
      </div>
      <div className="dashboard-grid">
        <article className="panel">
          <h2>Véhicules</h2>
          <p>Ajouter des véhicules à vendre ou à louer, puis basculer leur mode commercial.</p>
          <Link className="button" to="/admin/vehicles">
            Gérer les véhicules
          </Link>
        </article>
        <article className="panel">
          <h2>Dossiers</h2>
          <p>Consulter les demandes clients et saisir une décision argumentée.</p>
          <Link className="button secondary" to="/admin/applications">
            Gérer les dossiers
          </Link>
        </article>
      </div>
    </section>
  );
}

