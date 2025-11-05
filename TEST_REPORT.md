# Güdlft Registration — Rapport de Tests  
Version : v0.9.1  
Date : [à compléter, ex : 27 octobre 2025]  
Préparé par : [Ton nom]



## 1. Objectif
Ce rapport présente les résultats des tests automatisés effectués sur l’application Güdlft Registration.  
L’objectif est de garantir la conformité du comportement de l’application avec les spécifications fonctionnelles (phases 1 et 2).

---

## 2. Environnement de test

| Composant | Version / Outil |
|------------|----------------|
| Python | 3.13.5 |
| Flask | 3.x |
| Pytest | 8.4.2 |
| Coverage | 7.x |
| Système | macOS (Darwin) |
| Données utilisées | clubs.json, competitions.json |

---

## 3. Méthodologie de test
- Utilisation de la méthode **TDD (Test Driven Development)**.  
- Tests couvrant les cas de réussite et d’échec (happy paths et sad paths).  
- Vérification unitaire, d’intégration et de gestion d’erreurs.  
- Tous les tests sont automatisés via **Pytest**.

---

## 4. Résumé des résultats

### Résultat global Pytest
- 13 tests collectés
- 13 réussis en 0.03s

### couverture du code 

Name Stmts Miss Cover
server.py 101 1 99%
tests/conftest.py 19 0 100%
tests/test_booking_flow.py 20 0 100%
tests/test_homepage.py 3 0 100%
tests/test_login_flow.py 5 0 100%
tests/test_more_errores.py 23 0 100%
tests/test_smoke.py 2 0 100%
TOTAL 173 1 99%


---

## 5. Détails des scénarios de test

| Nom du test | Description | Résultat |
|--------------|-------------|----------|
| test_homepage_returns_200 | La page d’accueil renvoie un statut OK | Réussi |
| test_login_with_valid_email_shows_summary | Connexion réussie avec un email valide | Réussi |
| test_book_page_opens_for_valid_competition_and_club | La page de réservation s’ouvre correctement | Réussi |
| test_cannot_book_more_than_12_places | La limite de 12 places est respectée | Réussi |
| test_refuse_when_not_enough_points | Message d’erreur si points insuffisants | Réussi |
| test_successful_booking_deducts_points_and_confirms | Réservation validée et points déduits | Réussi |
| test_login_unknown_email_redirects | Email invalide géré correctement | Réussi |
| test_book_with_invalid_names_redirects_to_index | Redirection si compétition ou club invalides | Réussi |
| test_purchase_invalid_places_value | Entrée non numérique refusée | Réussi |
| test_purchase_with_unknown_entities_redirects | Gestion des entités inconnues | Réussi |
| test_points_endpoint_json | Endpoint /points fonctionne correctement | Réussi |
| test_logout_redirects | Déconnexion renvoie à l’accueil | Réussi |
| test_pytest_detects_tests | Vérification du fonctionnement de Pytest | Réussi |

---

## 6. Observations
- Aucun plantage détecté.  
- Tous les bogues de la phase 1 corrigés.  
- Les messages flash apparaissent correctement dans les templates.  
- Le code respecte les règles Flask et les pratiques de TDD.  

---

## 7. Conclusion
- Tous les tests sont passés avec succès.  
- Couverture totale : **99 %**.  
- Application stable, conforme aux spécifications fonctionnelles.  
- Prête pour validation finale QA et tests de performance.

