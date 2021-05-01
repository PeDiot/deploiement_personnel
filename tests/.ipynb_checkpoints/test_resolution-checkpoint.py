"""Description.

Teste la classe de résolution du problème de déploiement.
"""

import coverage
import pytest
from deploiement import (
    Mois,
    Employes,
    Inf,
    Cout,
    Couts,
    Prerequis,
    Echange,
    Probleme,
    GrapheD,
    Sommet,
    Arrete,
    Resolution
)


@pytest.fixture
def probleme():
    """Problème utilisé pour les tests."""
    return Probleme(
        personnel = [
            Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf),
            Prerequis(mois = "Mars", nb_employes_min = 4, nb_employes_max = Inf),
            Prerequis(mois = "Avril", nb_employes_min = 2, nb_employes_max = 2)
        ],
        echange = Echange(1, 1/2),
        couts = Couts(90, 100, 300),
        h_supp = 1/4
    )

@pytest.fixture
def probleme_sans_solution():
    """Retranscription du problème d'exemple en graphe."""
    return Probleme(
        personnel = [
            Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf),
            Prerequis(mois = "Mars", nb_employes_min = 7, nb_employes_max = 7)
        ],
        echange = Echange(3, 1/3),
        couts = Couts(160, 200, 200),
        h_supp = 1/4
    )

def test_instanciation(probleme):
    """Création."""
    solution = Resolution(GrapheD(probleme))
    assert isinstance(solution, Resolution)
    
def test_trouve_chemin(probleme):
    """Teste le solveur."""
    solution = Resolution(GrapheD(probleme))
    sortie = solution._trouve_chemin()
    attendu = ['Février - 3', 'Mars - 3', 'Avril - 2']
    assert sortie == attendu
    
def test_couts_optimaux(probleme):
    """Test."""
    solution = Resolution(GrapheD(probleme))
    sortie = solution._couts_optimaux()
    attendu = (
        [0, 75.0, 90],
        [0, 75.0, 165.0]
    )
    assert sortie == attendu
    
def test_bilan(probleme):
    """Test."""
    solution = Resolution(GrapheD(probleme))
    sortie = solution._bilan()
    attendu = [
        ('Février - 3', 0, 0),
        ('Mars - 3', 75.0, 75.0),
        ('Avril - 2', 90, 165.0)
    ]
    
def test_est_resolvable(probleme, probleme_sans_solution):
    """Teste la fonction qui détermine si un problème a une solution."""
    solution = Resolution(GrapheD(probleme))
    sans_solution = Resolution(GrapheD(probleme_sans_solution))
    assert solution._est_resolvable() == True
    assert sans_solution._est_resolvable() == False
