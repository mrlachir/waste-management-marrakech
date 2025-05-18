import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import ttk, messagebox, font
from data.marrakech_data import OBJECTIVE_DEFAULT, CONSTRAINTS_DEFAULT
from src.simplex_solver import parse_constraint, simplex_manual
from src.visualization import plot_solution
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
# PIL import removed as it's not currently needed
# from PIL import Image, ImageTk

# Interface Tkinter with modern styling
root = tk.Tk()
root.title("Optimisation des déchets - Marrakech")
root.geometry("1200x900")  # Larger window for better layout
root.configure(bg="#f5f5f5")  # Light gray background

# Custom fonts
heading_font = font.Font(family="Segoe UI", size=14, weight="bold")
subheading_font = font.Font(family="Segoe UI", size=12)
normal_font = font.Font(family="Segoe UI", size=10)

# Custom style for widgets
style = ttk.Style()
style.theme_use('clam')  # Use clam as base theme

# Configure colors
style.configure('TFrame', background='#f5f5f5')
style.configure('TLabel', background='#f5f5f5', font=normal_font)
style.configure('TButton', font=normal_font, background='#4CAF50', foreground='black')
style.configure('TEntry', font=normal_font)
style.map('TButton',
    background=[('active', '#45a049'), ('pressed', '#3d8b40')],
    foreground=[('pressed', 'white'), ('active', 'white')])

# Custom styles for specific widgets
style.configure('Header.TLabel', font=heading_font, background='#f5f5f5')
style.configure('Subheader.TLabel', font=subheading_font, background='#f5f5f5')
style.configure('Primary.TButton', background='#4CAF50', foreground='white')
style.configure('Secondary.TButton', background='#f0f0f0')
style.configure('Card.TFrame', background='#ffffff', relief='solid', borderwidth=1)

# Main container with padding
main_container = ttk.Frame(root, padding="20 20 20 20")
main_container.pack(fill=tk.BOTH, expand=True)

# Title section
title_frame = ttk.Frame(main_container)
title_frame.pack(fill=tk.X, pady=(0, 20))
ttk.Label(title_frame, text="Optimisation de la Gestion des Déchets", style='Header.TLabel').pack()
ttk.Label(title_frame, text="Ville de Marrakech", style='Subheader.TLabel').pack()

# Two-column layout
content_frame = ttk.Frame(main_container)
content_frame.pack(fill=tk.BOTH, expand=True)

# Left column - Input controls
input_frame = ttk.Frame(content_frame, padding="10 10 10 10")
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

# Input section with card-like appearance
input_card = ttk.Frame(input_frame, padding="15 15 15 15")
input_card.pack(fill=tk.X, pady=(0, 15))
input_card.configure(style='Card.TFrame')

# Fonction objectif with better styling
ttk.Label(input_card, text="Fonction objectif", style='Subheader.TLabel').pack(anchor=tk.W)
ttk.Label(input_card, text="Format: 1x + 1y + 1z (maximiser)", font=("Segoe UI", 9, "italic")).pack(anchor=tk.W, pady=(0, 5))

objective_entry = ttk.Entry(input_card, width=40, font=normal_font)
objective_entry.insert(0, OBJECTIVE_DEFAULT)
objective_entry.pack(fill=tk.X, pady=(0, 10))

# Constraints section with card-like appearance
constraints_card = ttk.Frame(input_frame, padding="15 15 15 15")
constraints_card.pack(fill=tk.X)

ttk.Label(constraints_card, text="Contraintes", style='Subheader.TLabel').pack(anchor=tk.W)
ttk.Label(constraints_card, text="Format: 500x + 800y + 600z <= 1500000", font=("Segoe UI", 9, "italic")).pack(anchor=tk.W, pady=(0, 10))

constraints_frame = ttk.Frame(constraints_card)
constraints_frame.pack(fill=tk.X, pady=5)

constraint_entries = []
for i, default in enumerate(CONSTRAINTS_DEFAULT):
    constraint_row = ttk.Frame(constraints_frame)
    constraint_row.pack(fill=tk.X, pady=3)
    
    # Add a small label indicating the constraint number
    ttk.Label(constraint_row, text=f"#{i+1}", width=3, font=normal_font).pack(side=tk.LEFT, padx=(0, 5))
    
    entry = ttk.Entry(constraint_row, width=40, font=normal_font)
    entry.insert(0, default)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    constraint_entries.append(entry)

# Fonction pour ajouter une contrainte
def add_constraint():
    i = len(constraint_entries)
    constraint_row = ttk.Frame(constraints_frame)
    constraint_row.pack(fill=tk.X, pady=3)
    
    # Add a small label indicating the constraint number
    ttk.Label(constraint_row, text=f"#{i+1}", width=3, font=normal_font).pack(side=tk.LEFT, padx=(0, 5))
    
    entry = ttk.Entry(constraint_row, width=40, font=normal_font)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    constraint_entries.append(entry)

