import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { api } from "../services/api.js";

export default function Register() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const data = await api.register(form);
      login(data);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section className="auth-page">
      <form className="panel form-panel" onSubmit={onSubmit}>
        <p className="eyebrow">Nouveau client</p>
        <h1>Création de compte</h1>
        {error && <p className="alert error">{error}</p>}
        <label htmlFor="register-email">Email</label>
        <input
          id="register-email"
          value={form.email}
          onChange={(event) => setForm({ ...form, email: event.target.value })}
          placeholder="prenom.nom@exemple.fr"
        />
        <label htmlFor="register-password">Mot de passe</label>
        <input
          id="register-password"
          type="password"
          value={form.password}
          onChange={(event) => setForm({ ...form, password: event.target.value })}
        />
        <button className="button" type="submit">
          Créer le compte
        </button>
      </form>
    </section>
  );
}

