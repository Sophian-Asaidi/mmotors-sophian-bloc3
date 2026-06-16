import { useEffect, useState } from "react";

import { api } from "../services/api.js";

const initialForm = {
  brand: "",
  model: "",
  year: new Date().getFullYear(),
  mileage: 0,
  price: "",
  monthly_price: "",
  energy: "Essence",
  transmission: "Manuelle",
  mode: "sale",
  status: "available",
};

function normalizeVehiclePayload(form) {
  return {
    ...form,
    year: Number(form.year),
    mileage: Number(form.mileage),
    price: form.price === "" ? null : Number(form.price),
    monthly_price: form.monthly_price === "" ? null : Number(form.monthly_price),
  };
}

export default function AdminVehicles() {
  const [form, setForm] = useState(initialForm);
  const [vehicles, setVehicles] = useState([]);
  const [error, setError] = useState("");

  const loadVehicles = () => api.getVehicles().then(setVehicles).catch((err) => setError(err.message));

  useEffect(() => {
    loadVehicles();
  }, []);

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await api.createVehicle(normalizeVehiclePayload(form));
      setForm(initialForm);
      loadVehicles();
    } catch (err) {
      setError(err.message);
    }
  };

  const switchMode = async (vehicleId) => {
    setError("");
    try {
      await api.switchVehicle(vehicleId);
      loadVehicles();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section>
      <div className="section-header">
        <div>
          <p className="eyebrow">Back-office</p>
          <h1>Véhicules</h1>
        </div>
      </div>
      {error && <p className="alert error">{error}</p>}
      <div className="admin-layout">
        <form className="panel form-panel" onSubmit={onSubmit}>
          <h2>Ajouter un véhicule</h2>
          <label htmlFor="brand">Marque</label>
          <input id="brand" value={form.brand} onChange={(event) => setForm({ ...form, brand: event.target.value })} />
          <label htmlFor="model">Modèle</label>
          <input id="model" value={form.model} onChange={(event) => setForm({ ...form, model: event.target.value })} />
          <div className="form-row">
            <label>
              Année
              <input
                type="number"
                value={form.year}
                onChange={(event) => setForm({ ...form, year: event.target.value })}
              />
            </label>
            <label>
              Kilométrage
              <input
                type="number"
                value={form.mileage}
                onChange={(event) => setForm({ ...form, mileage: event.target.value })}
              />
            </label>
          </div>
          <div className="form-row">
            <label>
              Prix achat
              <input
                type="number"
                value={form.price}
                onChange={(event) => setForm({ ...form, price: event.target.value })}
              />
            </label>
            <label>
              Mensualité
              <input
                type="number"
                value={form.monthly_price}
                onChange={(event) => setForm({ ...form, monthly_price: event.target.value })}
              />
            </label>
          </div>
          <label htmlFor="energy">Énergie</label>
          <input id="energy" value={form.energy} onChange={(event) => setForm({ ...form, energy: event.target.value })} />
          <label htmlFor="mode">Mode</label>
          <select id="mode" value={form.mode} onChange={(event) => setForm({ ...form, mode: event.target.value })}>
            <option value="sale">Vente</option>
            <option value="rental">Location</option>
          </select>
          <button className="button" type="submit">
            Ajouter
          </button>
        </form>

        <div className="table-panel">
          <table>
            <thead>
              <tr>
                <th>Véhicule</th>
                <th>Mode</th>
                <th>Prix</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {vehicles.map((vehicle) => (
                <tr key={vehicle.id}>
                  <td>
                    {vehicle.brand} {vehicle.model}
                  </td>
                  <td>{vehicle.mode === "rental" ? "Location" : "Vente"}</td>
                  <td>{vehicle.mode === "rental" ? `${vehicle.monthly_price} €/mois` : `${vehicle.price} €`}</td>
                  <td>
                    <button className="button ghost" type="button" onClick={() => switchMode(vehicle.id)}>
                      Basculer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

