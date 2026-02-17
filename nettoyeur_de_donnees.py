import pandas as pd

class LadiqCleaner :
    def __init__(self, file_path, separator = ';') :
        # On garde ton encodage utf-8-sig
        self.df = pd.read_csv(file_path, sep=separator, encoding='utf-8-sig', low_memory=False)
        self.initial_shape = self.df.shape
        self.quality_scores = {}

    def measure_completeness(self):
        """METRIQUE LADIQ : Taux de remplissage."""
        completeness = self.df.notnull().mean() * 100
        self.quality_scores['completeness'] = completeness.mean()
        return completeness

    def clean_duplicates(self) :
        """METRIQUE LADIQ : Unicité."""
        before = self.df.shape[0]
        self.df.drop_duplicates(inplace=True)
        after = self.df.shape[0]
        self.quality_scores['duplicates_removed'] = before - after

    def handle_missing_values(self, strategy='drop') :
        """Nettoyage des lignes vides."""
        if strategy == 'drop' :
            self.df.dropna(subset=['Score moyen', 'UAI'], inplace=True)
        return "Nettoyage effectué."

    def check_consistency(self, col_name, min_val=0, max_val=500):
        """METRIQUE LADIQ : Cohérence."""
        if col_name in self.df.columns:
            # On s'assure que la colonne est bien numérique
            self.df[col_name] = pd.to_numeric(self.df[col_name], errors='coerce')
            before = self.df.shape[0]
            self.df = self.df[(self.df[col_name] >= min_val) & (self.df[col_name] <= max_val)]
            after = self.df.shape[0]
            self.quality_scores['incoherent_rows_removed'] = before - after

    def merge_with_ips(self, ips_file_path):
        """
        FONCTION CRUCIALE : Fusionne les notes avec l'Indice Social.
        C'est ici qu'on valide la qualité de l'identifiant UAI.
        """
        df_ips = pd.read_csv(ips_file_path, sep=';', encoding='utf-8-sig')
        # On ne garde que les colonnes utiles dans le fichier IPS
        df_ips = df_ips[['UAI', 'IPS']]
        
        # Fusion sur la colonne 'UAI'
        self.df = pd.merge(self.df, df_ips, on='UAI', how='left')
        
        # On calcule combien de collèges ont bien été trouvés
        match_rate = self.df['IPS'].notnull().mean() * 100
        print(f"✅ Fusion IPS terminée. Taux de correspondance : {match_rate:.2f}%")

    def get_report(self):
        print(f"\n--- RAPPORT LADIQ ---")
        print(f"Taille initiale : {self.initial_shape}")
        print(f"Taille actuelle : {self.df.shape}")
        print(f"Doublons supprimés : {self.quality_scores.get('duplicates_removed', 0)}")
        print(f"Complétude moyenne : {self.quality_scores.get('completeness', 0):.2f}%")
        print(f"---------------------\n")

# --- EXECUTION ---

# 1. Chargement et premier nettoyage
cleaner = LadiqCleaner("fichierscsv/fr-en-evaluations_nationales_6eme_par_etablissement.csv")
cleaner.measure_completeness()
cleaner.clean_duplicates()
cleaner.check_consistency('Score moyen')
cleaner.handle_missing_values()

# 2. Ajout de la dimension sociale (IPS)
cleaner.merge_with_ips("fichierscsv/fr-en-ips-colleges-ap2023.csv")

# 3. Rapport final
cleaner.get_report()

# 4. Calcul de l'indicateur final (Corrélation)
# On convertit l'IPS en nombre (parfois il y a des virgules)
cleaner.df['IPS'] = pd.to_numeric(cleaner.df['IPS'], errors='coerce')

# On calcule la corrélation entre IPS et Score moyen
correlation = cleaner.df['IPS'].corr(cleaner.df['Score moyen'])

print(f"INDICATEUR PRONTO : Corrélation entre IPS et Résultats : {correlation:.2f}")
if correlation > 0.6:
    print("Analyse : Les données montrent un fort lien entre milieu social et réussite scolaire.")