import { useEffect, useState } from "react";

import { api } from "../services/api.js";

export default function AdminApplications() {
  const [applications, setApplications] = useState([]);
  const [comment, setComment] = useState("");
  const [error, setError] = useState("");

  const loadApplications = () =>
    api.getAdminApplications().then(setApplications).catch((err) => setError(err.message));

  useEffect(() => {
    loadApplications();
  }, []);

  const decide = async (applicationId, status) => {
    setError("");
    try {
      await api.updateApplicationStatus(applicationId, {
        status,
        admin_comment: comment || (status === "approved" ? "Dossier accepté." : "Dossier incomplet."),
      });
      setComment("");
      loadApplications();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section>
      <div className="section-header">
        <div>
          <p className="eyebrow">Back-office</p>
          <h1>Dossiers clients</h1>
        </div>
      </div>
      {error && <p className="alert error">{error}</p>}
      <div className="panel form-panel wide">
        <label htmlFor="admin-comment">Commentaire de décision</label>
        <input
          id="admin-comment"
          value={comment}
          onChange={(event) => setComment(event.target.value)}
          placeholder="Commentaire envoyé au client"
        />
      </div>
      <div className="table-panel">
        <table>
          <thead>
            <tr>
              <th>Client</th>
              <th>Véhicule</th>
              <th>Type</th>
              <th>Statut</th>
              <th>Documents</th>
              <th>Décision</th>
            </tr>
          </thead>
          <tbody>
            {applications.map((item) => (
              <tr key={item.id}>
                <td>{item.user_email}</td>
                <td>{item.vehicle_title}</td>
                <td>{item.application_type === "rental" ? "Location" : "Achat"}</td>
                <td>{item.status}</td>
                <td>{item.documents.length}</td>
                <td className="table-actions">
                  <button className="button" type="button" onClick={() => decide(item.id, "approved")}>
                    Valider
                  </button>
                  <button className="button danger" type="button" onClick={() => decide(item.id, "rejected")}>
                    Refuser
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

