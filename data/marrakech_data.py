# Données spécifiques à Marrakech
OBJECTIVE_DEFAULT = "1x + 1y + 1z"  # Maximiser F = x + y + z (tonnes traitées par jour)
CONSTRAINTS_DEFAULT = [
    "500x + 800y + 600z <= 1500000",  # Budget quotidien (DH)
    "1x + 0y + 0z <= 800",          # Capacité de recyclage (tonnes/jour)
    "0x + 1y + 0z <= 600",          # Capacité d'incinération (tonnes/jour)
    "0x + 0y + 1z <= 400",          # Capacité de compostage (tonnes/jour)
    "1x + 1y + 1z <= 1644"          # Total des déchets produits par jour
]