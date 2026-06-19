# M-Motors - Location et achat de véhicules

## Contexte

M-Motors est une entreprise spécialisée dans la vente de véhicules d’occasion.

Le projet consiste à ajouter un service de location longue durée avec option d’achat, tout en conservant le fonctionnement existant de vente de véhicules.

L’application permet aux clients de rechercher un véhicule, de créer un compte, de déposer un dossier dématérialisé avec documents, puis de suivre l’avancement de ce dossier.

Le back-office permet aux administrateurs d’ajouter des véhicules, de gérer leur mode de disponibilité et de traiter les dossiers clients.

## Architecture

- Frontend : React + Vite
- Backend : FastAPI + SQLAlchemy
- Base locale : SQLite
- Base production prévue : PostgreSQL via `DATABASE_URL`
- Supervision : `/health`, `/metrics`, logs backend et alerte simulée
- Conteneurisation : Docker Compose fourni en option

## Comptes de test

| Rôle | Email | Mot de passe |
|---|---|---|
| Admin | admin.so@mmotors.fr | AdminSo2026! |
| Client | client.so@mmotors.fr | ClientSo2026! |

## Lancer le backend en local

```powershell
cd backend
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

URLs utiles :

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

URL : http://localhost:5173

## Tests backend

```powershell
cd backend
.\venv\Scripts\activate
pytest
pytest --cov=app
```

## User stories couvertes

Client :

- consulter les véhicules ;
- filtrer achat / location ;
- créer un compte ;
- se connecter ;
- déposer un dossier avec documents ;
- suivre l'état de ses dossiers.

Administrateur :

- accéder au back-office ;
- ajouter un véhicule ;
- basculer un véhicule en vente ou location ;
- consulter les dossiers ;
- valider ou refuser un dossier.

## Sécurité

- JWT pour l'authentification ;
- mots de passe hachés avec Bcrypt ;
- séparation des rôles `user` et `admin` ;
- routes admin protégées ;
- validation des données avec Pydantic ;
- contrôle des fichiers uploadés ;
- configuration par variables d'environnement ;
- CORS paramétrable.

## Monitoring et alerting

- `GET /health` vérifie l'état API + base de données ;
- `GET /metrics` expose des métriques simples au format Prometheus ;
- `POST /health/alert-test` déclenche une alerte simulée dans les logs ;
- logs middleware sur chaque requête : méthode, chemin, statut, durée.

## Docker Compose optionnel

```powershell
docker compose up --build
```

Le fichier `docker-compose.yml` inclut une architecture possible avec API, PostgreSQL, frontend, Prometheus et Grafana.
