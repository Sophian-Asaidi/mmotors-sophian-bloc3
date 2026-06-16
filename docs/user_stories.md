# User stories

## Démarche de développement

- Comprendre le besoin métier et le rôle utilisateur.
- Écrire la user story au format "En tant que..., je veux..., afin de...".
- Définir les critères d'acceptation.
- Implémenter le backend si une donnée ou une règle métier est nécessaire.
- Implémenter l'écran ou le composant frontend.
- Ajouter ou adapter les tests.
- Vérifier manuellement le parcours.
- Passer la user story en statut `done`.

## User stories client

### US01 - Rechercher un véhicule

En tant que client, je veux consulter les véhicules disponibles afin d'identifier un modèle adapté à mon besoin.

Critères d'acceptation :

- la liste des véhicules est visible ;
- les informations principales sont affichées ;
- le bouton de dépôt de dossier est disponible.

Statut : done.

### US02 - Filtrer achat ou location

En tant que client, je veux filtrer les véhicules entre achat et location afin de voir uniquement les offres pertinentes.

Critères d'acceptation :

- le filtre achat affiche les véhicules en vente ;
- le filtre location affiche les véhicules en location ;
- le filtre est disponible depuis l'écran de recherche.

Statut : done.

### US03 - Créer un compte

En tant que client, je veux créer un compte afin de déposer et suivre mes dossiers.

Critères d'acceptation :

- l'email est unique ;
- le mot de passe est hashé ;
- l'utilisateur reçoit un JWT après inscription.

Statut : done.

### US04 - Déposer un dossier

En tant que client, je veux déposer un dossier d'achat ou de location avec documents afin que M-Motors puisse l'étudier.

Critères d'acceptation :

- le dossier est rattaché à un véhicule ;
- le type de dossier correspond au mode du véhicule ;
- les documents acceptés sont PDF, PNG, JPG ou JPEG ;
- le statut initial est `pending`.

Statut : done.

### US05 - Suivre un dossier

En tant que client, je veux suivre le statut de mes dossiers afin de savoir s'ils sont validés ou refusés.

Critères d'acceptation :

- seuls mes dossiers sont visibles ;
- le statut est affiché ;
- le commentaire admin est affiché s'il existe.

Statut : done.

## User stories admin

### US06 - Ajouter un véhicule

En tant qu'administrateur, je veux ajouter un véhicule à vendre ou à louer afin d'alimenter le catalogue.

Critères d'acceptation :

- seuls les admins peuvent créer un véhicule ;
- les champs sont validés ;
- le véhicule apparaît dans la recherche.

Statut : done.

### US07 - Basculer vente ou location

En tant qu'administrateur, je veux basculer un véhicule de vente vers location ou inversement afin d'adapter l'offre commerciale.

Critères d'acceptation :

- l'action est réservée aux admins ;
- le mode est mis à jour ;
- le véhicule remonte dans le bon filtre.

Statut : done.

### US08 - Consulter les dossiers

En tant qu'administrateur, je veux consulter tous les dossiers afin de traiter les demandes clients.

Critères d'acceptation :

- seuls les admins accèdent à la liste complète ;
- les informations client, véhicule et documents sont visibles.

Statut : done.

### US09 - Valider ou refuser un dossier

En tant qu'administrateur, je veux valider ou refuser un dossier afin d'informer le client de la décision.

Critères d'acceptation :

- le statut devient `approved` ou `rejected` ;
- un commentaire peut être ajouté ;
- le client voit le résultat dans son espace.

Statut : done.

