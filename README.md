# Simulateur de Propagation (Épidémie sur Grille)
![Logo V-Sim](V-sim_Logo.png)
## Description

Ce projet est un simulateur interactif développé en Python, modélisant la propagation d'une épidémie au sein d'une population sur une grille 2D. Contrairement à une simulation statique, ce programme met en scène des **individus mobiles** dont les déplacements influencent dynamiquement les zones de risque en temps réel.

L'objectif est d'analyser l'interaction entre l'environnement (cases fixes) et des agents porteurs (personnages) à travers un système de **hitbox de contamination**.

---

## Logique des États

La simulation repose sur une machine à états finis appliquée à chaque cellule de la grille :

| État | Code Couleur | Représentation Visuelle | Signification |
| :--- | :--- | :--- | :--- |
| **0** | `""` (Transparent) | 🖼️ **Fond de carte** | Case vide (laisse apparaître le décor `map1.png`). |
| **1** | `#0077b6` | 🔵 **Bleu foncé** | **Sain** : Position centrale du personnage en bonne santé. |
| **2** | `#bc4749` | 🔴 **Rouge brique** | **Infecté** : Position centrale du personnage malade. |
| **3** | `#ff8fa3` | 💓 **Rose / Rouge clair** | **Zone d'infection** : Hitbox de danger autour d'un malade. |
| **4** | `#ade8f4` | 💎 **Bleu ciel** | **Zone de présence** : Rayon visuel autour d'un personnage sain. |

---

## Aspects Techniques 

Ce projet exploite plusieurs concepts fondamentaux du programme de spécialité NSI :

### Structures de données
* **Dictionnaires (`dict`) :** La grille est gérée par une structure `grille = {(lig, col): données}`. Cela permet une recherche et une mise à jour des cases en **complexité temporelle constante $O(1)$**, garantissant la fluidité de l'interface même sur de grandes grilles.
* **Modélisation de voisinage :** Calcul algorithmique des zones d'infection via des vecteurs de déplacement `directions = [(dx, dy), ...]` (Voisinage de Moore).

### Programmation et Interface
* **Interface Graphique (GUI) :** Utilisation de **Tkinter** pour la gestion de la fenêtre, du Canvas et de la boucle événementielle.
* **Modularité :** Séparation claire entre la **logique métier** (calcul des infections) et la **couche visuelle** (rafraîchissement du Canvas).
* **Programmation Fonctionnelle :** Utilisation de fonctions `lambda` pour la gestion dynamique des commandes des boutons.

---

## L'Équipe

* **Ilan Vast** ([@pouavro](https://github.com/pouavro)) : Algorithmique de propagation, gestion de la structure de données et logique de déplacement.
* **Lucas** ([@zewaave](https://github.com/zewaave)) : Interface utilisateur (UI), design graphique et gestion des assets visuels.

---

## Installation et Utilisation
1. **Copier** le dossier `version finale` sur votre PC.
2. **Ouvrir** le dossier (ne pas rester dans le .zip).
3. **Lancer** le fichier `main.py` (Double-clic ou via terminal).

> **Important :** Le dossier `images` doit rester au même endroit que `main.py` pour que les graphiques s'affichent.

---

## Évolutions possibles

* Ajout d'un graphique de suivi (S-I-R : Sains, Infectés, Rétablis) en temps réel.
* Implémentation de différents types d'individus (médecins, personnes immunisées).
* Réglage dynamique des probabilités via des curseurs (`Scale`) Tkinter.
