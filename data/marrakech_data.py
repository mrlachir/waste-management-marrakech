# Données spécifiques à Marrakech
OBJECTIVE_DEFAULT = "1x + 1y"  # Maximiser Z = x + y (tonnes traitées par jour)
CONSTRAINTS_DEFAULT = [
    "500x + 800y <= 1500000",  # Budget quotidien (DH)
    "1x + 0y <= 800",         # Capacité de recyclage (tonnes/jour)
    "0x + 1y <= 600",         # Capacité d'incinération (tonnes/jour)
    "1x + 1y <= 1644"         # Total des déchets produits par jour
]