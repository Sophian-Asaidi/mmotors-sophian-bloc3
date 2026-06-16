# Migration SQLite vers PostgreSQL

## Situation actuelle

SQLite est utilisé pour simplifier le développement local, les tests et la correction.

## Cible recommandée

PostgreSQL managé sur Render, Railway, Heroku ou équivalent.

## Étapes de migration

Créer une base PostgreSQL dans le cloud.
Récupérer l'URL de connexion.
Définir la variable d'environnement :

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
```

Installer le driver PostgreSQL si nécessaire :

```bash
pip install psycopg2-binary
```

Ajouter `psycopg2-binary` dans `backend/requirements.txt`.
Démarrer l'API : les tables sont créées automatiquement au démarrage.
Exécuter le seed pour créer les comptes de démonstration.
Importer les données existantes si nécessaire.

## Migration des données

Pour un petit volume, exporter SQLite en CSV puis importer dans PostgreSQL est suffisant. Pour un projet plus avancé, Alembic serait ajouté pour versionner les migrations.

## Sauvegardes

Le choix PostgreSQL cloud facilite :

- les sauvegardes automatiques ;
- la restauration à un instant donné ;
- le respect du RPO de 15 minutes ;
- le respect du RTO de 1 heure.

