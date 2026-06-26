import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { api } from './api.js';
import './styles.css';

function Badge({ value }) {
  const label = {
    pending: 'En attente',
    approved: 'Validé',
    rejected: 'Refusé',
    sale: 'Achat',
    rent: 'Location',
    admin: 'Admin',
    user: 'Client',
  }[value] || value;

  return <span className={`badge badge-${value}`}>{label}</span>;
}

function Layout({ user, page, setPage, logout, children }) {
  const nav = user?.role === 'admin'
    ? [
      ['admin', 'Administration'],
      ['monitoring', 'Supervision'],
    ]
    : user?.role === 'user'
      ? [
        ['catalog', 'Catalogue'],
        ['client', 'Espace client'],
      ]
      : [
        ['catalog', 'Catalogue'],
      ];

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span>M</span>
          <div>
            <b>M-Motors</b>
            <small>LLD & occasion</small>
          </div>
        </div>

        <nav>
          {nav.map(([id, label]) => (
            <button
              key={id}
              onClick={() => setPage(id)}
              className={page === id ? 'active' : ''}
            >
              {label}
            </button>
          ))}
        </nav>

        <div className="account">
          {user ? (
            <>
              <p>{user.email}</p>
              <Badge value={user.role} />
              <button className="ghost" onClick={logout}>Déconnexion</button>
            </>
          ) : (
            <button onClick={() => setPage('login')}>Connexion</button>
          )}
        </div>
      </aside>

      <main>{children}</main>
    </div>
  );
}

