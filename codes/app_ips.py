import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # Bibliothèque puissante pour les cartes interactives
from pathlib import Path

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Audit IPS & Réussite au Brevet", layout="wide")

@st.cache_data # Pour éviter de recharger les fichiers à chaque clic
def load_data():
    root = Path(__file__).resolve().parent.parent
    data_dir = root / 'fichierscsv'

    df_ips_path = data_dir / 'fr-en-ips-colleges-ap2023.csv'
    df_brevet_path = data_dir / 'fr-en-indicateurs-valeur-ajoutee-colleges.csv'

    df_ips = pd.read_csv(df_ips_path, sep=';')
    df_brevet = pd.read_csv(df_brevet_path, sep=';')
    
    # Nettoyage rapide (version simplifiée)
    df_ips['IPS'] = pd.to_numeric(df_ips['IPS'].astype(str).str.replace(',', '.'), errors='coerce')
    df_brevet = df_brevet[df_brevet['Session'] == 2024].copy()
    df_brevet['Note_Ecrit'] = pd.to_numeric(df_brevet["Note à l'écrit G"].astype(str).str.replace(',', '.'), errors='coerce')
    
    # IMPORTANT : On garde le nom de l'Académie tel quel pour le GeoJSON
    df = pd.merge(df_ips[['UAI', 'Nom de l\'établissement', 'IPS', 'Académie']], 
                  df_brevet[['UAI', 'Note_Ecrit']], on='UAI').dropna()
    return df

df = load_data()

# --- TITRE PRINCIPAL ---
st.title("📊 Tableau de Bord : IPS vs Réussite au Brevet")
st.markdown("Analyse géographique et statistique de la corrélation sociale.")

# --- CRÉATION DES ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🔬 Audit Scientifique", "🌍 Vue Citoyenne", "🗺️ Carte Géographique"])

# --- ONGLET 1 : SCIENTIFIQUE (Inchangé) ---
with tab1:
    st.header("Analyse Statistique & Machine Learning")
    # ... (Garde ton code boxplot et regplot ici) ...

# --- ONGLET 2 : GRAND PUBLIC (Inchangé) ---
with tab2:
    st.header("Le 'Thermomètre' de votre collège")
    # ... (Garde ton code thermomètre et moteur de recherche ici) ...

# --- ONGLET 3 : LA CARTE (Nouveau !) ---
with tab3:
    st.header("Fractures Territoriales en France")
    
    # 1. Préparation des données pour la carte (Grouper par Académie)
    df_map = df.groupby('Académie').agg({
        'IPS': 'mean',
        'Note_Ecrit': 'mean',
        'UAI': 'count' # Pour afficher le nombre d'établissements
    }).reset_index()
    df_map = df_map.rename(columns={'UAI': 'Nb_Etablissements'})

    # 2. Sélecteur de variable à visualiser
    variable = st.radio("Sélectionner la donnée à visualiser :", 
                        ('IPS Moyen', 'Note Moyenne au Brevet'))
    
    # Mapping des noms pour Plotly
    var_map = {'IPS Moyen': 'IPS', 'Note Moyenne au Brevet': 'Note_Ecrit'}
    selected_var = var_map[variable]
    color_scale = px.colors.sequential.Bluered if selected_var == 'IPS' else px.colors.sequential.YlGnBu

    st.subheader(f"Carte de France par Académie : {variable}")
    
    # 3. Lien vers le GeoJSON des académies (Hébergé en ligne pour Streamlit Cloud)
    geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/academies-avec-outre-mer.geojson"
    
    # 4. Création de la carte Plotly Choropleth
    fig_map = px.choropleth_mapbox(df_map, 
                                geojson=geojson_url, 
                                locations='Académie',  # Colonne commune dans le GeoJSON et ton DF
                                featureidkey='properties.nom', # Clé dans le GeoJSON
                                color=selected_var,
                                color_continuous_scale=color_scale,
                                mapbox_style="carto-positron",
                                zoom=5, 
                                center={"lat": 46.2276, "lon": 2.2137}, # Centre de la France
                                opacity=0.8,
                                labels={'IPS': 'IPS Moyen', 'Note_Ecrit': 'Note / 20', 'Nb_Etablissements': 'Collèges'}
                               )
    
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # Carte plein écran
    
    st.plotly_chart(fig_map, use_container_width=True) # Affichage interactif

    # Affichage du tableau de données en dessous pour référence
    st.dataframe(df_map.sort_values(by=selected_var, ascending=False))