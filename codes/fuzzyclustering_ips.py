import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import pandas as pd
from scipy.interpolate import make_interp_spline

# ==========================================
# 1. GÉNÉRATION DES DONNÉES SIMULÉES
# ==========================================
# Nous simulons un jeu de données réaliste basé sur les tendances du graphique original.
# IPS de 60 à 160, Note de 5 à 18.
np.random.seed(42)  # Pour la reproductibilité
n_samples = 500
ips_simulated = np.random.uniform(60, 160, n_samples)
# La note suit une tendance linéaire avec du bruit
note_simulated = 4 + 0.065 * ips_simulated + np.random.normal(0, 1.2, n_samples)
note_simulated = np.clip(note_simulated, 0, 20)  # On reste entre 0 et 20

# Préparation des données pour scikit-fuzzy (transposées)
data = np.vstack((ips_simulated, note_simulated))

# ==========================================
# 2. APPLICATION DU FUZZY C-MEANS (FCM)
# ==========================================
# Nous définissons 5 clusters comme dans l'original (Très Déf., Déf., Moyen, Fav., Très Fav.)
n_clusters = 5
# Paramètre de flou 'm' (fuzziness coefficient). Typiquement entre 1.2 et 2.0.
# Plus 'm' est élevé, plus les clusters se chevauchent (sont 'flous').
m = 1.7

# Application de FCM
# cntr : Centres des clusters (centroïdes)
# u : Matrice d'appartenance (Membership matrix) -> C'est ICI que réside le 'Fuzzy'
cntr, u, u0, d, jm, p, fpc = fuzz.cmeans(
    data, n_clusters, m, error=0.005, maxiter=1000, init=None
)

# ==========================================
# 3. PRÉPARATION DE LA VISUALISATION VULGARISÉE
# ==========================================

# Définition des couleurs (approximativement celles de ton graphique original)
colors = ['#E57373', '#FFAB91', '#FFD54F', '#81D4FA', '#4FC3F7'] # Rouge, Orange, Jaune, Bleu clair, Bleu vif
# Pour correspondre aux catégories, on trie les clusters par IPS croissant
sorted_indices = np.argsort(cntr[:, 0])
cntr = cntr[sorted_indices]
u = u[sorted_indices]

# Titre et labels vulgarisés
title = "LE LADIQ INNOVE : Visualisation 'Floue' (Fuzzy) de la mixité sociale au Brevet"
ylabel = "Note Moyenne à l'écrit (sur 20)"
xlabel = "Indice de Position Sociale (IPS) du collège"
category_labels = ['Très Défavorisé', 'Défavorisé', 'Moyen / Mixte', 'Favorisé', 'Très Favorisé']

# Création de la figure
plt.figure(figsize=(14, 8), dpi=100)
ax = plt.gca()

# --- PARTIE A : Affichage des données brutes (points floutés) ---
# Nous affichons tous les points, mais leur opacité (alpha) dépend de leur appartenance principale.
# Cela montre la densité tout en suggérant le flou.
for j in range(n_samples):
    # Trouver le cluster d'appartenance maximale pour ce point
    cluster_membership = u[:, j]
    max_membership_idx = np.argmax(cluster_membership)
    max_membership_val = cluster_membership[max_membership_idx]
    
    # Afficher le point avec l'opacité liée à son appartenance max
    # (plus il est 'pur' dans un cluster, plus il est opaque)
    ax.scatter(data[0, j], data[1, j], 
               color=colors[max_membership_idx], 
               alpha=max_membership_val * 0.6, # On réduit l'opacité globale
               s=15, linewidths=0)

# --- PARTIE B : Modélisation des distributions floues (Courbes) ---
# Nous n'affichons plus des barres rigides, mais des courbes de probabilité de distribution.
# Pour simplifier, nous ajustons des courbes de distribution gaussienne sur l'appartenance (u).

# Générer un axe IPS lisse pour les courbes
ips_smooth = np.linspace(60, 160, 200)

for i in range(n_clusters):
    # Pour chaque cluster, nous interpolons la distribution des appartenances 'u'
    # afin de créer une courbe lisse qui représente la 'zone d'influence' du cluster.
    
    # Nous utilisons une approche de lissage par Spline sur les données d'appartenance
    # pour obtenir une courbe d'allure naturelle.
    
    # 1. Calculer une distribution de densité pondérée par l'appartenance FCM
    weights = u[i, :]
    # Créer une estimation de densité (KDE) pour visualiser la forme
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(data[0, :], weights=weights)
    curve_y = kde(ips_smooth)
    
    # Normaliser la courbe pour qu'elle soit visible à une échelle de note 0-20
    # C'est une représentation visuelle du *degré d'appartenance*, pas une note.
    # On la scale arbitrairement pour la visualisation superposée.
    curve_y_scaled = (curve_y / np.max(curve_y)) * 19 # Max proche de 20
    
    # Remplir la zone sous la courbe (chevauchement flou)
    ax.fill_between(ips_smooth, 0, curve_y_scaled, color=colors[i], alpha=0.3)
    
    # Afficher la ligne de la courbe
    ax.plot(ips_smooth, curve_y_scaled, color=colors[i], linestyle='-', linewidth=2.5, label=category_labels[i])
    
    # Afficher le Centroïde (Note moyenne du cluster idéal)
    # C'est l'équivalent des barres d'origine, mais ici c'est un point central 'flou'
    ax.scatter(cntr[i, 0], cntr[i, 1], color=colors[i], s=150, edgecolors='black', zorder=10)
    ax.text(cntr[i, 0], cntr[i, 1] + 0.5, f"{cntr[i, 1]:.1f}/20", 
            ha='center', fontweight='bold', fontsize=12, color='black',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))

# --- PARTIE C : Éléments fixes de mise en page ---
# Moyenne nationale estimée (comme sur l'original)
moyenne_nationale = 12.0
ax.axhline(moyenne_nationale, color='gray', linestyle='--', linewidth=1.5, label='Moyenne nationale estimée')

# Paramètres des axes
ax.set_xlim(60, 160)
ax.set_ylim(0, 21)
ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

# Grille d'arrière-plan simplifiée
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Légende vulgarisée
leg = ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
leg.get_frame().set_edgecolor('black')

# Affichage
plt.tight_layout()
plt.show()

# ==========================================
# 4. JUSTIFICATION POUR L'ALE (TEXTE)
# ==========================================
print("\n--- JUSTIFICATION DE L'APPROCHE FUZZY POUR TON ALE ---")
print("1. PROBLÈME DE L'ORIGINAL : Ton premier graphique classait un IPS de 99 et un IPS de 81")
print("   dans la même catégorie 'Défavorisé'. C'est brutal et peu précis.")
print("2. SOLUTION FUZZY (FCM) : Le code ci-dessus utilise FCM. Cela signifie")
print("   qu'un collège N'APPARTIENT PAS à un seul cluster. Il appartient à TOUS")
print("   les clusters avec des degrés différents (ex: 80% Moyen, 20% Favorisé).")
print("3. VISUALISATION : Nous avons remplacé les barres rigides par des COURBES.")
print("   Les zones où les courbes se chevauchent (couleurs mélangées) montrent")
print("   la mixité sociale réelle et les transitions fluides.")
print("   C'est ça la 'précision' que demandait ta tutrice : la prise en compte du dégradé.")