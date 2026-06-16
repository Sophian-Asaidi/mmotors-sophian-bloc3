import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { api } from "../services/api.js";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "userLocal@Motors", password: "UserMot1!" });
  const [error, setError] = useState("");

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const data = await api.login(form);
      login(data);
      navigate(data.user.role === "admin" ? "/admin" : "/dashboard");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section className="auth-page">
      <form className="panel form-panel" onSubmit={onSubmit}>
        <p className="eyebrow">Accès sécurisé</p>
        <h1>Connexion</h1>
        {error && <p className="alert error">{error}</p>}
        <label htmlFor="email">Email</label>
        <input
          id="email"
          value={form.email}
          onChange={(event) => setForm({ ...form, email: event.target.value })}
        />
        <label htmlFor="password">Mot de passe</label>
        <input
          id="password"
          type="password"
          value={form.password}
          onChange={(event) => setForm({ ...form, password: event.target.value })}
        />
        <button className="button" type="submit">
          Se connecter
        </button>
        <p>
          Pas encore de compte ? <Link to="/register">Créer un compte</Link>
        </p>
      </form>
    </section>
  );
}