# Fonction pour calculer et afficher les résultats
def calculate():
    objective = objective_entry.get()
    constraints = [entry.get() for entry in constraint_entries]
    
    try:
        # Show a loading message
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Calcul en cours...\n")
        root.update()
        
        # Parse objective function for 3 variables
        terms = [term.strip() for term in objective.split('+')]
        c = [0, 0, 0]  # Initialize coefficients for x, y, z
        
        for term in terms:
            if 'x' in term:
                c[0] = float(term.replace("x", "").strip() or 1)
            elif 'y' in term:
                c[1] = float(term.replace("y", "").strip() or 1)
            elif 'z' in term:
                c[2] = float(term.replace("z", "").strip() or 1)
        
        A = []
        b = []
        for constraint in constraints:
            coeffs, limit = parse_constraint(constraint)
            A.append(coeffs)
            b.append(limit)
        
        solution, objective_value, tableaux = simplex_manual(c, A, b)
        
        if solution is None:
            messagebox.showerror("Erreur", "Problème non borné ou insoluble.")
            return
        
        x, y, z = solution
        
        # Afficher les résultats avec un meilleur formatage
        result_text.delete(1.0, tk.END)
        
        # Titre et résultats principaux avec mise en forme
        result_text.insert(tk.END, "RÉSULTATS DE L'OPTIMISATION\n", "title")
        result_text.insert(tk.END, "\n")
        
        result_text.insert(tk.END, "Solution optimale:\n", "subtitle")
        result_text.insert(tk.END, f"• Recyclage (x): {x:.2f} tonnes\n", "result")
        result_text.insert(tk.END, f"• Incinération (y): {y:.2f} tonnes\n", "result")
        result_text.insert(tk.END, f"• Compostage (z): {z:.2f} tonnes\n", "result")
        result_text.insert(tk.END, f"• Total traité (F): {objective_value:.2f} tonnes\n\n", "result_highlight")
        
        # Configurer les styles de texte
        result_text.tag_configure("title", font=("Segoe UI", 12, "bold"), foreground="#212121")
        result_text.tag_configure("subtitle", font=("Segoe UI", 11, "bold"), foreground="#424242")
        result_text.tag_configure("result", font=("Segoe UI", 10), foreground="#212121")
        result_text.tag_configure("result_highlight", font=("Segoe UI", 10, "bold"), foreground="#4CAF50")
        
        # Ajouter les tableaux avec un formatage amélioré
        result_text.insert(tk.END, "Tableaux de résolution:\n", "subtitle")
        
        var_names = ["F", "x", "y", "z"] + [f"s{i+1}" for i in range(len(b))] + ["b"]
        for idx, tab in enumerate(tableaux):
            df = pd.DataFrame(tab, columns=var_names)
            result_text.insert(tk.END, f"Tableau {idx+1}:\n", "table_title")
            result_text.insert(tk.END, f"{df.to_string(index=False)}\n\n", "table_content")
        
        result_text.tag_configure("table_title", font=("Segoe UI", 10, "italic"), foreground="#616161")
        result_text.tag_configure("table_content", font=("Consolas", 9))
        
        # Mettre à jour le graphique
        plot_solution(solution, A, b, canvas, fig)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

# Buttons with improved styling
buttons_frame = ttk.Frame(input_frame)
buttons_frame.pack(fill=tk.X, pady=15)

ttk.Button(buttons_frame, text="+ Ajouter une contrainte", command=add_constraint, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
ttk.Button(buttons_frame, text="Calculer la solution optimale", command=calculate, style='Primary.TButton').pack(side=tk.LEFT)

# Right column - Results and visualization
results_frame = ttk.Frame(content_frame, padding="10 10 10 10")
results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Results section with card-like appearance
results_card = ttk.Frame(results_frame, padding="15 15 15 15")
results_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

ttk.Label(results_card, text="Résultats de l'optimisation", style='Subheader.TLabel').pack(anchor=tk.W, pady=(0, 10))

# Zone de texte pour les tableaux avec meilleur style
result_text = tk.Text(results_card, height=15, width=80, font=("Consolas", 10), bg="#ffffff", relief="flat")
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
result_text.configure(padx=10, pady=10)

scrollbar = ttk.Scrollbar(results_card, orient="vertical", command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Visualization section with card-like appearance
visualization_card = ttk.Frame(results_frame, padding="15 15 15 15")
visualization_card.pack(fill=tk.BOTH, expand=True)

ttk.Label(visualization_card, text="Visualisation graphique", style='Subheader.TLabel').pack(anchor=tk.W, pady=(0, 10))

# Graphique avec meilleur style
fig = plt.Figure(figsize=(10, 6), dpi=100, facecolor='#ffffff')
canvas = FigureCanvasTkAgg(fig, master=visualization_card)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Lancer l'application
root.mainloop()