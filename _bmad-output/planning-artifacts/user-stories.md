---
project_name: dont-stop-til-you-get-enough
user_name: Boss
date: '2026-03-10'
---

# User Stories

## Epic 1: Configuration du Jeu

### US1.1: Sélection du jeu
En tant qu'utilisateur, je veux sélectionner un jeu (Loto ou Euromillion) afin de configurer les paramètres spécifiques à ce jeu.

**Critères d'acceptation:**
- Liste déroulante pour choisir Loto ou Euromillion
- Les paramètres affichés correspondent au jeu sélectionné

### US1.2: Configuration des paramètres Loto
En tant qu'utilisateur, je veux configurer les paramètres du Loto afin de définir les conditions de mon batch.

**Paramètres:**
- Type: Loto / Grand-Loto / Super-Loto (select)
- Prix grille: float (input)
- Nombre de grilles: int ou range (double slider 1-1000)
- 2nd tirage: True / False / Les deux (radio)
- Prix 2nd tirage: float (input)
- Tirages historiques: range dates (double slider dates)

### US1.3: Configuration des paramètres Euromillion
En tant qu'utilisateur, je veux configurer les paramètres Euromillion afin de définir les conditions de mon batch.

**Paramètres:**
- Prix grille: float (input)
- Nombre de grilles: int ou range (double slider 1-1000)
- Etoile+: True / False / Les deux (radio)
- Prix Etoile+: float (input)
- Tirages historiques: range dates (double slider dates)

---

## Epic 2: Configuration du Modèle

### US2.1: Sélection du modèle
En tant qu'utilisateur, je veux sélectionner un modèle de prédiction afin de générer des prédictions.

**Critères d'acceptation:**
- Liste des modèles disponibles (Random, SameValue)
- Les paramètres affichés correspondent au modèle sélectionné

### US2.2: Configuration Random
En tant qu'utilisateur, je veux configurer le modèle Random afin de définir comment générer mes numéros aléatoires.

**Paramètres:**
- seed: timestamp / valeur fixe (select)

### US2.3: Configuration SameValue Loto
En tant qu'utilisateur, je veux configurer le modèle SameValue pour le Loto afin de définir mes numéros fixes.

**Paramètres:**
- numero1-5: int (input 1-49)
- numero_comp: int (input 1-10)

### US2.4: Configuration SameValue Euromillion
En tant qu'utilisateur, je veux configurer le modèle SameValue pour Euromillion afin de définir mes numéros et étoiles fixes.

**Paramètres:**
- numero1-5: int (input 1-50)
- etoile1-2: int (input 1-12)

---

## Epic 3: Exécution des Batchs

### US3.1: Lancement d'un batch
En tant qu'utilisateur, je veux lancer un batch avec mes paramètres afin de générer des prédictions.

**Critères d'acceptation:**
- Bouton "Lancer" avec paramètre itérations (stepper)
- Si range sur paramètres → lance plusieurs batchs
- Chaque batch reçoit un numéro unique auto-incrémenté

### US3.2: Affichage progression
En tant qu'utilisateur, je veux voir la progression en direct de mes batchs afin de suivre l'avancement.

**Critères d'acceptation:**
- Vue workers + batches en cours
- Progression mise à jour toutes les 500ms
- Résultats mis à jour en live

### US3.3: Arrêt des batchs
En tant qu'utilisateur, je veux pouvoir arrêter tous mes batchs en cours.

**Critères d'acceptation:**
- Bouton "Arrêter tout"
- Arrêt propre (pas de corruption données)

### US3.4: Reprise après crash
En tant qu'utilisateur, je veux que mes batchs reprennent automatiquement après un crash.

**Critères d'absorption:**
- État sauvegardé en SQLite
- Reprise depuis dernier point stable

### US3.5: Voir prochain tirage
En tant qu'utilisateur, je veux voir les prédictions pour le prochain tirage de mes batchs.

**Critères d'acceptation:**
- Menu contextuel par batch
- Bouton "Voir prochain tirage"
- Affiche les N itérations prédites

### US3.6: Mettre à jour batch
En tant qu'utilisateur, je veux mettre à jour un batch lorsque l'historique est mis à jour.

**Critères d'acceptation:**
- Compare prédiction avec vrai résultat
- Continue jusqu'au prochain tirage non historisé

---

## Epic 4: Résultats et Comparaison

### US4.1: Consultation des résultats
En tant qu'utilisateur, je veux consulter les résultats de mes batchs afin d'analyser les performances.

**Critères d'acceptation:**
- Métriques: Bons numéros (min/max/moy), Gains totaux, Coût total, ROI
- Différentes présentations selon le jeu

### US4.2: Comparaison multi-batch
En tant qu'utilisateur, je veux comparer plusieurs batchs afin d'identifier les meilleures configurations.

**Critères d'acceptation:**
- Filtres, tris, group by
- Liste des itérations par timestamp

### US4.3: Ajustement workers
En tant qu'utilisateur, je veux ajuster le nombre de workers en live.

**Critères d'acceptation:**
- Slider ou input pour nombre de workers
- Batches en cours redémarrent si nécessaire

---

## Epic 5: Gestion des Données

### US5.1: Téléchargement données FDJ
En tant qu'utilisateur, je veux télécharger automatiquement les données FDJ.

**Critères d'acceptation:**
- Scraping du site FDJ (Loto, Euromillion)
- Parsing CSV automatique

### US5.2: Données manuelles
En tant qu'utilisateur, je veux pouvoir fournir les données manuellement.

**Critères d'acceptation:**
- Upload de fichiers CSV
- Fallback si scraping échoue

### US5.3: Merge historique Loto
En tant qu'utilisateur, je veux que les 3 types de Loto soient mergés.

**Critères d'acceptation:**
- Merge Loto + Grand-Loto + Super-Loto en BDD
