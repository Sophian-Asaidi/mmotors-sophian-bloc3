import { useCallback, useEffect, useState } from "react";

import VehicleCard from "../components/VehicleCard.jsx";
import { api } from "../services/api.js";

export default function Search() {
  const [mode, setMode] = useState("sale");
  const [search, setSearch] = useState("");
  const [vehicles, setVehicles] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const loadVehicles = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getVehicles({ mode, search });
      setVehicles(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [mode, search]);

  useEffect(() => {
    loadVehicles();
  }, [loadVehicles]);

  return (
    <section>
      <div className="section-header">
        <div>
          <p className="eyebrow">Catalogue</p>
          <h1>Recherche véhicules</h1>
        </div>
        <div className="segmented" aria-label="Type de recherche">
          <button className={mode === "sale" ? "active" : ""} type="button" onClick={() => setMode("sale")}>
            Achat
          </button>
          <button className={mode === "rental" ? "active" : ""} type="button" onClick={() => setMode("rental")}>
            Location
          </button>
        </div>
      </div>

      <form className="search-bar" onSubmit={(event) => event.preventDefault()}>
        <label htmlFor="vehicle-search">Recherche</label>
        <input
          id="vehicle-search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Marque, modèle, énergie"
        />
        <button type="button" className="button" onClick={loadVehicles}>
          Filtrer
        </button>
      </form>

      {error && <p className="alert error">{error}</p>}
      {loading && <p>Chargement des véhicules...</p>}
      <div className="vehicle-grid">
        {vehicles.map((vehicle) => (
          <VehicleCard key={vehicle.id} vehicle={vehicle} />
        ))}
      </div>
    </section>
  );
}

