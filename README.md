# PRONTO 🎓 — Système d'Audit Qualité de Données & Dashboard LADIQ (IPS / Brevet)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20+-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![IMT Atlantique](https://img.shields.io/badge/École-IMT%20Atlantique-00A3A6?style=flat)](https://www.imt-atlantique.fr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Système d'audit automatisé et dashboard décisionnel pour fiabiliser et analyser l'impact de la qualité des données éducatives ouvertes (IPS & Brevet des collèges) selon le cadre méthodologique LADIQ.**

---

### 🌐 Démonstration en Ligne (Accès Recruteurs)

👉 **Lien direct vers le Dashboard interactif :**  
L'application Streamlit est déployée et accessible directement en ligne sur **Streamlit Community Cloud** :  
**[🔗 Ouvrir le Dashboard PRONTO en direct](https://pronto-imt.streamlit.app)** *(ou via [share.streamlit.io](https://share.streamlit.io))*

---

## 🎯 Problématique & Cas d'Usage

Dans le système éducatif français, les décisions d'allocation de moyens et de mixité reposent sur des indicateurs clés :
- **L'Indice de Position Sociale (IPS)** des collèges (DEPP)
- **Les résultats du Diplôme National du Brevet (DNB)** par établissement

Comment la **qualité des données** (manquants historiques, recalibrage 2022 des pondérations PCS, syntaxe des UAI) influence-t-elle la robustesse des indicateurs et les décisions publiques ?

PRONTO implémente le cadre d'évaluation **LADIQ (Learning Analytics Data Quality Framework)** à travers 5 dimensions fondamentales :
- **Complétude (C)** : Taux de remplissage effectif des données (99.9% post-2022 vs ~94% historique).
- **Actualité (Act)** : Prise en compte de la volatilité temporelle et de la fraîcheur des sessions.
- **Exactitude (E)** : Contrôle syntaxique rigoureux par expressions régulières (ex. format UAI `^\d{7}[A-Z]$`).
- **Logique (L)** : Vérification des bornes métier (IPS ∈ [38, 192], taux de réussite ∈ [0%, 100%]).
- **Intelligibilité (I)** : Documentation sémantique des colonnes et traçabilité des transformations.

---

## 📊 Fonctionnalités Clés du Dashboard

| Onglet | Contenu & Analyses |
| :--- | :--- |
| **📊 Vue d'ensemble** | Nuage de points IPS × Note DNB avec droite de régression OLS ($r = 0.87$), distributions par secteur public/privé, répartition par quintiles. |
| **🔍 Complétude & Cohérence** | Évolution temporelle (2016-2021 vs 2022 vs 2023+), jauges de cohérence temporelle, analyse de rupture du recalibrage 2022 des PCS. |
| **📈 Corrélation & ALE** | Modèle **Random Forest ($R^2 = 0.93$)**, importance des variables (IPS à 78%), **courbes ALE (Accumulated Local Effects)** avec bande d'intervalle de confiance à 95%. |
| **🗺️ Analyse Régionale** | Barplot comparatif des IPS régionaux, bubble chart interactif (taille = effectif, couleur = taux de réussite) et tableau détaillé. |
| **📋 Cadre LADIQ** | Avancement des 6 phases LADIQ, diagramme radar multidimensionnel de qualité et roadmap du projet. |

---

## 🔬 Résultats & Méthodologie Statistique

- **Corrélation linéaire robuste :** Pearson $r = 0.87$ entre l'IPS et la note moyenne à l'écrit du Brevet.
- **Régression non-linéaire (Random Forest) :** $R^2 = 0.93$, validant que l'environnement socio-économique reste le prédicteur prépondérant de la performance scolaire globale.
- **Effets Locaux Cumulés (ALE Plots) :** Décomposition de l'effet marginal pur de l'IPS en neutralisant les effets confondants (secteur public/privé, taille d'établissement) :
  - **IPS ~ 55 (très défavorisé) :** impact marginal de **$-3.3$ points** sur la note au brevet.
  - **IPS ~ 100 (référence moyenne nationale) :** impact nul ($0$ pt).
  - **IPS ~ 160 (très favorisé) :** impact marginal de **$+4.5$ points**.

---

## 🗂️ Structure du Projet

```text
pronto/
├── app.py                             # Point d'entrée principal du Dashboard Streamlit
├── requirements.txt                   # Dépendances de production
├── LADIQ_framework.png                # Schéma du framework LADIQ
├── CV_PRONTO.md                       # Guide de valorisation CV & Recruteurs (FR / EN)
│
├── codes/                             # Pipeline d'audit et traitement de données
│   ├── nettoyeur_de_donnees.py        # Moteur d'audit automatisé LADIQ (C, A, L, Act, I)
│   ├── audit_ips_ale.py               # Calcul des courbes ALE et modèle Random Forest
│   ├── audit_ips_xgboost.py           # Modélisation alternative XGBoost
│   ├── visualisation_nettoyage.py     # Génération des preuves visuelles avant/après
│   └── visualisation_IPS.py           # Études de dispersion et visualisations thématiques
│
├── stream/                            # Module Streamlit autonome
│   ├── app.py                         # Code source du dashboard interactif
│   └── requirements.txt               # Spécification des paquets Python
│
├── fichierscsv/                       # Jeux de données ouverts sources (DEPP)
│   ├── fr-en-ips-colleges-ap2023.csv
│   └── fr-en-dnb-par-etablissement.csv
│
├── fichiers_certifies/                # Jeux de données certifiés après audit LADIQ
│   ├── CLEANED_fr-en-ips-colleges-ap2023.csv
│   └── CLEANED_fr-en-dnb-par-etablissement.csv
│
└── visualisation/                     # Preuves visuelles générées
```

---

## ⚡ Installation et Exécution Locale

### 1. Cloner le dépôt
```bash
git clone https://github.com/elouenlm/pronto.git
cd pronto
```

### 2. Créer l'environnement virtuel et installer les dépendances
```bash
python -m venv .venv

# Sur Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Sur Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Lancer le dashboard Streamlit
```bash
streamlit run app.py
```
L'interface s'ouvre automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

---

## ☁️ Déploiement Cloud (Streamlit Community Cloud)

Ce projet est pré-configuré pour un déploiement continu et gratuit en 1 clic :
1. Rendez-vous sur **[share.streamlit.io](https://share.streamlit.io)**
2. Connectez votre compte GitHub.
3. Sélectionnez le dépôt `elouenlm/pronto`, branche `main`, fichier `app.py`.
4. Cliquez sur **Deploy** ! L'application est mise à jour automatiquement à chaque nouveau `git push`.

---

## 👥 Équipe de Réalisation (IMT Atlantique)

Projet conçu et développé dans le cadre de la formation d'ingénieur à l'**IMT Atlantique Brest** :
- **Elouen LE MAGUET** — *Lead Data & Statistiques* (Modélisation, pipeline de qualité, architecture analytique)
- **Brayan VIDAL** — *Lead Recherche & État de l'art*
- **Paul LE NY** — *Lead Développement & Visualisation*
- **Supervision :** Fahima Djelil (Enseignante-chercheuse, IMT Atlantique)

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Données sources sous Licence Ouverte (Etalab / DEPP Ministère de l'Éducation Nationale).
