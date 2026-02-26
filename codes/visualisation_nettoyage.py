import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Configuration du style visuel (Optionnel mais plus pro) ---
plt.style.use('seaborn-v0_8-whitegrid')

def comparer_fichiers_ladiq():
    """Charge les fichiers bruts et certifiés pour générer des preuves visuelles."""
    print("Chargement des fichiers pour la comparaison visuelle...")
    
    # Lecture des fichiers
    dnb_raw = pd.read_csv("fichierscsv/fr-en-dnb-par-etablissement.csv", sep=";", low_memory=False)
    dnb_clean = pd.read_csv("fichiers_certifies/CLEANED_fr-en-dnb-par-etablissement.csv", sep=";", low_memory=False)

    ips_raw = pd.read_csv("fichierscsv/fr-en-ips-colleges-ap2023.csv", sep=";", low_memory=False)
    ips_clean = pd.read_csv("fichiers_certifies/CLEANED_fr-en-ips-colleges-ap2023.csv", sep=";", low_memory=False)

    # ==========================================================
    # VISUALISATION 1 : LE COMPTEUR DE LIGNES (Exactitude & Cohérence)
    # ==========================================================
    fig1, axs1 = plt.subplots(1, 2, figsize=(12, 5))
    
    # Barres DNB
    axs1[0].bar(['Brut (Sale)', 'Certifié (Propre)'], [len(dnb_raw), len(dnb_clean)], color=['#e74c3c', '#2ecc71'])
    axs1[0].set_title('Impact du filtre sur le DNB', fontsize=12)
    axs1[0].set_ylabel('Nombre de Lignes')
    # Ajout du texte sur les barres
    for i, val in enumerate([len(dnb_raw), len(dnb_clean)]):
        axs1[0].text(i, val + 2000, f"{val:,}", ha='center', fontweight='bold')

    # Barres IPS
    axs1[1].bar(['Brut (Sale)', 'Certifié (Propre)'], [len(ips_raw), len(ips_clean)], color=['#e74c3c', '#2ecc71'])
    axs1[1].set_title("Impact du filtre sur l'IPS", fontsize=12)
    axs1[1].set_ylabel('Nombre de Lignes')
    for i, val in enumerate([len(ips_raw), len(ips_clean)]):
        axs1[1].text(i, val + 200, f"{val:,}", ha='center', fontweight='bold')

    fig1.suptitle("Preuve 1 : Suppression des anomalies et doublons", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("preuve1_volume_lignes.png", dpi=150)
    print("✅ Graphique 1 généré : preuve1_volume_lignes.png")

    # ==========================================================
    # VISUALISATION 2 : LA DISTRIBUTION (La magie du Typage)
    # ==========================================================
    # On va montrer que le Taux de Réussite DNB est maintenant "calculable"
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    # Dans le fichier propre, c'est devenu un vrai nombre mathématique (float) !
    sns.histplot(data=dnb_clean, x='Taux_Reussite', bins=40, color='#3498db', kde=True, ax=ax2)
    
    ax2.set_title("Preuve 2 : Distribution Mathématique du Taux de Réussite (Fichier Certifié)", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Taux de Réussite au Brevet (%)", fontsize=12)
    ax2.set_ylabel("Nombre de Collèges", fontsize=12)
    
    # On ajoute une ligne verticale pour la moyenne
    moyenne = dnb_clean['Taux_Reussite'].mean()
    ax2.axvline(moyenne, color='#e74c3c', linestyle='--', linewidth=2, label=f'Moyenne : {moyenne:.1f}%')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig("preuve2_distribution_maths.png", dpi=150)
    print("✅ Graphique 2 généré : preuve2_distribution_maths.png")

# --- Lancement du script ---
if __name__ == "__main__":
    comparer_fichiers_ladiq()