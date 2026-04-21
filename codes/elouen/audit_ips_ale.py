import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from PyALE import ale
import os

# --- CONFIGURATION DES FICHIERS ---
FILE_IPS = 'fichierscsv/fr-en-ips-colleges-ap2023.csv'
FILE_BREVET = 'fichierscsv/fr-en-indicateurs-valeur-ajoutee-colleges.csv'

class IpsFullAuditor:
    def __init__(self, ips_path, brevet_path):
        self.ips_path = ips_path
        self.brevet_path = brevet_path
        self.df = None
        
        # Vérification de l'existence des fichiers
        if not os.path.exists(ips_path):
            raise FileNotFoundError(f"❌ Fichier IPS introuvable : {ips_path}")
        if not os.path.exists(brevet_path):
            raise FileNotFoundError(f"❌ Fichier Brevet introuvable : {brevet_path}")

    def clean_numeric(self, series):
        """Nettoie les colonnes numériques (gestion des virgules françaises)."""
        return pd.to_numeric(series.astype(str).str.replace(',', '.'), errors='coerce')

    def prepare_data(self):
        print("🔄 Chargement et fusion des données en cours...")
        
        # 1. Chargement IPS
        df_ips = pd.read_csv(self.ips_path, sep=';', encoding='utf-8-sig')
        df_ips['IPS'] = self.clean_numeric(df_ips['IPS'])
        
        # 2. Chargement Brevet (IVAC)
        df_brut = pd.read_csv(self.brevet_path, sep=';', encoding='utf-8-sig')
        
        # On cible la session la plus récente
        df_brevet = df_brut[df_brut['Session'] == 2024].copy()
        
        # Nettoyage des colonnes
        df_brevet['Note_Ecrit'] = self.clean_numeric(df_brevet["Note à l'écrit G"])
        df_brevet['Candidats'] = self.clean_numeric(df_brevet['Nb candidats G'])
        
        # 3. Encodage du Secteur (Public = 1, Privé = 0)
        df_ips['Is_Public'] = df_ips['Secteur'].map({'public': 1, 'prive': 0})
        
        # 4. Fusion sur le code UAI
        self.df = pd.merge(
            df_ips[['UAI', 'IPS', 'Is_Public', 'Académie']], 
            df_brevet[['UAI', 'Note_Ecrit', 'Candidats']], 
            on='UAI', 
            how='inner'
        ).dropna(subset=['IPS', 'Note_Ecrit', 'Candidats'])
        
        print(f"✅ Analyse prête sur {len(self.df)} établissements.")

    def run_ale_analysis(self):
        if self.df is None: return

        # Variables utilisées pour la prédiction (Features)
        features = ['IPS', 'Is_Public', 'Candidats']
        X = self.df[features]
        y = self.df['Note_Ecrit']

        print(f"🤖 Entraînement de la Forêt Aléatoire sur : {features}")
        model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
        model.fit(X, y)

        # --- AJOUT DU CALCUL DU R² ---
        r2_score = model.score(X, y)
        print("\n" + "="*40)
        print(f"📈 SCORE DE QUALITÉ DU MODÈLE (R²)")
        print(f"R² = {r2_score:.4f}")
        print(f"Interprétation : {r2_score*100:.1f}% de la variance de la note")
        print("au Brevet est expliquée par les variables choisies.")
        print("="*40 + "\n")

        # Calcul de l'importance
        importances = model.feature_importances_
        print("--- Importance des variables ---")
        for f, imp in zip(features, importances):
            print(f"📍 {f}: {imp:.1%}")

        print("\n📊 Génération de la courbe ALE pour l'IPS...")
        ale_eff = ale(X=X, model=model, feature=['IPS'], grid_size=40, include_CI=True)
        
        fig = plt.gcf()
        fig.set_size_inches(10, 6)
        ax = plt.gca()
        ax.set_title(f"Effet Local Accumulé (ALE) de l'IPS\n(Modèle Random Forest - R²: {r2_score:.2f})", fontsize=13)
        ax.set_xlabel("Indice de Position Sociale (IPS)")
        ax.set_ylabel("Impact sur la note (en points)")
        ax.axhline(0, color='black', linewidth=1, alpha=0.3)
        ax.grid(True, linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig("courbe_ale_ips_pure.png", dpi=150)
        print("💾 Graphique sauvegardé : courbe_ale_ips_pure.png")
        plt.show()

# --- DÉMARRAGE ---
if __name__ == "__main__":
    auditor = IpsFullAuditor(FILE_IPS, FILE_BREVET)
    auditor.prepare_data()
    auditor.run_ale_analysis()