# M-Motors - Solution digitale achat et location

## Contexte

M-Motors est une entreprise spécialisée dans la vente de véhicules d’occasion.

Le projet consiste à ajouter un service de location longue durée avec option d’achat, tout en conservant le fonctionnement existant de vente de véhicules.

L’application permet aux clients de rechercher un véhicule, de créer un compte, de déposer un dossier dématérialisé avec documents, puis de suivre l’avancement de ce dossier.

Le back-office permet aux administrateurs d’ajouter des véhicules, de gérer leur mode de disponibilité, de consulter les dossiers clients et de traiter les demandes.

## Technologies utilisées

Le projet contient :

* un frontend React / Vite ;
* un backend FastAPI ;
* une base SQLite utilisée uniquement en local ;
* une base PostgreSQL utilisée en production sur Render via la variable d’environnement `DATABASE_URL` ;
* une supervision avec `/health`, `/metrics`, logs backend et alerte simulée ;
* une gestion des rôles `user` et `admin`.

## Comptes de test

| Rôle   | Email                                               | Mot de passe  |
| ------ | --------------------------------------------------- | ------------- |
| Admin  | [admin.so@mmotors.fr](mailto:admin.so@mmotors.fr)   | AdminSo2026!  |
| Client | [client.so@mmotors.fr](mailto:client.so@mmotors.fr) | ClientSo2026! |

## Architecture

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
   |-- PostgreSQL en production via Render

Supervision
   |-- GET /health
   |-- GET /metrics
   |-- POST /health/alert-test
   |-- logs backend
```

## Structure du projet

```text
mmotors-sophian-bloc3/
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

### Côté client

* consulter le catalogue des véhicules ;
* filtrer les véhicules par achat ou location ;
* créer un compte ;
* se connecter ;
* déposer un dossier avec document ;
* suivre l’état de ses dossiers ;
* consulter le message envoyé par l’administrateur ;
* ajouter un document complémentaire à un dossier encore en attente.

### Côté administrateur

* accéder au back-office ;
* ajouter un véhicule ;
* passer un véhicule en vente ou en location ;
* consulter les dossiers clients ;
* voir le détail complet d’un dossier ;
* consulter le message du client ;
* consulter et télécharger les documents joints ;
* ajouter un commentaire interne visible uniquement dans le back-office ;
* envoyer un message visible par le client sans valider ni refuser le dossier ;
* valider ou refuser un dossier.

## Corrections ajoutées

À la suite du retour correcteur, plusieurs corrections ont été ajoutées :

* l’administrateur ne voit plus les écrans réservés au client ;
* les visiteurs et clients ne voient plus la page de supervision ;
* l’administrateur peut consulter le détail complet d’un dossier avant de le valider ou de le refuser ;
* l’administrateur peut voir le message du client et les documents joints ;
* l’administrateur peut ajouter un commentaire interne sur chaque dossier ;
* le commentaire interne est visible uniquement dans le back-office ;
* l’administrateur peut envoyer un message au client sans changer le statut du dossier ;
* le client peut ajouter des documents complémentaires sur un dossier encore en attente ;
* la production utilise PostgreSQL via la variable d’environnement `DATABASE_URL`.

## Base de données

L’application utilise deux configurations selon l’environnement.

En local, SQLite est utilisé pour faciliter le développement et les tests :

```env
DATABASE_URL=sqlite:///./mmotors.db
```

En production, le backend déployé sur Render utilise PostgreSQL grâce à la variable d’environnement `DATABASE_URL` :

```env
DATABASE_URL=postgresql://...
```

L’URL réelle de la base PostgreSQL n’est pas stockée dans le code source. Elle est configurée directement dans les variables d’environnement Render.

Cette configuration permet de séparer le code applicatif de la base de données de production. Les données ne dépendent donc plus d’un fichier SQLite local et restent conservées après un redéploiement du backend.

## Sécurité

* authentification JWT ;
* mots de passe hachés avec Bcrypt ;
* rôles `user` et `admin` ;
* routes administrateur protégées ;
* routes client protégées par authentification ;
* validation des données avec Pydantic ;
* contrôle des fichiers uploadés ;
* configuration par variables d’environnement ;
* CORS paramétrable.

## Monitoring et alerting

* `GET /health` vérifie l’état de l’API ;
* `GET /metrics` expose des métriques simples ;
* `POST /health/alert-test` simule une alerte dans les logs ;
* les logs backend indiquent les requêtes, statuts et erreurs.

## Lancer le backend en local

```powershell
cd backend
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH=(Get-Location).Path
python -m uvicorn app.main:app --reload
```

URLs backend :

* API : http://127.0.0.1:8000
* Swagger : http://127.0.0.1:8000/docs
* Healthcheck : http://127.0.0.1:8000/health
* Metrics : http://127.0.0.1:8000/metrics

## Lancer le frontend en local

```powershell
cd frontend
npm config set registry https://registry.npmjs.org/
npm install
npm run dev
```

URL frontend :

```text
http://localhost:5173
```

## Tests backend

```powershell
cd backend
.\venv\Scripts\activate
$env:PYTHONPATH=(Get-Location).Path
python -m pytest
python -m pytest --cov=app
```

## Déploiement

Le frontend est déployé sur Vercel.

Le backend est déployé sur Render.

En production, le backend utilise PostgreSQL via la variable d’environnement `DATABASE_URL`.

## Docker Compose optionnel

```powershell
docker compose up --build
```

Le fichier `docker-compose.yml` fournit une architecture possible avec frontend, backend, PostgreSQL, Prometheus et Grafana.
