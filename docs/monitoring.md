# Monitoring et alerting

## Logs

Un middleware journalise chaque requête :

- méthode HTTP ;
- chemin ;
- code de statut ;
- durée d'exécution.

Les erreurs non prévues sont journalisées avec une trace pour faciliter le diagnostic.

## Healthcheck

Endpoint :

```http
GET /health
```

Réponse attendue :

```json
{
  "status": "ok",
  "database": "ok",
  "alerting": "simulated",
  "rpo": "15 min",
  "rto": "1 heure"
}
```

## Alerting simulé

Endpoint :

```http
POST /health/alert-test
```

Ce point d'entrée écrit une alerte simulée dans les logs. Dans un cloud réel, cette alerte pourrait être reliée à :

- Render/Railway logs ;
- Sentry ;
- Slack ;
- email ;
- webhook d'astreinte.

## Gestion d'erreur

Les erreurs fonctionnelles utilisent des codes HTTP explicites :

- `401` pour l'absence ou l'invalidité du JWT ;
- `403` pour un rôle insuffisant ;
- `404` pour une ressource introuvable ;
- `409` pour un email déjà utilisé ;
- `422` pour une entrée invalide.

## RPO et RTO

- RPO : 15 min, avec sauvegarde base au minimum toutes les 15 minutes.
- RTO : 1 heure, avec procédure de restauration documentée et variables d'environnement sauvegardées.

