import pandas as pd
import re
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime

# 1. CONFIGURATION DU "CERVEAU" (Logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 🧠 RAISONNEMENT | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("LADIQ_AI")

class LadiqSmartAuditor:
    """
    Auditeur LADIQ Intelligent.
    Il audite, nettoie en temps réel, évalue la qualité, ET génère un nouveau fichier certifié.
    """

    def __init__(self, file_path: str, separator: str = ';', volatilite_annees: int = 5):
        self.file_path = Path(file_path)
        self.volatilite = volatilite_annees
        self.quality_report = {}
        
        try:
            self.df = pd.read_csv(self.file_path, sep=separator, encoding='utf-8-sig', low_memory=False)
            self.initial_rows = len(self.df)
            self.initial_cols = len(self.df.columns)
            logger.info(f"Fichier '{self.file_path.name}' chargé. ({self.initial_rows} lignes, {self.initial_cols} colonnes)")
        except Exception as e:
            logger.error(f"Échec critique du chargement : {e}")
            raise

        self.scores = {'C': 0.0, 'A': 0.0, 'L': 0.0, 'Act': 0.0, 'I': 0.0}
        self.metrics = {
            'total_cellules': self.df.size,
            'valeurs_presentes': 0,
            'lignes_syntaxe_ko': 0,
            'lignes_coherence_ko': 0,
            'annee_moyenne': datetime.now().year,
            'cols_documentees': 0
        }

    # --- MÉTHODES D'AUDIT ET DE NETTOYAGE EN MÉMOIRE ---
    
    def auditer_completude(self):
        logger.info("--- Phase 1 : Audit de la Complétude ---")
        nb_vides = self.df.isnull().sum().sum()
        self.metrics['valeurs_presentes'] = self.metrics['total_cellules'] - nb_vides
        self.scores['C'] = self.metrics['valeurs_presentes'] / self.metrics['total_cellules']

    def auditer_exactitude(self, col_id: str, regex_pattern: str):
        logger.info("--- Phase 2 : Audit de l'Exactitude (Syntaxe) ---")
        if col_id not in self.df.columns: return
        avant = len(self.df)
        self.df = self.df[self.df[col_id].astype(str).str.match(regex_pattern, na=False)]
        apres = len(self.df)
        self.metrics['lignes_syntaxe_ko'] = avant - apres
        self.scores['A'] = apres / self.initial_rows

    def auditer_coherence(self, col_cible: str, min_val: float, max_val: float):
        logger.info("--- Phase 3 : Audit de la Cohérence (Logique Métier) ---")
        if col_cible not in self.df.columns: return
        clean_col = self.df[col_cible].astype(str).str.replace(',', '.').str.replace('%', '')
        vals_numeriques = pd.to_numeric(clean_col, errors='coerce')
        
        hors_bornes = vals_numeriques[(vals_numeriques < min_val) | (vals_numeriques > max_val)]
        self.metrics['lignes_coherence_ko'] = len(hors_bornes)
        
        self.df[col_cible] = vals_numeriques 
        self.df = self.df[(self.df[col_cible] >= min_val) & (self.df[col_cible] <= max_val)]
        
        nb_testes = len(vals_numeriques)
        self.scores['L'] = 1 - (len(hors_bornes) / nb_testes) if nb_testes > 0 else 0

    def auditer_actualite(self, col_date: str):
        logger.info("--- Phase 4 : Audit de l'Actualité (Temporel) ---")
        if col_date not in self.df.columns: return
        annees = self.df[col_date].astype(str).str.extract(r'(\d{4})')[0]
        annees = pd.to_numeric(annees, errors='coerce').dropna()
        if annees.empty: return
        
        self.metrics['annee_moyenne'] = annees.mean()
        age_moyen = datetime.now().year - self.metrics['annee_moyenne']
        self.scores['Act'] = max(0, 1 - (age_moyen / self.volatilite))

    def auditer_intelligibilite(self, mapping_cols: Dict[str, str]):
        logger.info("--- Phase 5 : Audit de l'Intelligibilité (Documentation) ---")
        self.df.rename(columns=mapping_cols, inplace=True)
        self.metrics['cols_documentees'] = len(mapping_cols)
        self.scores['I'] = self.metrics['cols_documentees'] / self.initial_cols

    # --- NOUVELLE MÉTHODE : GÉNÉRATION DU FICHIER NETTOYÉ ---
    
    def exporter_donnees_propres(self, dossier_sortie: str = "donnees_certifiees"):
        """
        Génère un nouveau fichier CSV contenant uniquement les données validées par l'audit LADIQ.
        """
        logger.info("--- Phase Finale : Exportation des données ---")
        
        # 1. Création du dossier s'il n'existe pas
        out_dir = Path(dossier_sortie)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Nommage professionnel (On rajoute "CLEANED_" devant le nom du fichier)
        fichier_sortie = out_dir / f"CLEANED_{self.file_path.name}"
        
        # 3. Écriture du fichier sur le disque
        self.df.to_csv(fichier_sortie, sep=';', index=False, encoding='utf-8-sig')
        
        logger.info(f"💾 SUCCÈS : Nouveau fichier généré -> {fichier_sortie}")
        return fichier_sortie

    # --- GÉNÉRATION DU RAPPORT RAISONNÉ ---
    def generer_rapport_raisonne(self):
        score_global = sum(self.scores.values()) / 5
        print(f"\n{'='*60}")
        print(f"🧐 RAPPORT D'AUDIT IA : {self.file_path.name}")
        print(f"NOTE GLOBALE : {score_global:.2%}")
        print(f"{'='*60}\n")
        return self.df

# =============================================================================
# EXÉCUTION DU SCÉNARIO
# =============================================================================
if __name__ == "__main__":
    
    # --- CAS 1 : IPS ---
    auditeur_ips = LadiqSmartAuditor("fichierscsv/fr-en-ips-colleges-ap2023.csv", volatilite_annees=5)
    
    auditeur_ips.auditer_intelligibilite({"UAI": "Code_Etablissement", "IPS": "Indice_Position_Sociale", "Rentrée scolaire": "Annee_Reference"})
    auditeur_ips.auditer_actualite("Annee_Reference")
    auditeur_ips.auditer_exactitude("Code_Etablissement", r"^\d{7}[A-Z]$")
    auditeur_ips.auditer_coherence("Indice_Position_Sociale", 45, 185)
    auditeur_ips.auditer_completude()
    
    auditeur_ips.generer_rapport_raisonne()
    
    # 💾 ICI ON CRÉE LE NOUVEAU FICHIER !
    fichier_ips_propre = auditeur_ips.exporter_donnees_propres("fichiers_certifies")


    # --- CAS 2 : DNB ---
    auditeur_dnb = LadiqSmartAuditor("fichierscsv/fr-en-dnb-par-etablissement.csv", volatilite_annees=2)
    
    auditeur_dnb.auditer_intelligibilite({"Numero d'etablissement": "Code_Etablissement", "Taux de réussite": "Taux_Reussite", "Session": "Annee_Examen"})
    auditeur_dnb.auditer_actualite("Annee_Examen")
    auditeur_dnb.auditer_exactitude("Code_Etablissement", r"^\d{7}[A-Z]$")
    auditeur_dnb.auditer_coherence("Taux_Reussite", 0, 100)
    auditeur_dnb.auditer_completude()
    
    auditeur_dnb.generer_rapport_raisonne()
    
    # 💾 ICI ON CRÉE LE NOUVEAU FICHIER !
    fichier_dnb_propre = auditeur_dnb.exporter_donnees_propres("fichiers_certifies")