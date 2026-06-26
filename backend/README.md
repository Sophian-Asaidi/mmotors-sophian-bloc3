# Backend M-Motors

Backend FastAPI de l'application M-Motors.

Il gère :

* l'authentification ;
* les rôles client et administrateur ;
* les véhicules ;
* les dossiers clients ;
* l'upload de documents ;
* les commentaires administrateur ;
* la supervision avec `/health`, `/metrics` et `/health/alert-test`.

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

* FastAPI pour créer l'API REST ;
* SQLAlchemy pour communiquer avec la base de données ;
* Pydantic pour valider les données ;
* JWT pour sécuriser les accès ;
* Bcrypt pour hacher les mots de passe ;
* Pytest pour les tests unitaires ;
* SQLite en local pour le développement ;
* PostgreSQL en production via la variable d'environnement `DATABASE_URL`.

## Base de données

Le backend utilise SQLAlchemy.

En local, si aucune variable `DATABASE_URL` n'est définie, l'application utilise SQLite :

```env
DATABASE_URL=sqlite:///./mmotors.db
```

En production, le service backend déployé sur Render utilise PostgreSQL avec la variable d'environnement `DATABASE_URL` :

```env
DATABASE_URL=postgresql://...
```

L'URL réelle de la base PostgreSQL n'est pas stockée dans le code source. Elle est configurée directement dans les variables d'environnement Render.

Cette organisation permet d'utiliser une base simple en local, tout en conservant les données en production après un redéploiement du backend.

## Variables d'environnement

Créer un fichier `.env` ou utiliser les variables de la plateforme de déploiement.

Exemple local :

```env
DATABASE_URL=sqlite:///./mmotors.db
JWT_SECRET_KEY=change-moi-avec-une-cle-longue
CORS_ORIGINS=http://localhost:5173
```

Exemple production Render :

```env
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=cle-secrete-configuree-sur-render
CORS_ORIGINS=https://mmotors-sophian-bloc3.vercel.app,http://localhost:5173
PYTHON_VERSION=3.12.10
```

## Fonctionnalités backend

### Authentification

* création de compte client ;
* connexion ;
* génération d'un token JWT ;
* récupération de l'utilisateur connecté.

### Véhicules

* consultation des véhicules ;
* filtre achat / location ;
* ajout de véhicule par un administrateur ;
* modification du mode vente / location par un administrateur.

### Dossiers clients

* dépôt d'un dossier par un client connecté ;
* ajout de documents lors du dépôt ;
* suivi des dossiers côté client ;
* ajout de documents complémentaires sur un dossier encore en attente.

### Administration

* consultation de tous les dossiers clients ;
* consultation détaillée d'un dossier ;
* consultation du message client ;
* consultation et téléchargement des documents joints ;
* ajout d'un commentaire interne visible uniquement dans le back-office ;
* ajout d'un message visible par le client sans changer le statut du dossier ;
* validation d'un dossier ;
* refus d'un dossier.

### Supervision

* vérification de l'état de l'API avec `/health` ;
* exposition de métriques simples avec `/metrics` ;
* simulation d'alerte avec `/health/alert-test`.

## Installation locale

```powershell
cd backend
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement local

```powershell
$env:PYTHONPATH=(Get-Location).Path
python -m uvicorn app.main:app --reload
```

URLs utiles :

* Swagger : http://127.0.0.1:8000/docs
* Healthcheck : http://127.0.0.1:8000/health
* Metrics : http://127.0.0.1:8000/metrics

## Routes principales

Authentification :

* `POST /auth/register`
* `POST /auth/login`
* `GET /auth/me`

Véhicules :

* `GET /vehicles`
* `GET /vehicles/{vehicle_id}`

Dossiers :

* `POST /applications`
* `GET /applications/me`
* `POST /applications/{application_id}/documents`

Administration :

* `GET /admin/applications`
* `GET /admin/applications/{application_id}`
* `PATCH /admin/applications/{application_id}/status`
* `PATCH /admin/applications/{application_id}/internal-comment`
* `PATCH /admin/applications/{application_id}/client-comment`
* `GET /admin/documents/{document_id}/download`
* `POST /admin/vehicles`
* `PATCH /admin/vehicles/{vehicle_id}/mode`

Monitoring :

* `GET /health`
* `GET /metrics`
* `POST /health/alert-test`

## Sécurité

* les mots de passe sont hachés avec Bcrypt ;
* les routes privées nécessitent un JWT ;
* les routes administrateur nécessitent le rôle `admin` ;
* un client ne peut consulter que ses propres dossiers ;
* un client ne peut ajouter des documents que sur ses propres dossiers encore en attente ;
* le commentaire interne n'est renvoyé que dans les réponses administrateur ;
* les fichiers uploadés sont contrôlés ;
* les données entrantes sont validées avec Pydantic ;
* les erreurs HTTP sont explicites.

## Tests

```powershell
cd backend
.\venv\Scripts\activate
$env:PYTHONPATH=(Get-Location).Path
python -m pytest
python -m pytest --cov=app
```

Les tests vérifient notamment :

* inscription et connexion ;
* erreurs d'authentification ;
* accès aux véhicules ;
* dépôt et suivi de dossier ;
* droits administrateur ;
* monitoring et alerting.
