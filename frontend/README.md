# Frontend M-Motors

Frontend React/Vite de l'application M-Motors.

Il permet aux clients de consulter les véhicules, déposer un dossier et suivre son avancement. Il permet aussi aux administrateurs de gérer les véhicules et les dossiers.

## Architecture frontend

```text
frontend/
├── src/
│   ├── api.js        appels HTTP vers le backend
│   ├── main.jsx      application React, routes et écrans
│   └── styles.css    styles de l'interface
├── index.html
├── package.json
├── Dockerfile
├── .env.example
└── README.md
```

## Choix techniques

- React pour l'interface ;
- Vite pour le serveur de développement et le build ;
- JavaScript ;
- React Router pour la navigation ;
- CSS pour le style ;
- appels API vers FastAPI.

## Variables d'environnement

Créer un fichier `.env` dans le dossier `frontend`.

Pour un lancement local :

```env
VITE_API_URL=http://127.0.0.1:8000
```

Pour un déploiement Vercel :

```env
VITE_API_URL=https://votre-api-render.onrender.com
```

## Installation locale

```powershell
cd frontend
npm config set registry https://registry.npmjs.org/
npm install
```

## Lancement

```powershell
npm run dev
```

URL locale :

```text
http://localhost:5173
```

## Build

```powershell
npm run build
```

Le dossier généré est :

```text
dist/
```

## Écrans principaux

- Accueil ;
- Catalogue des véhicules ;
- filtre achat / location ;
- connexion ;
- inscription ;
- espace client ;
- dépôt de dossier ;
- suivi des dossiers ;
- back-office administrateur ;
- supervision.

## Connexion au backend

Tous les appels vers l'API passent par `src/api.js`.

Le frontend utilise la variable :

```text
VITE_API_URL
```

Cela permet de changer facilement l'adresse de l'API entre le local et le déploiement.

## Sécurité côté frontend

- stockage du token JWT côté client ;
- ajout du token dans les appels aux routes protégées ;
- séparation des parcours client et administrateur ;
- affichage conditionnel selon le rôle connecté ;
- gestion des erreurs retournées par l'API.

## Déploiement Vercel

Paramètres conseillés :

```text
Root Directory: frontend
Framework Preset: Vite
Install Command: npm install
Build Command: npm run build
Output Directory: dist
```
