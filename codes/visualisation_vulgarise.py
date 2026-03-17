import matplotlib.pyplot as plt
import os

# Données du modèle (importances issues de audit_ips_ale.py / audit_ips_xgboost.py)
# À mettre à jour avec les valeurs réelles affichées par le modèle
labels = ['IPS (Social)', 'Taille (Élèves)', 'Secteur (Public/Privé)']
values = [88, 10, 2]  # ex : valeurs issues de model.feature_importances_
colors = ['#3498db', '#95a5a6', '#e74c3c']

plt.figure(figsize=(8, 4))
plt.barh(labels, values, color=colors)
plt.title("Qui décide de la note au Brevet ?\n(Importance des facteurs selon l'IA)", fontsize=12)
plt.xlabel("Influence sur la prédiction (%)")
plt.xlim(0, 100)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
os.makedirs("visualisation", exist_ok=True)
plt.savefig("visualisation/importance_variables_vulgarise.png", dpi=150)
print("💾 Graphique sauvegardé : visualisation/importance_variables_vulgarise.png")
plt.show()