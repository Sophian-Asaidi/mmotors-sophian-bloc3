import { useEffect, useState } from "react";

import { api } from "../services/api.js";

const LABELS = {
  pending: "En attente",
  approved: "Validé",
  rejected: "Refusé",
};

export default function ApplicationStatus() {
  const [applications, setApplications] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api.getMyApplications().then(setApplications).catch((err) => setError(err.message));
  }, []);

  return (
    <section>
      <div className="section-header">
        <div>
          <p className="eyebrow">Suivi</p>
          <h1>Mes dossiers</h1>
        </div>
      </div>
      {error && <p className="alert error">{error}</p>}
      <div className="table-panel">
        <table>
          <thead>
            <tr>
              <th>Véhicule</th>
              <th>Type</th>
              <th>Statut</th>
              <th>Documents</th>
              <th>Commentaire</th>
            </tr>
          </thead>
          <tbody>
            {applications.map((item) => (
              <tr key={item.id}>
                <td>{item.vehicle_title}</td>
                <td>{item.application_type === "rental" ? "Location" : "Achat"}</td>
                <td>
                  <span className={`status status-${item.status}`}>{LABELS[item.status]}</span>
                </td>
                <td>{item.documents.length}</td>
                <td>{item.admin_comment || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

