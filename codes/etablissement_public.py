import pandas as pd
import json

# Tes fichiers habituels
FILE_IPS = 'fichierscsv/fr-en-ips-colleges-ap2023.csv'
FILE_BREVET = 'fichierscsv/fr-en-indicateurs-valeur-ajoutee-colleges.csv'

def clean_numeric(series):
    return pd.to_numeric(series.astype(str).str.replace(',', '.'), errors='coerce')

print("🔄 Préparation des données pour le site web...")

# 1. Chargement
df_ips = pd.read_csv(FILE_IPS, sep=';', encoding='utf-8-sig')
df_brut = pd.read_csv(FILE_BREVET, sep=';', encoding='utf-8-sig')

df_ips['IPS'] = clean_numeric(df_ips['IPS'])
df_brevet = df_brut[df_brut['Session'] == 2024].copy()
df_brevet['Taux_Reussite'] = clean_numeric(df_brevet["Taux de réussite G"])

# 2. Fusion
df = pd.merge(
    df_ips[['UAI', 'Nom de l\'établissement', 'Nom de la commune', 'Secteur', 'IPS']], 
    df_brevet[['UAI', 'Taux_Reussite']], 
    on='UAI', how='inner'
).dropna(subset=['IPS', 'Taux_Reussite'])

# --- ⚠️ NOTE POUR LA CARTE GPS ---
# Tes fichiers CSV de base n'ont pas les coordonnées GPS exactes (Latitude/Longitude).
# Pour que la liste et la recherche marchent, on met des zéros par défaut.
# (La carte affichera tout au même endroit pour l'instant).
df['lat'] = 46.0 
df['lon'] = 2.0  

# 3. Formatage pour le site web
df = df.rename(columns={
    "Nom de l'établissement": "nom",
    "Nom de la commune": "ville",
    "Secteur": "secteur",
    "IPS": "ips",
    "Taux_Reussite": "taux"
})

# 4. Création du fichier Javascript
records = df.to_dict(orient='records')
js_content = "const collegesData = " + json.dumps(records, ensure_ascii=False) + ";"

with open("mes_colleges.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ SUCCESS : Fichier 'mes_colleges.js' créé avec {len(df)} établissements !")