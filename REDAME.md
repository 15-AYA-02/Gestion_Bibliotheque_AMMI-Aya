# Gestion de Bibliothèque (Tkinter + Matplotlib)

## Auteur
**Aya Ammi**

## Installation

### 1. Cloner le dépôt
git clone https://github.com/15-AYA-02/Gestion_Bibliotheque_AMMI-Aya.git
cd Gestion_Bibliotheque
### 2. Créer un environnement virtuel 
python -m venv venv
venv\Scripts\activate
### 3. Installer les dépendances
pip install -r requirements.txt
##  Lancer l'application
python src/main.py

## Fonctionnalités principales

-  Ajouter / supprimer des **livres**
-  Ajouter des **membres**
- Gérer les **emprunts / retours**
-  Générer des **statistiques graphiques** :
  - Diagramme circulaire par genre
  - Histogramme des auteurs les plus populaires
  - Courbe des emprunts sur les 30 derniers jours
## Structure du projet
Gestion_Bibliotheque/
├── src/
│   ├── main.py
│   ├── bibliotheque.py
│   ├── exceptions.py
│   ├── visualisations.py
├── data/
│   ├── livres.txt
│   ├── membres.txt
│   └── historique.csv
├── assets/
│   └── stats_auteurs.png
    └── stats_emprunts.png
    └── stats_genres.png
├── README.md
└── requirements.txt
## Exemples d'utilisation:

### 1. Interface d'ajout de livre
(assets/ajout_livre.png)

### 2. Interface d'ajout de membre
(assets/ajout_membre.png)

### 3. Emprunt  de livre

(assets/emprunt_livre.png)
### 4.retour de livre

(assets/rendre_livre.png)
### 5.Statistiques générées automatiquement

(assets/statistiques.png)
  
## Crédits
Projet développé par **Aya AMMI** 