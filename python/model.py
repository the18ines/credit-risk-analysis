import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

y_true = dataset['Risk_Class'].astype(int)
y_pred = dataset['Risque_Prédit'].astype(int)

classes = sorted(y_true.unique().tolist())
noms = {0: 'Faible', 1: 'Modéré', 2: 'Élevé'}
labels = [noms[c] for c in classes]

cm = confusion_matrix(y_true, y_pred, labels=classes)

fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='RdYlGn',
            xticklabels=labels, yticklabels=labels,
            linewidths=0.5, linecolor='white', ax=ax, vmin=0)
ax.set_xlabel('Prédit', fontsize=11, fontweight='bold')
ax.set_ylabel('Réel', fontsize=11, fontweight='bold')
ax.set_title('Matrice de Confusion — Random Forest', 
             fontsize=12, fontweight='bold', pad=10)
plt.tight_layout()
plt.show()  