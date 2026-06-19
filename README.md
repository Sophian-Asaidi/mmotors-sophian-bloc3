# M-Motors - Location et achat de véhicules

## Contexte

M-Motors est une entreprise spécialisée dans la vente de véhicules d’occasion.

Le projet consiste à ajouter un service de location longue durée avec option d’achat, tout en conservant le fonctionnement existant de vente de véhicules.

L’application permet aux clients de rechercher un véhicule, de créer un compte, de déposer un dossier dématérialisé avec documents, puis de suivre l’avancement de ce dossier.

Le back-office permet aux administrateurs d’ajouter des véhicules, de gérer leur mode de disponibilité et de traiter les dossiers clients.

# M-Motors - Solution digitale achat et location

Le projet contient :

- un frontend React/Vite ;
- un backend FastAPI ;
- une base SQLite pour le local ;
- une configuration PostgreSQL possible via Docker Compose ;
- une supervision avec `/health`, `/metrics`, logs et alerte simulée.

## Comptes de test

| Rôle | Email | Mot de passe |
|---|---|---|
| Admin | admin.so@mmotors.fr | AdminSo2026! |
| Client | client.so@mmotors.fr | ClientSo2026! |

## Architecture générale

```text
Utilisateur
   |
   v
Frontend React / Vite
   |
   | appels HTTP avec JWT
   v
Backend FastAPI
   |
   |-- api/              routes REST
   |-- services/         logique métier
   |-- repositories/     accès aux données
   |-- schemas/          validation Pydantic
   |-- domain/           modèles SQLAlchemy
   |-- core/             configuration, sécurité, base
   |-- utils/            fonctions utilitaires
   |
   v
Base de données
   |-- SQLite en local
   |-- PostgreSQL prévu via Docker Compose

Supervision
   |-- GET /health
   |-- GET /metrics
   |-- POST /health/alert-test
   |-- logs backend
```

## Structure du projet

```text
mmotors_reference_complete/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── domain/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── main.py
│   │   └── seed.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
├── monitoring/
│   └── prometheus.yml
├── docker-compose.yml
├── render.yaml
├── vercel.json
└── README.md
```

## Fonctionnalités principales

Côté client :

- consulter le catalogue des véhicules ;
- filtrer les véhicules par achat ou location ;
- créer un compte ;
- se connecter ;
- déposer un dossier avec document ;
- suivre l'état de ses dossiers.

Côté administrateur :

- accéder au back-office ;
- ajouter un véhicule ;
- passer un véhicule en vente ou en location ;
- consulter les dossiers clients ;
- valider ou refuser un dossier.

## Sécurité

- authentification JWT ;
- mots de passe hachés avec Bcrypt ;
- rôles `user` et `admin` ;
- routes administrateur protégées ;
- validation des données avec Pydantic ;
- contrôle des fichiers uploadés ;
- configuration par variables d'environnement ;
- CORS paramétrable.

## Monitoring et alerting

- `GET /health` vérifie l'état de l'API et de la base ;
- `GET /metrics` expose des métriques simples ;
- `POST /health/alert-test` simule une alerte dans les logs ;
- les logs backend indiquent les requêtes, statuts et erreurs.

## Lancer le backend en local

```powershell
cd backend
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

URLs backend :

- API : http://127.0.0.1:8000
- Swagger : http://127.0.0.1:8000/docs
- Healthcheck : http://127.0.0.1:8000/health
- Metrics : http://127.0.0.1:8000/metrics

## Lancer le frontend en local

```powershell
cd frontend
npm config set registry https://registry.npmjs.org/
npm install
npm run dev
```

URL frontend : http://localhost:5173

## Tests backend

```powershell
cd backend
.\venv\Scripts\activate
pytest
pytest --cov=app
```

## Docker Compose optionnel

```powershell
docker compose up --build
```

Le fichier `docker-compose.yml` fournit une architecture possible avec frontend, backend, PostgreSQL, Prometheus et Grafana.
