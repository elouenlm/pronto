# PRONTO - Validation d'un framework de conception d'indicateurs de qualité à partir de données de qualité

Etudiants : 

LE MAGUET Elouen
LE NY Paul
VIDAL Brayan

> **Projet de Qualité des Données** - Système d'audit automatisé basé sur le framework LADIQ pour nettoyer et certifier les données éducatives françaises, pour observer l'influence des données incomplètes sur la décision d'un indicateur dans le domaine de l'éducation.

---

### Cas d'usage
Ce projet traite deux types de données du système éducatif français :
- **IPS (Indice de Position Sociale)** des collèges
- **Résultats du DNB (Diplôme National du Brevet)** par établissement

Le système évalue 5 dimensions de la qualité :
- **C**omplétude : Taux de remplissage des cellules
- **A**ctualité : Fraîcheur temporelle des données
- **E**xactitude : Conformité syntaxique (regex)
- **L**ogique : Cohérence des valeurs métier
- **I**ntelligibilité : Documentation des colonnes


## 🗂️ Structure du projet

```
pronto/
├── codes/
│   ├── nettoyeur_de_donnees.py        # Moteur d'audit LADIQ
│   └── visualisation_nettoyage.py     # Génération de preuves visuelles
├── fichierscsv/                       # Données brutes (input)
│   ├── fr-en-ips-colleges-ap2023.csv
│   ├── fr-en-ips-colleges-ap2022.csv
│   ├── fr-en-ips_colleges.csv
│   └── fr-en-dnb-par-etablissement.csv
├── fichiers_certifies/                # Données nettoyées (output)
│   ├── CLEANED_fr-en-ips-colleges-ap2023.csv
│   └── CLEANED_fr-en-dnb-par-etablissement.csv
├── visualisation/                     # Graphiques de preuve
│   ├── preuve1_volume_lignes.png
│   └── preuve2_distribution_maths.png
├── references/                        # Documentation annexe
└── README.md
```

---

## ⚙️ Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Cloner le dépôt**
```bash
git clone https://gitlab-df.imt-atlantique.fr/b25vidal/pronto.git
cd pronto
```

2. **Installer les dépendances**
```bash
pip install pandas matplotlib seaborn scipy streamlit plotly scikit-fuzzy numpy
```

---

## 🚀 Utilisation

### 1. Nettoyage des données

Exécutez le script d'audit principal :

```bash
python codes/nettoyeur_de_donnees.py
```

**Sortie attendue :**
```
09:14:00 | 🧠 RAISONNEMENT | Fichier 'fr-en-ips-colleges-ap2023.csv' chargé. (13972 lignes, 24 colonnes)
...
============================================================
🧐 RAPPORT D'AUDIT IA : fr-en-ips-colleges-ap2023.csv
NOTE GLOBALE : 72.49%
============================================================
09:14:01 | 🧠 RAISONNEMENT | 💾 SUCCÈS : Nouveau fichier généré -> fichiers_certifies\CLEANED_fr-en-ips-colleges-ap2023.csv
```

Les fichiers certifiés seront générés dans `fichiers_certifies/`.

### 2. Génération des visualisations

Créez les preuves visuelles pour comparer avant/après :

```bash
python codes/visualisation_nettoyage.py
```

**Sortie attendue :**
```
Chargement des fichiers pour la comparaison visuelle...
✅ Graphique 1 généré : preuve1_volume_lignes.png
✅ Graphique 2 généré : preuve2_distribution_maths.png
```

Les graphiques seront sauvegardés dans `visualisation/`.

### 3. Dashboard interactif

Lancez l'application Streamlit pour visualiser le diagnostic et les analyses en temps réel :

```bash
python -m streamlit run pronto/codes/elouen/app.py
```

Le dashboard s'ouvre ensuite dans votre navigateur sur `http://localhost:8503`.

---

## Sources du dashboard

- Données synthétiques inspirées par les publications DEPP 2022-2024.
- Méthodologie basée sur le cadre LADIQ pour la qualité des données.
- Visualisation interactive développée avec Streamlit et Plotly.

## Métriques de qualité

Le système calcule une **note globale** basée sur la formule LADIQ :

```
Score = (C × A × L × Act × I) × 100
```

Où :
- **C** = Complétude (% cellules remplies)
- **A** = Exactitude (% lignes valides syntaxiquement)
- **L** = Logique (% valeurs dans les bornes métier)
- **Act** = Actualité (fraîcheur temporelle selon volatilité)
- **I** = Intelligibilité (% colonnes documentées)

---

## Exemples de règles appliquées

### IPS (volatilité = 5 ans)
- **Code UAI** : Format `^\d{7}[A-Z]$` (ex: 0010001A)
- **IPS** : Valeur entre 45 et 185
- **Année** : Données de moins de 5 ans

### DNB (volatilité = 2 ans)
- **Code établissement** : Format `^\d{7}[A-Z]$`
- **Taux de réussite** : Entre 0% et 100%
- **Session** : Données de moins de 2 ans

---

## 👥 Auteurs

Projet réalisé dans le cadre du cours de PRONTO - IMT Atlantique.

---

## 📝 Licence

Projet académique - IMT Atlantique 2026.
