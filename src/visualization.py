import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def plot_solution(solution, A, b, canvas, fig):
    # Déterminer le nombre de variables non nulles dans la solution
    non_zero_vars = sum(1 for val in solution if val > 0.001)
    x, y, z = solution
    fig.clf()
    
    # Set modern style for the plot
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Choisir entre visualisation 2D ou 3D en fonction du nombre de variables non nulles
    if non_zero_vars <= 2:
        # Créer un subplot 2D avec un look moderne
        ax = fig.add_subplot(111, facecolor='#f8f9fa')
    else:
        # Show message for 3 variables
        ax = fig.add_subplot(111, facecolor='#f8f9fa')
        ax.text(0.5, 0.5, '3D visualization not available\nPlease use 2 variables for visualization', 
               horizontalalignment='center', verticalalignment='center', 
               fontsize=12, color='#212121', transform=ax.transAxes)
        return
    
    # Ajuster la taille de la figure pour plus de clarté et assurer la visibilité dans le conteneur scrollable
    fig.set_size_inches(10, 6)  # Taille optimale pour la visualisation
    fig.tight_layout(pad=2.5)  # Améliorer l'espacement pour éviter les chevauchements
    
    # Modern color palette
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#E91E63', '#3F51B5']
    
    if non_zero_vars <= 2:
        # Visualisation 2D pour 2 variables ou moins
        # Déterminer quelles variables sont non nulles
        active_vars = []
        if x > 0.001:
            active_vars.append(0)  # x est actif
        if y > 0.001:
            active_vars.append(1)  # y est actif
        if z > 0.001:
            active_vars.append(2)  # z est actif
            
        # Si une seule variable est active, on ajoute une deuxième pour la visualisation
        if len(active_vars) == 1:
            if active_vars[0] != 0:
                active_vars.insert(0, 0)  # Ajouter x comme deuxième variable
            else:
                active_vars.append(1)  # Ajouter y comme deuxième variable
        
        # Extraire les deux variables actives
        var1_idx, var2_idx = active_vars[0], active_vars[1]
        var_names = ["Recyclage (x)", "Incinération (y)", "Compostage (z)"]
        var_values = [x, y, z]
        
        # Définir les limites des axes avec une marge plus large
        var1_max = max(800, var_values[var1_idx] + 100)  # Marge de 100 tonnes
        var2_max = max(600, var_values[var2_idx] + 100)  # Marge de 100 tonnes
        
        # Créer un espace de points pour le tracé
        var1_range = np.linspace(0, var1_max, 100)
        
        # Tracer chaque contrainte comme une ligne
        for i, (coeffs, limit) in enumerate(zip(A, b)):
            color = colors[i % len(colors)]
            
            # Calculer var2 en fonction de var1 à partir de l'équation de contrainte
            if coeffs[var2_idx] != 0:
                var2_values = (limit - coeffs[var1_idx] * var1_range) / coeffs[var2_idx]
                # Filtrer les valeurs négatives (non réalisables)
                valid_indices = var2_values >= 0
                ax.plot(var1_range[valid_indices], var2_values[valid_indices], 
                         color=color, linewidth=2, label=f"Contrainte {i+1}")
        
        # Ajouter la solution optimale avec un marqueur plus visible
        ax.scatter([var_values[var1_idx]], [var_values[var2_idx]], marker='o', s=100, 
                   color='#E91E63', edgecolor='white', linewidth=2, label="Solution optimale")
        
        # Ajouter une annotation pour la solution optimale
        ax.text(var_values[var1_idx], var_values[var2_idx], 
                f'({var_values[var1_idx]:.1f}, {var_values[var2_idx]:.1f})', 
                color='#212121', fontsize=10, fontweight='bold')
        
        # Définir les limites et ajouter des marges
        ax.set_xlim(0, var1_max)
        ax.set_ylim(0, var2_max)
        
        # Améliorer la lisibilité avec un style moderne
        ax.set_xlabel(f"{var_names[var1_idx]}, tonnes", fontsize=10, fontweight='bold', color='#424242')
        ax.set_ylabel(f"{var_names[var2_idx]}, tonnes", fontsize=10, fontweight='bold', color='#424242')
        ax.set_title("Optimisation des déchets à Marrakech (2D)", fontsize=14, fontweight='bold', color='#212121', pad=15)
        
        # Ajouter une légende personnalisée
        legend_elements = []
        for i in range(len(A)):
            color = colors[i % len(colors)]
            legend_elements.append(plt.Line2D([0], [0], color=color, lw=2, label=f"Contrainte {i+1}"))
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#E91E63', 
                                         markersize=10, label="Solution optimale"))
    else:
        # Visualisation 3D pour 3 variables
        # Définir les limites des axes avec une marge plus large
        x_max = max(800, x + 100)  # Marge de 100 tonnes
        y_max = max(600, y + 100)  # Marge de 100 tonnes
        z_max = max(400, z + 100)  # Marge de 100 tonnes
        
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
        ax.set_title("Optimisation des déchets à Marrakech (3D)", fontsize=14, fontweight='bold', color='#212121', pad=15)
        
        # Set a good viewing angle for 3D
        ax.view_init(elev=30, azim=45)
        
        # Add a custom legend
        legend_elements = []
        for i in range(len(A)):
            color = colors[i % len(colors)]
            legend_elements.append(plt.Line2D([0], [0], color=color, lw=4, label=f"Contrainte {i+1}"))
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#E91E63', 
                                         markersize=10, label="Solution optimale"))
    
    # Ajouter la légende
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1), 
              fontsize=9, frameon=True, framealpha=0.9)
    
    # Improve grid appearance
    ax.grid(True, linestyle='--', alpha=0.4, color='#9e9e9e')
    
    # Style the ticks
    ax.tick_params(colors='#616161', labelsize=9)
    
    # Add a subtle background color to the entire figure
    fig.patch.set_facecolor('#f8f9fa')
    
    # Ajuster l'agencement pour éviter les chevauchements et assurer une bonne visibilité
    plt.tight_layout(pad=2.0)
    
    # Mettre à jour le canvas et s'assurer que le graphique est visible
    canvas.draw()
    canvas.flush_events()