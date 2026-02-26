import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class IpsCoherenceAuditor:
    """
    Auditeur spécialisé dans la stabilité temporelle de l'IPS.
    Compare les périodes Pré-2022, 2022 et Post-2022.
    """
    
    def __init__(self, files_dict: dict):
        self.files = files_dict
        self.dataframes = {}
        self.merged_df = None

    def _load_and_clean(self, key: str, path: str):
        """Charge un fichier et prépare l'IPS (conversion numérique)."""
        print(f"🔄 Chargement de la période : {key}")
        df = pd.read_csv(path, sep=';', encoding='utf-8-sig', low_memory=False)
        
        # On force l'IPS en numérique (gestion des virgules françaises)
        df['IPS'] = pd.to_numeric(df['IPS'].astype(str).str.replace(',', '.'), errors='coerce')
        
        # On ne garde que la dernière année disponible dans chaque fichier pour l'UAI
        df = df.sort_values('Rentrée scolaire').groupby('UAI').tail(1)
        
        return df[['UAI', 'IPS', 'Rentrée scolaire']].rename(columns={
            'IPS': f'IPS_{key}',
            'Rentrée scolaire': f'Annee_{key}'
        })

    def run_analysis(self):
        """Fusionne les 3 périodes sur l'UAI (Inner Join)."""
        df_pre = self._load_and_clean('Pre2022', self.files['pre'])
        df_2022 = self._load_and_clean('2022', self.files['2022'])
        df_post = self._load_and_clean('Post2022', self.files['post'])

        # Fusion en cascade
        self.merged_df = pd.merge(df_pre, df_2022, on='UAI', how='inner')
        self.merged_df = pd.merge(self.merged_df, df_post, on='UAI', how='inner')
        
        print(f"✅ Analyse terminée sur {len(self.merged_df)} établissements communs aux 3 périodes.")

    def visualize_coherence(self):
        """Génère les graphiques de corrélation inter-périodes."""
        if self.merged_df is None: return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # 1. Rupture Méthodologique (Pré-2022 vs 2022)
        corr1 = self.merged_df['IPS_Pre2022'].corr(self.merged_df['IPS_2022'])
        sns.regplot(ax=ax1, data=self.merged_df, x='IPS_Pre2022', y='IPS_2022', 
                    scatter_kws={'alpha':0.2}, line_kws={'color':'red'})
        ax1.plot([50, 160], [50, 160], 'k--', alpha=0.5) # Ligne de stabilité parfaite
        ax1.set_title(f"1. Rupture Méthodologique 2022\nCorrélation : {corr1:.3f}")

        # 2. Stabilité Post-2022 (2022 vs 2024-2025)
        corr2 = self.merged_df['IPS_2022'].corr(self.merged_df['IPS_Post2022'])
        sns.regplot(ax=ax2, data=self.merged_df, x='IPS_2022', y='IPS_Post2022', 
                    scatter_kws={'alpha':0.2}, line_kws={'color':'blue'})
        ax2.plot([50, 160], [50, 160], 'k--', alpha=0.5)
        ax2.set_title(f"2. Stabilité Post-2022 (Nouveau Barème)\nCorrélation : {corr2:.3f}")

        plt.suptitle("Audit de Cohérence Inter-Années (LADIQ)", fontsize=16, fontweight='bold')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig("visualisation/coherence_longitudinale_ips.png")
        print("📊 Graphique sauvegardé : visualisation/coherence_longitudinale_ips.png")

# --- EXÉCUTION DU SCRIPT ---
if __name__ == "__main__":
    config_fichiers = {
        'pre': 'fichierscsv/fr-en-ips_colleges.csv',
        '2022': 'fichierscsv/fr-en-ips-colleges-ap2022.csv',
        'post': 'fichierscsv/fr-en-ips-colleges-ap2023.csv'
    }
    
    auditor = IpsCoherenceAuditor(config_fichiers)
    auditor.run_analysis()
    auditor.visualize_coherence()