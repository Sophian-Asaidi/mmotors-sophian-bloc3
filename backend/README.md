# Backend M-Motors

Backend FastAPI de l'application M-Motors.

Il gère :

- l'authentification ;
- les rôles client et administrateur ;
- les véhicules ;
- les dossiers clients ;
- l'upload de documents ;
- la supervision avec `/health`, `/metrics` et `/health/alert-test`.

## Architecture backend

```text
backend/
├── app/
│   ├── api/              routes FastAPI
│   │   ├── auth.py
│   │   ├── vehicles.py
│   │   ├── applications.py
│   │   ├── admin.py
│   │   └── monitoring.py
│   ├── core/             configuration, base, sécurité
│   │   ├── settings.py
│   │   ├── database.py
│   │   └── security.py
│   ├── domain/           modèles SQLAlchemy
│   │   └── models.py
│   ├── repositories/     accès à la base de données
│   │   ├── users.py
│   │   ├── vehicles.py
│   │   └── applications.py
│   ├── schemas/          schémas Pydantic
│   │   ├── auth.py
│   │   ├── vehicle.py
│   │   └── application.py
│   ├── services/         logique métier
│   │   ├── auth_service.py
│   │   ├── vehicle_service.py
│   │   ├── application_service.py
│   │   └── monitoring.py
│   ├── utils/            validation et outils
│   │   └── files.py
│   ├── main.py           point d'entrée FastAPI
│   └── seed.py           données de départ
├── tests/
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Choix techniques

- FastAPI pour créer l'API REST ;
- SQLAlchemy pour communiquer avec la base ;
- Pydantic pour valider les données ;
- JWT pour sécuriser les accès ;
- Bcrypt pour hacher les mots de passe ;
- Pytest pour les tests unitaires ;
- SQLite en local ;
- PostgreSQL possible avec Docker Compose ou une variable `DATABASE_URL`.

## Variables d'environnement

Créer un fichier `.env` ou utiliser les variables de la plateforme de déploiement.

Exemple :

```env
DATABASE_URL=sqlite:///./mmotors.db
JWT_SECRET_KEY=change-moi-avec-une-cle-longue
CORS_ORIGINS=http://localhost:5173
```

## Installation locale

```powershell
cd backend
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```powershell
python -m uvicorn app.main:app --reload
```

URLs utiles :

- Swagger : http://127.0.0.1:8000/docs
- Healthcheck : http://127.0.0.1:8000/health
- Metrics : http://127.0.0.1:8000/metrics

## Routes principales

Authentification :

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

Véhicules :

- `GET /vehicles`
- `GET /vehicles/{vehicle_id}`

Dossiers :

- `POST /applications`
- `GET /applications/me`

Administration :

- gestion des véhicules ;
- consultation des dossiers ;
- validation des dossiers ;
- refus des dossiers.

Monitoring :

- `GET /health`
- `GET /metrics`
- `POST /health/alert-test`

## Sécurité

- les mots de passe sont hachés ;
- les routes privées nécessitent un JWT ;
- les routes admin nécessitent le rôle `admin` ;
- les fichiers uploadés sont contrôlés ;
- les données entrantes sont validées par Pydantic ;
- les erreurs HTTP sont explicites.

## Tests

```powershell
pytest
pytest --cov=app
```

Les tests vérifient notamment :

- inscription et connexion ;
- erreurs d'authentification ;
- accès aux véhicules ;
- dépôt et suivi de dossier ;
- droits administrateur ;
- monitoring et alerting.
