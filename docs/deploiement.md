# Déploiement cloud

Déploiement via Render et Vercel.

## Option recommandée : Render

### Backend

Créer un service web Render :

- Root directory : `backend`
- Build command : `pip install -r requirements.txt`
- Start command : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Variables :

```bash
APP_ENV=production
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=valeur-longue-et-aleatoire
CORS_ORIGINS=https://url-du-frontend.onrender.com
UPLOAD_DIR=./uploads
LOG_LEVEL=INFO
```

### Frontend

Créer un service static site Render :

- Root directory : `frontend`
- Build command : `npm install && npm run build`
- Publish directory : `dist`

Variable :

```bash
VITE_API_URL=https://url-du-backend.onrender.com
```

## Option Railway

Railway peut héberger le backend et fournir une base PostgreSQL. Le frontend peut être déployé sur Railway, Render static site ou Netlify.

## Vérifications avant dépôt final

- Le frontend public charge correctement.
- Le backend `/health` retourne `200`.
- La connexion admin fonctionne.
- La connexion user fonctionne.
- Un dossier peut être déposé.
- Un dossier peut être validé depuis l'admin.
- Les liens Git sont publics.
- Les identifiants sont visibles dans le rapport PDF.

