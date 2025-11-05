# Güdlft Registration — Rapport de Tests
Version : v1.0.0  
Date : 05 novembre 2025  
Préparé par : Adrien Fischer

## 1. Objectif
Ce rapport présente les résultats des tests automatisés effectués sur l’application Güdlft Registration.  
L’objectif est de garantir la conformité du comportement de l’application avec les spécifications fonctionnelles.

---

## 2. Environnement de test

| Composant | Version / Outil |
|-----------|------------------|
| Python    | 3.13.5           |
| Flask     | 3.x              |
| Pytest    | 8.4.2            |
| Coverage  | 7.x (plugin pytest-cov 7.0.0) |
| Système   | macOS (Darwin)   |
| Données   | clubs.json, competitions.json (isolés via fixtures) |

---

## 3. Méthodologie
- Approche **TDD** quand pertinent.  
- Tests **unitaires** (fonctions pures, sans Flask ni fichiers).  
- Tests **d’intégration** (client Flask, routes principales, cas succès/erreur).  
- **Isolation des données** via `conftest.py` (tmp + monkeypatch des chemins JSON).  

---

## 4. Résultats Pytest

### Exécution complète
```
30 tests collectés
30 réussis
Durée (run -v) : 0.08 s
```

### Couverture du code
Commande : `pytest --cov=server --cov-report=term-missing`

```
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
server.py     115      3    97%   118, 134, 156
-----------------------------------------
TOTAL         115      3    97%
```

---

## 5. Périmètre couvert (exemples représentatifs)

### Intégration
- `GET /` : page d’accueil OK.  
- `POST /showSummary` : connexion email valide et invalide (200/302 attendus).  
- `GET /book/<competition>/<club>` : page de réservation accessible.  
- `POST /purchasePlaces` : limite 12 places, points insuffisants, succès.  
- `GET /points` : réponse JSON attendue.  
- `GET /logout` : redirection attendue.

### Unitaire (fonctions pures)
- `can_book(points, requested)` : règles métier (≤12, points suffisants).  
- `sanitize_places(value)` : conversion contrôlée vers entier positif.  
- `calculate_remaining_places(total, booked)` : calcul simple et validations.

---

## 6. Observations
- Aucun plantage.  
- Cas limites pris en charge (entrées invalides, noms inconnus, dépassement des quotas).  
- Les lignes non couvertes (118, 134, 156) correspondent à des branches peu probables et non critiques.

---

## 7. Conclusion
- **30/30 tests réussis**.  
- **Couverture : 97 %** sur `server.py`.  
- L’application est stable et conforme au périmètre fonctionnel visé.
