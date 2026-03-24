import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generate_vulgarized_chart(df):
    df = df.copy()

    # 1. On crée nos tranches d'IPS (bins)
    bins = [0, 80, 100, 120, 140, 200]
    labels = ['Très Défavorisé\n(<80)', 'Défavorisé\n(80-100)', 'Moyen / Mixte\n(100-120)', 
              'Favorisé\n(120-140)', 'Très Favorisé\n(>140)']
    colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db']

    # 2. On groupe les données par ces tranches
    df['Zone_IPS'] = pd.cut(df['IPS'], bins=bins, labels=labels)
    stats_zone = df.groupby('Zone_IPS')['Note_Ecrit'].mean()

    # 3. Création du graphique
    plt.figure(figsize=(12, 7))
    bars = plt.bar(stats_zone.index, stats_zone.values, color=colors, edgecolor='black', alpha=0.8)

    # 4. Personnalisation esthétique
    plt.title("Le 'Thermomètre' de la réussite au Brevet selon l'IPS", fontsize=16, fontweight='bold', pad=20)
    plt.ylabel("Note moyenne à l'écrit (sur 20)", fontsize=12)
    plt.ylim(0, 20)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajout des valeurs au-dessus des barres
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{height:.1f}/20', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Ajout d'une ligne pour la moyenne nationale (exemple à 12/20)
    plt.axhline(y=12, color='grey', linestyle='--', label='Moyenne nationale estimée')
    plt.legend()

    plt.tight_layout()
    plt.savefig("visualisation/thermometre_ips_reussite.png", dpi=150)
    print("💾 Graphique de vulgarisation sauvegardé : visualisation/thermometre_ips_reussite.png")
    plt.show()

# Pour l'utiliser, ajoute simplement cette ligne à la fin de ton script :
# generate_vulgarized_chart(auditor.df)