import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import ttk, messagebox
from data.marrakech_data import OBJECTIVE_DEFAULT, CONSTRAINTS_DEFAULT
from src.simplex_solver import parse_constraint, simplex_manual
from src.visualization import plot_solution
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

# Interface Tkinter
root = tk.Tk()
root.title("Optimisation des déchets - Marrakech")
root.geometry("1000x800")  # Augmenter la taille de la fenêtre

# Frame pour l'entrée des données
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Fonction objectif
ttk.Label(input_frame, text="Fonction objectif (ex: 1x + 1y):").pack()
objective_entry = ttk.Entry(input_frame, width=40)
objective_entry.insert(0, OBJECTIVE_DEFAULT)
objective_entry.pack(pady=5)

# Contraintes
ttk.Label(input_frame, text="Contraintes (ex: 500x + 800y <= 1500000):").pack()
constraints_frame = ttk.Frame(input_frame)
constraints_frame.pack(pady=5)
constraint_entries = []
for default in CONSTRAINTS_DEFAULT:
    entry = ttk.Entry(constraints_frame, width=40)
    entry.insert(0, default)
    entry.pack(pady=2)
    constraint_entries.append(entry)

# Fonction pour ajouter une contrainte
def add_constraint():
    entry = ttk.Entry(constraints_frame, width=40)
    entry.pack(pady=2)
    constraint_entries.append(entry)

# Fonction pour calculer et afficher les résultats
def calculate():
    objective = objective_entry.get()
    constraints = [entry.get() for entry in constraint_entries]
    
    try:
        obj_coeffs = [float(x.strip().replace("x", "").replace("y", "")) for x in objective.split("+")]
        c = obj_coeffs
        
        A = []
        b = []
        for constraint in constraints:
            coeffs, limit = parse_constraint(constraint)
            A.append(coeffs)
            b.append(limit)
        
        solution, z, tableaux = simplex_manual(c, A, b)
        
        if solution is None:
            messagebox.showerror("Erreur", "Problème non borné ou insoluble.")
            return
        
        x, y = solution
        
        # Afficher les tableaux
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Optimisation des déchets à Marrakech\n\n")
        result_text.insert(tk.END, f"Solution optimale : x = {x:.2f} tonnes (recyclage), y = {y:.2f} tonnes (incinération)\n")
        result_text.insert(tk.END, f"Total traité (Z) = {z:.2f} tonnes\n\n")
        
        var_names = ["Z", "x", "y"] + [f"s{i+1}" for i in range(len(b))] + ["b"]
        for idx, tab in enumerate(tableaux):
            df = pd.DataFrame(tab, columns=var_names)
            result_text.insert(tk.END, f"Tableau {idx}:\n{df.to_string(index=False)}\n\n")
        
        # Forcer la mise à jour du graphique
        plot_solution(solution, A, b, canvas, fig)
        canvas.get_tk_widget().pack_forget()  # Supprimer l'ancien canvas
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  # Réafficher
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

# Boutons
ttk.Button(input_frame, text="Ajouter une contrainte", command=add_constraint).pack(pady=5)
ttk.Button(input_frame, text="Calculer", command=calculate).pack(pady=10)

# Frame pour les résultats
result_frame = ttk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True)

# Zone de texte pour les tableaux
result_text = tk.Text(result_frame, height=20, width=80)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Graphique
fig = plt.Figure(figsize=(10, 6), dpi=100)  # Augmenter la taille de la figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Lancer l'application
root.mainloop()