import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import { api } from "../services/api.js";

export default function ApplicationForm() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [vehicles, setVehicles] = useState([]);
  const [vehicleId, setVehicleId] = useState(params.get("vehicleId") || "");
  const [applicationType, setApplicationType] = useState(params.get("type") || "purchase");
  const [message, setMessage] = useState("");
  const [files, setFiles] = useState([]);
  const [error, setError] = useState("");

  const selectedVehicle = useMemo(
    () => vehicles.find((vehicle) => String(vehicle.id) === String(vehicleId)),
    [vehicles, vehicleId],
  );

  useEffect(() => {
    api.getVehicles().then(setVehicles).catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    if (selectedVehicle) {
      setApplicationType(selectedVehicle.mode === "rental" ? "rental" : "purchase");
    }
  }, [selectedVehicle]);

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    const formData = new FormData();
    formData.append("vehicle_id", vehicleId);
    formData.append("application_type", applicationType);
    formData.append("message", message);
    files.forEach((file) => formData.append("documents", file));

    try {
      await api.createApplication(formData);
      navigate("/applications");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section className="auth-page">
      <form className="panel form-panel wide" onSubmit={onSubmit}>
        <p className="eyebrow">Dossier client</p>
        <h1>Déposer un dossier</h1>
        {error && <p className="alert error">{error}</p>}

        <label htmlFor="vehicle">Véhicule</label>
        <select id="vehicle" value={vehicleId} onChange={(event) => setVehicleId(event.target.value)} required>
          <option value="">Sélectionner un véhicule</option>
          {vehicles.map((vehicle) => (
            <option key={vehicle.id} value={vehicle.id}>
              {vehicle.brand} {vehicle.model} - {vehicle.mode === "rental" ? "Location" : "Achat"}
            </option>
          ))}
        </select>

        <label htmlFor="type">Type de dossier</label>
        <select
          id="type"
          value={applicationType}
          onChange={(event) => setApplicationType(event.target.value)}
          required
        >
          <option value="purchase">Achat</option>
          <option value="rental">Location</option>
        </select>

        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          rows="4"
          placeholder="Informations utiles pour l'étude du dossier"
        />

        <label htmlFor="documents">Documents justificatifs</label>
        <input
          id="documents"
          type="file"
          multiple
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={(event) => setFiles(Array.from(event.target.files))}
        />

        <button className="button" type="submit">
          Envoyer le dossier
        </button>
      </form>
    </section>
  );
}

