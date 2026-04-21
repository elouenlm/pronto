# Dashboard PRONTO — Groupe 59

## Évaluation qualité de l'indicateur IPS/DNB selon le cadre LADIQ

**IMT Atlantique Brest · Avril 2026**  
Équipe : Le Maguet · Vidal · Le Ny  
Encadrant : Fahima Djelil

---

## Lancement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer le dashboard
streamlit run app.py
```

Le dashboard s'ouvre automatiquement sur `http://localhost:8501`

---

## Fonctionnalités

### 📊 Vue d'ensemble
- Nuage de points IPS × Note DNB avec droite de régression (r = 0,87)
- Distribution de l'IPS par secteur (public/privé)
- Note DNB par quintile IPS
- Évolution par session (2022–2024)

### 🔍 Complétude & Cohérence
- Évolution de la complétude IPS par période (2016–2021 / 2022 / 2023+)
- Scores de cohérence temporelle (IPS et DNB)
- Impact du recalibrage 2022 sur les pondérations PCS

### 📈 Corrélation & ALE
- Courbe ALE (Accumulated Local Effects) de l'IPS sur la note au Brevet
- Importance des variables du modèle Random Forest (R² = 0,93)
- Points clés : IPS 55 → −3,3 pts | IPS 100 → 0 | IPS 160 → +4,5 pts

### 🗺️ Analyse Régionale
- IPS moyen par région (barplot + carte bubble)
- Tableau détaillé avec taux de réussite

### 📋 Cadre LADIQ
- Avancement des 6 phases LADIQ
- Radar des dimensions de qualité
- Planning des jalons (S15 → S23)

---

## Pour connecter vos données réelles

Remplacez la fonction `generate_data()` dans `app.py` par :

```python
@st.cache_data
def load_real_data():
    df_ips = pd.read_csv('fichierscsv/fr-en-ips-colleges-ap2023.csv', sep=';', encoding='utf-8-sig')
    df_dnb = pd.read_csv('fichierscsv/fr-en-indicateurs-valeur-ajoutee-colleges.csv', sep=';', encoding='utf-8-sig')
    # ... fusion sur UAI comme dans audit_ips_ale.py
    return df
```

---

## Structure

```
dashboard_pronto/
├── app.py              # Dashboard principal
├── requirements.txt    # Dépendances Python
└── README.md           # Ce fichier
```

---

## Références

- Djelil & Mandran (2025). LADIQ framework. LAK'25.
- Rocher (2016, 2023). Construction et actualisation de l'IPS. DEPP.
- Dauphant et al. (2023). L'IPS : un outil statistique. Note d'Info n°23.16. DEPP.
- Apley & Zhu (2020). ALE plots. Journal of the Royal Statistical Society.
