import numpy as np
import matplotlib.pyplot as plt

def plot_solution(solution, A, b, canvas, fig):
    x, y = solution
    fig.clf()
    ax = fig.add_subplot(111)
    
    # Ajuster la taille de la figure pour plus de clarté
    fig.set_size_inches(10, 6)  # Augmenter la taille (largeur, hauteur)
    
    # Définir les limites des axes avec une marge plus large
    x_max = max(1644, x + 200)  # Marge de 200 tonnes
    y_max = max(800, y + 200)   # Marge de 200 tonnes
    x_vals = np.linspace(0, x_max, 400)
    
    # Tracer les contraintes
    for i, (coeffs, limit) in enumerate(zip(A, b)):
        if coeffs[1] != 0:
            y_vals = (limit - coeffs[0] * x_vals) / coeffs[1]
            ax.plot(x_vals, y_vals, label=f"Contrainte {i+1}")
        else:
            ax.axvline(limit / coeffs[0], label=f"Contrainte {i+1}")
    
    # Remplir la région réalisable
    ax.fill_between(x_vals, 0, np.min([limit for _, limit in zip(A, b)]), 
                    where=(x_vals <= x_max), alpha=0.3, label="Région réalisable")
    
    # Ajouter la solution optimale
    ax.plot(x, y, "ro", label="Solution optimale", markersize=10)
    
    # Définir les limites et ajouter des marges
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.margins(x=0.15, y=0.15)  # 15% de marge sur les axes
    
    # Améliorer la lisibilité
    ax.set_xlabel("Recyclage (x, tonnes)", fontsize=12)
    ax.set_ylabel("Incinération (y, tonnes)", fontsize=12)
    ax.set_title("Optimisation des déchets à Marrakech", fontsize=14, pad=15)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=10)  # Légende à droite
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Ajuster l'agencement pour éviter les chevauchements
    plt.tight_layout()
    
    # Mettre à jour le canvas
    canvas.draw()