function LoginPage({ onAuth }) {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('client.so@mmotors.fr');
  const [password, setPassword] = useState('ClientSo2026!');
  const [error, setError] = useState('');

  async function submit(e) {
    e.preventDefault();
    setError('');

    try {
      const data = mode === 'login'
        ? await api.login(email, password)
        : await api.register(email, password);

      onAuth(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="panel narrow">
      <h1>{mode === 'login' ? 'Connexion' : 'Création de compte'}</h1>
      <p className="muted">Connecte-toi pour accéder aux fonctionnalités de l’application.</p>

      <form onSubmit={submit} className="form">
        <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
        <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Mot de passe" type="password" />
        {error && <p className="error">{error}</p>}
        <button>{mode === 'login' ? 'Se connecter' : 'Créer le compte'}</button>
      </form>

      <button className="link" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
        {mode === 'login' ? 'Créer un compte' : 'J’ai déjà un compte'}
      </button>
    </section>
  );
}

function VehicleCard({ vehicle, user, onApply }) {
  return (
    <article className="card vehicle">
      <div className="vehicle-head">
        <h3>{vehicle.brand} {vehicle.model}</h3>
        <Badge value={vehicle.mode} />
      </div>

      <p>{vehicle.year} · {vehicle.mileage.toLocaleString('fr-FR')} km · {vehicle.energy} · {vehicle.transmission}</p>

      <strong>
        {vehicle.mode === 'sale'
          ? `${vehicle.price?.toLocaleString('fr-FR')} €`
          : `${vehicle.monthly_price} €/mois`}
      </strong>

      {user?.role === 'user' && (
        <button onClick={() => onApply(vehicle)}>Déposer un dossier</button>
      )}

      {!user && <small>Connecte-toi pour déposer un dossier.</small>}
    </article>
  );
}

function CatalogPage({ user, token }) {
  const [mode, setMode] = useState('');
  const [vehicles, setVehicles] = useState([]);
  const [selected, setSelected] = useState(null);
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);
  const [notice, setNotice] = useState('');

  useEffect(() => {
    api.vehicles(mode).then(setVehicles).catch(err => setNotice(err.message));
  }, [mode]);

  async function submitApplication(e) {
    e.preventDefault();

    const form = new FormData();
    form.append('vehicle_id', selected.id);
    form.append('offer_type', selected.mode);
    form.append('message', message);

    if (file) form.append('documents', file);

    try {
      await api.submitApplication(token, form);
      setNotice('Dossier déposé avec succès.');
      setSelected(null);
      setMessage('');
      setFile(null);
    } catch (err) {
      setNotice(err.message);
    }
  }

  return (
    <section>
      <div className="hero">
        <h1>Catalogue M-Motors</h1>
        <p>Recherche un véhicule à acheter ou à louer en longue durée.</p>
      </div>

      <div className="filters">
        {[
          ['', 'Tous'],
          ['sale', 'Achat'],
          ['rent', 'Location'],
        ].map(([id, label]) => (
          <button key={id} className={mode === id ? 'active' : ''} onClick={() => setMode(id)}>
            {label}
          </button>
        ))}
      </div>

      {notice && <p className="notice">{notice}</p>}

      <div className="grid">
        {vehicles.map(v => (
          <VehicleCard key={v.id} vehicle={v} user={user} onApply={setSelected} />
        ))}
      </div>

      {selected && (
        <div className="modal">
          <form className="panel form" onSubmit={submitApplication}>
            <h2>Dossier pour {selected.brand} {selected.model}</h2>
            <textarea value={message} onChange={e => setMessage(e.target.value)} placeholder="Message complémentaire" />
            <input type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={e => setFile(e.target.files[0])} />
            <div className="row">
              <button>Envoyer</button>
              <button type="button" className="ghost" onClick={() => setSelected(null)}>Annuler</button>
            </div>
          </form>
        </div>
      )}
    </section>
  );
}

function ClientPage({ user, token, setPage }) {
  const [items, setItems] = useState([]);
  const [filesByApplication, setFilesByApplication] = useState({});
  const [noticeByApplication, setNoticeByApplication] = useState({});
  const [error, setError] = useState('');

  async function loadApplications() {
    try {
      const data = await api.myApplications(token);
      setItems(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function addDocument(applicationId) {
    const file = filesByApplication[applicationId];

    if (!file) {
      setNoticeByApplication({
        ...noticeByApplication,
        [applicationId]: 'Choisis un document avant d’envoyer.',
      });
      return;
    }

    const formData = new FormData();
    formData.append('documents', file);

    try {
      await api.addApplicationDocuments(token, applicationId, formData);

      setNoticeByApplication({
        ...noticeByApplication,
        [applicationId]: 'Document ajouté au dossier.',
      });

      setFilesByApplication({
        ...filesByApplication,
        [applicationId]: null,
      });

      await loadApplications();
    } catch (err) {
      setNoticeByApplication({
        ...noticeByApplication,
        [applicationId]: err.message,
      });
    }
  }

  useEffect(() => {
    if (token && user?.role === 'user') {
      loadApplications();
    }
  }, [token, user]);

  if (!user) {
    return (
      <section className="panel">
        <h1>Espace client</h1>
        <p>Connecte-toi pour accéder à tes dossiers.</p>
        <button onClick={() => setPage('login')}>Connexion</button>
      </section>
    );
  }

  if (user.role === 'admin') {
    return (
      <section className="panel">
        <h1>Espace client indisponible</h1>
        <p>Un administrateur doit utiliser uniquement le back-office.</p>
        <button onClick={() => setPage('admin')}>Aller à l’administration</button>
      </section>
    );
  }

  return (
    <section>
      <h1>Mes dossiers</h1>

      {error && <p className="error">{error}</p>}

      <div className="stack">
        {items.map(app => (
          <article className="card" key={app.id}>
            <div className="vehicle-head">
              <h3>{app.vehicle.brand} {app.vehicle.model}</h3>
              <Badge value={app.status} />
            </div>

            <p>{app.message || 'Aucun message'}</p>

            <small>{app.documents.length} document(s)</small>

            {app.admin_comment && (
              <p className="notice">Message : {app.admin_comment}</p>
            )}

            {app.status === 'pending' && (
              <div className="document-add">
                <input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  onChange={e => setFilesByApplication({
                    ...filesByApplication,
                    [app.id]: e.target.files[0],
                  })}
                />

                <button type="button" onClick={() => addDocument(app.id)}>
                  Ajouter un document
                </button>

                {noticeByApplication[app.id] && (
                  <p className="notice">{noticeByApplication[app.id]}</p>
                )}
              </div>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}

function AdminApplicationModal({ application, token, onClose, onDecision }) {
  const [adminComment, setAdminComment] = useState(application.admin_comment || '');
  const [clientNotice, setClientNotice] = useState('');
  const [internalComment, setInternalComment] = useState(application.internal_comment || '');
  const [internalNotice, setInternalNotice] = useState('');
  const [error, setError] = useState('');

  async function decide(status) {
    setError('');

    try {
      await onDecision(
        application.id,
        status,
        adminComment || (status === 'approved' ? 'Dossier validé' : 'Dossier refusé')
      );
      onClose();
    } catch (err) {
      setError(err.message);
    }
  }

  async function download(document) {
    setError('');

    try {
      await api.downloadAdminDocument(token, document);
    } catch (err) {
      setError(err.message);
    }
  }

  async function saveInternalComment() {
    setError('');
    setInternalNotice('');

    try {
      await api.updateInternalComment(token, application.id, internalComment);
      setInternalNotice('Commentaire interne enregistré.');
    } catch (err) {
      setError(err.message);
    }
  }

  async function saveClientComment() {
    setError('');
    setClientNotice('');

    try {
      await api.updateClientComment(token, application.id, adminComment);
      setClientNotice('Message client enregistré.');
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="modal">
      <div className="panel modal-large">
        <div className="vehicle-head">
          <h2>Détail du dossier #{application.id}</h2>
          <Badge value={application.status} />
        </div>

        {error && <p className="error">{error}</p>}

        <div className="detail-grid">
          <div>
            <h3>Client</h3>
            <p>{application.user.email}</p>
          </div>

          <div>
            <h3>Véhicule</h3>
            <p>{application.vehicle.brand} {application.vehicle.model}</p>
            <small>
              {application.vehicle.year} · {application.vehicle.mileage.toLocaleString('fr-FR')} km
            </small>
          </div>

          <div>
            <h3>Type de demande</h3>
            <Badge value={application.offer_type} />
          </div>

          <div>
            <h3>Statut</h3>
            <Badge value={application.status} />
          </div>
        </div>

        <h3>Message du client</h3>
        <div className="message-box">
          {application.message || 'Aucun message client.'}
        </div>

        <h3>Documents joints</h3>
        {application.documents.length === 0 ? (
          <p className="muted">Aucun document joint au dossier.</p>
        ) : (
          <div className="stack">
            {application.documents.map(document => (
              <div className="line" key={document.id}>
                <span>{document.filename}</span>
                <button type="button" onClick={() => download(document)}>
                  Télécharger
                </button>
              </div>
            ))}
          </div>
        )}

        <h3>Commentaire interne</h3>

        <textarea
          value={internalComment}
          onChange={e => setInternalComment(e.target.value)}
          placeholder="Note interne pour le service commercial"
        />

        <div className="row">
          <button type="button" onClick={saveInternalComment}>
            Enregistrer le commentaire interne
          </button>
        </div>

        {internalNotice && <p className="notice">{internalNotice}</p>}

        <h3>Message pour le client</h3>

        <textarea
          value={adminComment}
          onChange={e => setAdminComment(e.target.value)}
          placeholder=""
        />

        <div className="row">
          <button type="button" onClick={saveClientComment}>
            Enregistrer le message client
          </button>
        </div>

        {clientNotice && <p className="notice">{clientNotice}</p>}

        <div className="row modal-actions">
          <button type="button" onClick={() => decide('approved')}>
            Valider le dossier
          </button>

          <button type="button" className="danger" onClick={() => decide('rejected')}>
            Refuser le dossier
          </button>

          <button type="button" className="ghost" onClick={onClose}>
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
}

function AdminPage({ user, token }) {
  const [apps, setApps] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [notice, setNotice] = useState('');
  const [selectedApplication, setSelectedApplication] = useState(null);
  const [form, setForm] = useState({
    brand: '',
    model: '',
    year: 2023,
    mileage: 0,
    energy: 'Essence',
    transmission: 'Manuelle',
    mode: 'sale',
    price: 15000,
    monthly_price: 250,
  });

  const load = () => {
    api.adminApplications(token).then(setApps);
    api.vehicles().then(setVehicles);
  };

  useEffect(() => {
    if (user?.role === 'admin') load();
  }, [user]);

  if (user?.role !== 'admin') {
    return (
      <section className="panel">
        <h1>Administration</h1>
        <p>Accès réservé aux administrateurs.</p>
      </section>
    );
  }

  async function openApplication(app) {
    const detail = await api.adminApplicationDetail(token, app.id);
    setSelectedApplication(detail);
  }

  async function decide(id, status, adminComment) {
    await api.decideApplication(token, id, status, adminComment);
    load();
  }

  async function createVehicle(e) {
    e.preventDefault();

    await api.createVehicle(token, {
      ...form,
      year: Number(form.year),
      mileage: Number(form.mileage),
      price: form.mode === 'sale' ? Number(form.price) : null,
      monthly_price: form.mode === 'rent' ? Number(form.monthly_price) : null,
    });

    setNotice('Véhicule ajouté');
    load();
  }

  async function switchMode(v) {
    await api.changeVehicleMode(
      token,
      v.id,
      v.mode === 'sale'
        ? { mode: 'rent', monthly_price: v.monthly_price || 299 }
        : { mode: 'sale', price: v.price || 15000 },
    );

    load();
  }

  return (
    <section>
      <h1>Back-office</h1>
      {notice && <p className="notice">{notice}</p>}

      <div className="admin-grid">
        <form className="panel form" onSubmit={createVehicle}>
          <h2>Ajouter un véhicule</h2>

          {['brand', 'model', 'year', 'mileage', 'energy', 'transmission'].map(k => (
            <input
              key={k}
              value={form[k]}
              onChange={e => setForm({ ...form, [k]: e.target.value })}
              placeholder={k}
            />
          ))}

          <select value={form.mode} onChange={e => setForm({ ...form, mode: e.target.value })}>
            <option value="sale">Vente</option>
            <option value="rent">Location</option>
          </select>

          <button>Ajouter</button>
        </form>

        <div className="panel">
          <h2>Véhicules</h2>

          {vehicles.map(v => (
            <div className="line" key={v.id}>
              <span>{v.brand} {v.model} <Badge value={v.mode} /></span>
              <button onClick={() => switchMode(v)}>Basculer</button>
            </div>
          ))}
        </div>
      </div>

      <h2>Dossiers clients</h2>

      <div className="stack">
        {apps.map(app => (
          <article className="card" key={app.id}>
            <div className="vehicle-head">
              <h3>{app.user.email}</h3>
              <Badge value={app.status} />
            </div>

            <p>{app.vehicle.brand} {app.vehicle.model} · {app.offer_type}</p>
            <p className="muted">{app.documents.length} document(s) joint(s)</p>

            <div className="row">
              <button onClick={() => openApplication(app)}>Voir le dossier</button>
              <button onClick={() => decide(app.id, 'approved', 'Dossier validé')}>Valider</button>
              <button className="danger" onClick={() => decide(app.id, 'rejected', 'Dossier refusé')}>Refuser</button>
            </div>
          </article>
        ))}
      </div>

      {selectedApplication && (
        <AdminApplicationModal
          application={selectedApplication}
          token={token}
          onClose={() => setSelectedApplication(null)}
          onDecision={decide}
        />
      )}
    </section>
  );
}

function MonitoringPage() {
  const [health, setHealth] = useState(null);
  const [metrics, setMetrics] = useState('');
  const [alert, setAlert] = useState(null);

  async function refresh() {
    setHealth(await api.health());
    setMetrics(await api.metrics());
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <section>
      <h1>Supervision</h1>

      <div className="admin-grid">
        <div className="panel">
          <h2>Healthcheck</h2>
          <pre>{JSON.stringify(health, null, 2)}</pre>
          <button onClick={refresh}>Rafraîchir</button>
        </div>

        <div className="panel">
          <h2>Alerting simulé</h2>
          <p>Déclenche une alerte de test dans les logs backend.</p>
          <button onClick={async () => setAlert(await api.alertTest())}>Tester l’alerte</button>
          {alert && <pre>{JSON.stringify(alert, null, 2)}</pre>}
        </div>
      </div>

      <div className="panel">
        <h2>Metrics</h2>
        <pre>{metrics}</pre>
      </div>
    </section>
  );
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [page, setPage] = useState('catalog');

  useEffect(() => {
    if (token) {
      api.me(token)
        .then(currentUser => {
          setUser(currentUser);

          if (currentUser.role === 'admin' && (page === 'catalog' || page === 'client' || page === 'login')) {
            setPage('admin');
          }

          if (currentUser.role !== 'admin' && page === 'monitoring') {
            setPage('catalog');
          }
        })
        .catch(() => {
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
        });
    }
  }, [token, page]);

  const content = useMemo(() => {
    if (page === 'login') {
      return (
        <LoginPage
          onAuth={(data) => {
            localStorage.setItem('token', data.access_token);
            setToken(data.access_token);
            setUser(data.user);
            setPage(data.user.role === 'admin' ? 'admin' : 'catalog');
          }}
        />
      );
    }

    if (page === 'client') {
      return <ClientPage user={user} token={token} setPage={setPage} />;
    }

    if (page === 'admin') {
      return <AdminPage user={user} token={token} />;
    }

    if (page === 'monitoring') {
      if (user?.role !== 'admin') {
        return (
          <section className="panel">
            <h1>Accès refusé</h1>
            <p>La supervision est réservée aux administrateurs.</p>
            <button onClick={() => setPage('catalog')}>Retour au catalogue</button>
          </section>
        );
      }

      return <MonitoringPage />;
    }

    return <CatalogPage user={user} token={token} />;
  }, [page, user, token]);

  return (
    <Layout
      user={user}
      page={page}
      setPage={setPage}
      logout={() => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setPage('catalog');
      }}
    >
      {content}
    </Layout>
  );
}

createRoot(document.getElementById('root')).render(<App />);