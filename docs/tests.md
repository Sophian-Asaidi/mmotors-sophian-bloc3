# Tests backend

Date :
25/05/2026

Objectif :
Valider le fonctionnement du backend avant intégration frontend. J'ai oublié de créer un certains de commits pour certains des tests.

---

## Test 1 — Health Check

Route :
GET /health

Résultat :
200 OK

Vérifications :

- API démarrée
- Base de données accessible
- Monitoring simulé actif
- RPO = 15 min
- RTO = 1 heure

Statut :
VALIDÉ

---

## Test 2 — Authentification administrateur

Route :
POST /auth/login

Compte :

adminLocal@Motors

Résultat :

200 OK

Vérifications :

- JWT généré
- rôle admin reconnu

Statut :
VALIDÉ

---

## Test 3 — Authentification utilisateur

Route :
POST /auth/login

Compte :

userLocal@Motors

Résultat :

200 OK

Vérifications :

- JWT généré
- rôle user reconnu

Statut :
VALIDÉ

---

## Test 4 — Mauvais mot de passe

Route :
POST /auth/login

Résultat :

401 Unauthorized

Vérifications :

- accès refusé
- message d’erreur cohérent

Statut :
VALIDÉ

---

## Test 5 — Route protégée sans authentification

Route :
GET /auth/me

Résultat :

401 Unauthorized

Vérifications :

- accès anonyme refusé

Statut :
VALIDÉ

---

## Test 6 — Liste véhicules

Route :
GET /vehicles

Résultat :

200 OK

Vérifications :

- véhicules affichés
- achat/location distingués

Statut :
VALIDÉ

---

## Test 7 — Détail véhicule

Route :
GET /vehicles/4

Résultat :

200 OK

Vérifications :

- données cohérentes
- véhicule trouvé

Statut :
VALIDÉ

---

## Test 8 — Véhicule inexistant

Route :
GET /vehicles/9999

Résultat :

Erreur gérée

Vérifications :

- réponse cohérente
- cas limite pris en compte

Statut :
VALIDÉ

## Test 9 — Dépôt de dossier avec document

Commande :
pytest tests/test_applications.py -v

Résultat :
PASSED

Vérifications :
- création dossier authentifié
- document PDF accepté
- statut initial pending

Statut :
VALIDÉ

---

## Test 10 — Suivi des dossiers utilisateur

Commande :
pytest tests/test_applications.py -v

Résultat :
PASSED

Vérifications :
- récupération des dossiers du client connecté

Statut :
VALIDÉ

---

## Test 11 — Accès dossier sans authentification

Commande :
pytest tests/test_applications.py -v

Résultat :
PASSED

Vérifications :
- accès refusé sans token
- réponse 401

Statut :
VALIDÉ

---

## Test 12 — Cohérence type dossier / véhicule

Commande :
pytest tests/test_applications.py -v

Résultat :
PASSED

Vérifications :
- un dossier location ne peut pas être créé sur un véhicule en vente
- réponse 400

Statut :
VALIDÉ

---

## Test 13 — Administration des dossiers

Commande :
pytest tests/test_admin.py -v

Résultat :
4 passed

Vérifications :
- validation d’un dossier par admin
- consultation des dossiers par admin
- refus d’accès admin à un simple utilisateur
- bascule véhicule vente/location

Statut :
VALIDÉ

---

## Rapport de couverture backend

Commande :
pytest --cov=app --cov-report=term-missing

Résultat :
19 tests passed

Couverture totale :
92 %

Analyse :
La couverture dépasse l’objectif de 80 % demandé. Les modules critiques sont couverts : authentification, véhicules, dossiers, administration, sécurité et healthcheck.

Warnings :
Des avertissements de dépréciation liés à python-jose apparaissent avec Python 3.13. Ils ne bloquent pas l’exécution des tests.

---

## Test 14 — Intégration frontend / backend catalogue

Test :
Affichage de la page véhicules depuis le frontend React.

URL :
http://localhost:5173/search

Résultat :
VALIDÉ

Vérifications :
- le frontend démarre avec Vite ;
- l’API FastAPI est appelée correctement ;
- les véhicules sont affichés ;
- les modes achat/location sont distingués ;
- les erreurs “Failed to fetch” disparaissent quand le backend est lancé.

## Test 15 — Workflow complet client / administration

Résultat :
VALIDÉ

Vérifications :
- connexion utilisateur
- dépôt dossier
- upload document
- suivi dossier client
- connexion admin
- validation dossier
- commentaire visible côté client
