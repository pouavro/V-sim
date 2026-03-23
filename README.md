# 🚀 Simulateur de Propagation (Épidémie sur Grille)
![Logo V-Sim](logo_vsim.png)
## 📝 Description

Ce projet est un simulateur interactif développé en Python, modélisant la propagation d'une épidémie au sein d'une population sur une grille 2D. Contrairement à une simulation statique, ce programme met en scène des **individus mobiles** dont les déplacements influencent dynamiquement les zones de risque en temps réel.

L'objectif est d'analyser l'interaction entre l'environnement (cases fixes) et des agents porteurs (personnages) à travers un système de **hitbox de contamination**.

---

## ⚙️ Logique des États

La simulation repose sur une machine à états finis appliquée à chaque cellule de la grille :

| État | Représentation Visuelle | Signification |
| :--- | :--- | :--- |
| **0** | 🟨 Beige | Case vide ou obstacle. |
| **1** | 🟩 Vert | Case saine (zone sécurisée). |
| **2** | 🟥 Rouge | **Infectee** : endroit pile de l'infecter. |
| **3** | 🟥 Rouge foncé | **zone infectee** : hitbox de l'infecter. |

---

## 🛠️ Aspects Techniques 

Ce projet exploite plusieurs concepts fondamentaux du programme de spécialité NSI :

### 📊 Structures de données
* **Dictionnaires (`dict`) :** La grille est gérée par une structure `grille = {(lig, col): données}`. Cela permet une recherche et une mise à jour des cases en **complexité temporelle constante $O(1)$**, garantissant la fluidité de l'interface même sur de grandes grilles.
* **Modélisation de voisinage :** Calcul algorithmique des zones d'infection via des vecteurs de déplacement `directions = [(dx, dy), ...]` (Voisinage de Moore).

### 💻 Programmation et Interface
* **Interface Graphique (GUI) :** Utilisation de **Tkinter** pour la gestion de la fenêtre, du Canvas et de la boucle événementielle.
* **Modularité :** Séparation claire entre la **logique métier** (calcul des infections) et la **couche visuelle** (rafraîchissement du Canvas).
* **Programmation Fonctionnelle :** Utilisation de fonctions `lambda` pour la gestion dynamique des commandes des boutons.

---

## 👥 L'Équipe

* **Ilan Vast** ([@pouavro](https://github.com/pouavro)) : Algorithmique de propagation, gestion de la structure de données et logique de déplacement.
* **Lucas** ([@zewaave](https://github.com/zewaave)) : Interface utilisateur (UI), design graphique et gestion des assets visuels.

---

## 🚀 Installation et Utilisation

1.  **Prérequis :** Python 3.10 ou supérieur.
2.  **Installation :** Téléchargez le script et assurez-vous que le fichier `perso 1.png` est présent à la racine du dossier.
3.  **Lancement :**
    ```bash
    python main.py
    ```
4.  **Simulation :** Cliquez sur **Simuler** pour générer les zones de danger et sur **Déplacement** pour observer l'évolution de l'épidémie avec le mouvement des porteurs.

---

## 📈 Évolutions possibles

* Ajout d'un graphique de suivi (S-I-R : Sains, Infectés, Rétablis) en temps réel.
* Implémentation de différents types d'individus (médecins, personnes immunisées).
* Réglage dynamique des probabilités via des curseurs (`Scale`) Tkinter.
