import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def plot_solution(solution, A, b, canvas, fig):
    x, y, z = solution
    fig.clf()
    
    # Set modern style for the plot
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Create 3D subplot with a modern look
    ax = fig.add_subplot(111, projection='3d', facecolor='#f8f9fa')
    
    # Ajuster la taille de la figure pour plus de clarté
    fig.set_size_inches(10, 6)  # Augmenter la taille (largeur, hauteur)
    
    # Définir les limites des axes avec une marge plus large
    x_max = max(800, x + 100)  # Marge de 100 tonnes
    y_max = max(600, y + 100)  # Marge de 100 tonnes
    z_max = max(400, z + 100)  # Marge de 100 tonnes
    
    # Modern color palette
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#E91E63', '#3F51B5']
    
    # Create a meshgrid for 3D plotting
    X = np.linspace(0, x_max, 20)
    Y = np.linspace(0, y_max, 20)
    X, Y = np.meshgrid(X, Y)
    
    # Plot each constraint as a 3D plane
    for i, (coeffs, limit) in enumerate(zip(A, b)):
        color = colors[i % len(colors)]
        
        # Calculate Z values from the constraint equation: ax + by + cz = d
        # If coefficient of z is 0, we need to handle it differently
        if coeffs[2] != 0:
            Z = (limit - coeffs[0] * X - coeffs[1] * Y) / coeffs[2]
            # Clip negative values (not feasible)
            Z = np.maximum(Z, 0)
            # Plot the surface
            surf = ax.plot_surface(X, Y, Z, alpha=0.3, color=color, label=f"Contrainte {i+1}")
            surf._facecolors2d = surf._facecolor3d
            surf._edgecolors2d = surf._edgecolor3d
        else:
            # If z coefficient is 0, we have a vertical plane
            if coeffs[1] != 0:
                # Calculate Y from X (when Z can be any value)
                Y_plane = (limit - coeffs[0] * X) / coeffs[1]
                Z_plane = np.zeros_like(X) + z_max/2  # Plot at middle of z-axis
                ax.plot_surface(X, Y_plane, Z_plane, alpha=0.3, color=color)
            elif coeffs[0] != 0:
                # Calculate X from Y (when Z can be any value)
                X_plane = (limit - coeffs[1] * Y) / coeffs[0]
                Z_plane = np.zeros_like(X) + z_max/2  # Plot at middle of z-axis
                ax.plot_surface(X_plane, Y, Z_plane, alpha=0.3, color=color)
    
    # Ajouter la solution optimale with a more prominent marker
    ax.scatter([x], [y], [z], marker='o', s=100, color='#E91E63', 
               edgecolor='white', linewidth=2, label="Solution optimale")
    
    # Add annotation for the optimal solution
    ax.text(x, y, z, f'({x:.1f}, {y:.1f}, {z:.1f})', 
            color='#212121', fontsize=10, fontweight='bold')
    
    # Définir les limites et ajouter des marges
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_zlim(0, z_max)
    
    # Améliorer la lisibilité with modern styling
    ax.set_xlabel("Recyclage (x, tonnes)", fontsize=10, fontweight='bold', color='#424242')
    ax.set_ylabel("Incinération (y, tonnes)", fontsize=10, fontweight='bold', color='#424242')
    ax.set_zlabel("Compostage (z, tonnes)", fontsize=10, fontweight='bold', color='#424242')
    ax.set_title("Optimisation des déchets à Marrakech", fontsize=14, fontweight='bold', color='#212121', pad=15)
    
    # Add a custom legend
    legend_elements = []
    for i in range(len(A)):
        color = colors[i % len(colors)]
        legend_elements.append(plt.Line2D([0], [0], color=color, lw=4, label=f"Contrainte {i+1}"))
    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#E91E63', 
                                     markersize=10, label="Solution optimale"))
    
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1), 
              fontsize=9, frameon=True, framealpha=0.9)
    
    # Improve grid appearance
    ax.grid(True, linestyle='--', alpha=0.4, color='#9e9e9e')
    
    # Style the ticks
    ax.tick_params(colors='#616161', labelsize=9)
    
    # Add a subtle background color to the entire figure
    fig.patch.set_facecolor('#f8f9fa')
    
    # Set a good viewing angle
    ax.view_init(elev=30, azim=45)
    
    # Ajuster l'agencement pour éviter les chevauchements
    plt.tight_layout()
    
    # Mettre à jour le canvas
    canvas.draw()