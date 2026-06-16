# Sécurité

## Authentification

L'API utilise un JWT Bearer. Après connexion ou inscription, le backend renvoie un token signé. Les routes protégées lisent ce token dans l'en-tête `Authorization`.

## Mots de passe

Les mots de passe ne sont jamais stockés en clair. Ils sont hashés avec bcrypt via `passlib`.

## Rôles

Deux rôles sont utilisés :

- `user` : recherche, dépôt et suivi de ses dossiers ;
- `admin` : gestion des véhicules et de tous les dossiers.

Les routes `/admin/*` vérifient explicitement le rôle admin.

## Validation des entrées

Pydantic valide les champs reçus par l'API :

- longueur email et mot de passe ;
- année, kilométrage et prix ;
- type de véhicule `sale` ou `rental` ;
- statut de dossier `approved` ou `rejected`.

## Documents

Les fichiers acceptés sont limités à :

- PDF ;
- PNG ;
- JPG ;
- JPEG.

Les noms de fichiers sont nettoyés et le fichier stocké reçoit un nom technique unique.

## Secrets

Le secret JWT doit être fourni par variable d'environnement en production :

```bash
JWT_SECRET_KEY=valeur-longue-et-aleatoire
```

Le fichier `.env` n'est pas versionné.

## Risques restants

Pour un passage en production réelle, il faudrait ajouter :

- antivirus ou scan des documents ;
- stockage objet type S3 ;
- limitation de taille des fichiers ;
- rotation des secrets ;
- politique de sauvegarde vérifiée automatiquement.

