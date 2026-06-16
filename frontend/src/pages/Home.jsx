import { Link } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export default function Home() {
  const { user } = useAuth();

  return (
    <section className="page-grid">
      <div className="panel intro-panel">
        <p className="eyebrow">Vente et location longue durée</p>
        <h1>M-Motors</h1>
        <p>
          Recherchez un véhicule d'occasion, choisissez achat ou location avec option d'achat,
          puis suivez votre dossier depuis votre espace client.
        </p>
        <div className="actions">
          <Link className="button" to="/search">
            Rechercher un véhicule
          </Link>
          <Link className="button secondary" to={user ? "/applications" : "/login"}>
            Suivre un dossier
          </Link>
        </div>
      </div>
      <div className="panel checklist-panel">
        <h2>Dossier 100 % dématérialisé</h2>
        <ul className="clean-list">
          <li>Création de compte sécurisée</li>
          <li>Téléversement des justificatifs</li>
          <li>Suivi du statut en temps réel</li>
          <li>Validation ou refus par un administrateur</li>
        </ul>
      </div>
    </section>
  );
}

