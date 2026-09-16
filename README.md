# PRONTO - Dashboard qualite IPS/DNB

PRONTO est un prototype de dashboard interactif pour auditer et explorer la qualite des donnees educatives francaises, dans le cadre du framework LADIQ.

Les ressources necessaires sont regroupees dans :

- `data/fr-en-ips-colleges-ap2023.csv` : donnees IPS chargees par le dashboard ;
- `data/fr-en-dnb-par-etablissement.csv` : source DNB conservee pour les analyses et extensions ;
- `assets/LADIQ_framework.png` : schema du framework affiche dans l'interface.

## Demonstration

L'application est developpee avec Streamlit et Plotly. Le dashboard presente :

- la completude et la coherence des donnees ;
- la relation entre l'Indice de Position Sociale (IPS) et les resultats du DNB ;
- des statistiques par secteur, session et region ;
- une analyse Random Forest et des courbes ALE ;
- un suivi des dimensions de qualite selon LADIQ.

> Les valeurs IPS sont chargees depuis le fichier DEPP empaquete. Les variables DNB utilisees pour le prototype sont generees pour la demonstration et ne constituent pas une publication statistique officielle.

## Lancer localement

```bash
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deployer avec Streamlit Community Cloud

1. Publier `app.py`, `requirements.txt` et `README.md` dans un depot GitHub public.
2. Ouvrir https://share.streamlit.io et choisir le depot.
3. Selectionner la branche puis `app.py` comme fichier principal.
4. Partager l'URL generee dans le CV.

Aucun secret ni aucune variable d'environnement n'est necessaire pour cette version de demonstration.

## Competences mobilisees

Python, Pandas, NumPy, scikit-learn, Streamlit, Plotly, data cleaning, data quality, data validation, exploratory data analysis, statistical analysis, Random Forest, ALE plots, data visualization, dashboard design, open data.

## Contexte

Projet realise a l'IMT Atlantique dans le cadre d'un projet de qualite des donnees. Les travaux s'appuient sur le framework LADIQ et sur des donnees educatives publiques de la DEPP.
