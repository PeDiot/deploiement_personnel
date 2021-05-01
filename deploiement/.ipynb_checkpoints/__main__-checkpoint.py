"""Description.

Démonstration du module.
"""

from .modelisation import (
    GrapheD,
    Sommet,
    Arrete
)
from .probleme import (
    Mois,
    Employes,
    Inf,
    Cout,
    Couts,
    Prerequis,
    Echange,
    Probleme
)
from .resolution import Resolution

personnel_str = """
Février / 3 / Inf
Mars / 4 / Inf
Avril / 7 / Inf
 Mai / 7 / Inf
Juin / 5 / 5
"""
echange_str = """
3 / .33
"""
couts_str = """
160 / 200 / 200
"""
h_supp_str = """
.25
"""

mon_probleme = Probleme.par_str(
    personnel_str, 
    echange_str,
    couts_str,
    h_supp_str
)
mon_probleme.affiche()

solution = Resolution(GrapheD(mon_probleme))
solution.affiche()
solution.genere_graphique()