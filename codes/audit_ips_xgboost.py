import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBRegressor  # Changement de modèle ici
from PyALE import ale
import os

# --- CONFIGURATION DES FICHIERS ---
FILE_IPS = 'fichierscsv/fr-en-ips-colleges-ap2023.csv'
FILE_BREVET = 'fichierscsv/fr-en-indicateurs-valeur-ajoutee-colleges.csv'

class IpsXGBoostAuditor:
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
            df_ips[['UAI', 'IPS', 'Is_Public']], 
            df_brevet[['UAI', 'Note_Ecrit', 'Candidats']], 
            on='UAI', 
            how='inner'
        ).dropna(subset=['IPS', 'Is_Public', 'Note_Ecrit', 'Candidats'])
        
        print(f"✅ Analyse prête sur {len(self.df)} établissements.")

    def run_ale_analysis(self):
        if self.df is None: return

        # Variables de prédiction
        features = ['IPS', 'Is_Public', 'Candidats']
        X = self.df[features]
        y = self.df['Note_Ecrit']

        print(f"🤖 Entraînement du modèle XGBoost sur : {features}")
        
        # Configuration de XGBoost
        model = XGBRegressor(
            n_estimators=150,
            learning_rate=0.08,
            max_depth=6,
            random_state=42,
            objective='reg:squarederror'
        )
        
        from sklearn.model_selection import cross_val_score
        model.fit(X, y)

        # Calcul de la qualité (R²) par validation croisée pour éviter le biais d'entraînement
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
        r2_score = cv_scores.mean()
        print(f"\n📈 Score de Qualité (R² CV-5) : {r2_score:.2f} ± {cv_scores.std():.2f}")
        print(f"Cela signifie que ~{r2_score*100:.1f}% de la note est expliquée par ces facteurs (validation croisée).")

        print("\n📊 Génération de la courbe ALE avec XGBoost...")
        # L'ALE isole l'effet de l'IPS
        ale_eff = ale(X=X, model=model, feature=['IPS'], grid_size=40, include_CI=True)
        
        # Personnalisation du graphique
        fig = plt.gcf()
        fig.set_size_inches(12, 7)
        ax = plt.gca()
        ax.set_title("Audit IPS : Effet Local Accumulé (Modèle XGBoost)\nImpact pur de l'IPS sur la Note au Brevet", fontsize=14)
        ax.set_xlabel("Indice de Position Sociale (IPS)", fontsize=12)
        ax.set_ylabel("Variation de la note (points)", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        
        os.makedirs("visualisation", exist_ok=True)
        plt.tight_layout()
        plt.savefig("visualisation/courbe_ale_ips_xgboost.png", dpi=150)
        print("💾 Graphique sauvegardé : visualisation/courbe_ale_ips_xgboost.png")
        plt.show()

# --- DÉMARRAGE ---
if __name__ == "__main__":
    auditor = IpsXGBoostAuditor(FILE_IPS, FILE_BREVET)
    auditor.prepare_data()
    auditor.run_ale_analysis()