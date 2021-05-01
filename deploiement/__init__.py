"""Description du module deploiement.

Exemple :

    >>> from deploiement import *
    >>> personnel_str = '''
    ... Février / 3 / Inf
    ... Mars / 4 / Inf
    ... Avril / 7 / Inf
    ...  Mai / 7 / Inf
    ... Juin / 5 / 5
    ... '''
    >>> echange_str = '''
    ... 3 / .33
    ... '''
    >>> couts_str = '''
    ... 160 / 200 / 200
    ... '''
    >>> h_supp_str = '''
    ... .25
    ... '''
    >>> mon_probleme = Probleme.par_str(
    ...     personnel_str,
    ...     echange_str,
    ...     couts_str,
    ...     h_supp_str
    ... )
    >>> mon_probleme.affiche()
    ┌─────────┬───────────────────────────┐
    │ Mois    │ Nombre d'employés minimal │
    ├─────────┼───────────────────────────┤
    │ Février │ 3                         │
    │ Mars    │ 4                         │
    │ Avril   │ 7                         │
    │ Mai     │ 7                         │
    │ Juin    │ 5                         │
    └─────────┴───────────────────────────┘
    ┌──────────────────────┐
    │ Coûts                │
    ├──────────────────────┤
    │ Changement : 160€    │
    │ Sous-effectif : 200€ │
    │ Sur-effectif : 200€  │
    └──────────────────────┘
    ┌─────────────────────────────────────────┐
    │ Contraintes                             │
    ├─────────────────────────────────────────┤
    │ Ajout maximal d'employés : 3            │
    │ Suppression maximale d'employés : 33.0% │
    │ 25.0% d'heures supplémentaires          │
    └─────────────────────────────────────────┘
    >>> solution = Resolution(GrapheD(mon_probleme))
    >>> solution.affiche()
    ┌─────────┬───────────────────┬──────────────┬───────────────┐
    │ Mois    │ Nombre d'employés │ Coût mensuel │ Coûts cumulés │
    ├─────────┼───────────────────┼──────────────┼───────────────┤
    │ Février │ 3                 │ 0€           │ 0€            │
    │ Mars    │ 4                 │ 160€         │ 160€          │
    │ Avril   │ 5                 │ 310.0€       │ 470.0€        │
    │ Mai     │ 5                 │ 150.0€       │ 620.0€        │
    │ Juin    │ 5                 │ 0€           │ 620.0€        │
    └─────────┴───────────────────┴──────────────┴───────────────┘
    >>> solution.genere_graphique()
    
    La commande python -m deploiement permettra d'afficher un exemple.
"""

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
from .modelisation import (
    GrapheD,
    Sommet,
    Arrete
)
from .resolution import Resolution

__all__ = [
    "Mois",
    "Employes",
    "Inf",
    "Cout",
    "Couts",
    "Prerequis",
    "Echange",
    "Probleme",
    "GrapheD",
    "Sommet",
    "Arrete",
    "Resolution"
]