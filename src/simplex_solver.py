import numpy as np
import pandas as pd

def parse_constraint(constraint_str):
    try:
        left, right = constraint_str.split("<=")
        # Split by + and handle each term
        terms = [term.strip() for term in left.split("+")]
        coeffs = [0, 0, 0]  # Initialize with 3 variables (x, y, z)
        
        for term in terms:
            if 'x' in term:
                coeffs[0] = float(term.replace("x", "").strip() or 1)
            elif 'y' in term:
                coeffs[1] = float(term.replace("y", "").strip() or 1)
            elif 'z' in term:
                coeffs[2] = float(term.replace("z", "").strip() or 1)
        
        limit = float(right.strip())
        return coeffs, limit
    except ValueError:
        raise ValueError("Format invalide. Utilisez par ex. '500x + 800y + 600z <= 1500000'")

def simplex_manual(c, A, b):
    n_vars = len(c)
    n_constraints = len(b)
    tableau = np.zeros((n_constraints + 1, n_vars + n_constraints + 2))  # Z, vars, slack, b
    
    tableau[0, 1:n_vars + 1] = [-coeff for coeff in c]
    tableau[0, 0] = 1
    
    for i in range(n_constraints):
        tableau[i + 1, 1:n_vars + 1] = A[i]
        tableau[i + 1, n_vars + 1 + i] = 1
        tableau[i + 1, -1] = b[i]
    
    tableaux = [tableau.copy()]
    
    while np.any(tableau[0, 1:-1] < 0):
        pivot_col = np.argmin(tableau[0, 1:-1]) + 1
        ratios = [tableau[i, -1] / tableau[i, pivot_col] if tableau[i, pivot_col] > 0 else np.inf for i in range(1, tableau.shape[0])]
        if all(r == np.inf for r in ratios):
            return None, None, "Problème non borné"
        pivot_row = np.argmin(ratios) + 1
        
        pivot_value = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_value
        
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                factor = tableau[i, pivot_col]
                tableau[i, :] -= factor * tableau[pivot_row, :]
        
        tableaux.append(tableau.copy())
    
    solution = np.zeros(n_vars)
    for j in range(n_vars):
        col = tableau[:, j + 1]
        if np.sum(col != 0) == 1 and col[0] == 0:
            row = np.where(col != 0)[0][0]
            solution[j] = tableau[row, -1]
    
    z = tableau[0, -1]
    return solution, z, tableaux