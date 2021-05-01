"""Description.

Tests pour la classe Modelisation du module modellisation.
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
    Arrete
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
def probleme_non_valide():
    """Problème ne pouvant pas être résolu."""
    return Probleme(
        personnel = [
            Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf),
            Prerequis(mois = "Mars", nb_employes_min = 1, nb_employes_max = 1)
        ],
        echange = Echange(3, 1/3),
        couts = Couts(160, 200, 200),
        h_supp = 1/4
    )

def test_verification_nb_employes():
    """Le nombre d'employés présents au cours d'un mois doit être positif."""
    with pytest.raises(ValueError):
        Sommet(mois='Février', nb_employes=-6)
        
def test_convertit_str():
    """Teste la fonction qui transforme un objet Sommet en chaine de caractères."""
    entree = Sommet("Mars", 2)
    sortie = entree._convertit_str
    attendu = "Mars - 2"
    assert sortie == attendu
    
def test_par_str():
    """Teste le constructeur alternatif de la classe Sommet."""
    entree = "Avril / 9"
    sortie = Sommet.par_str(entree)
    attendu = Sommet("Avril", 9)
    assert sortie == attendu
    
def test_instanciation(probleme):
    """Création."""
    grapheD = GrapheD(probleme=probleme)
    assert isinstance(grapheD, GrapheD)
    
def test_inputs_graphe(probleme):
    """Teste la fonction qui renvoie les arguments du graphe."""
    grapheD = GrapheD(probleme)
    sortie = grapheD._inputs_graphe
    attendu = (
        "Février - 3",
        "Avril - 2",
        ["Février", "Mars", "Avril"],
        [3, 4, 2],
        [Inf, Inf, 2],
        Echange(ajout_max=1, suppression_max=0.5),
        Couts(changement=90, sur_effectif=100, sous_effectif=300),
        0.25
    ) 
    assert "_inputs_graphe" not in vars(grapheD)
    assert sortie == attendu
    
def test_repr(probleme):
    """Teste le repr."""
    grapheD = GrapheD(probleme = probleme)
    assert (
        repr(grapheD)
        == "GrapheD(depart = Février - 3, arrivee = Avril - 2, mois = ['Février', 'Mars', 'Avril'], min_pers = [3, 4, 2], max_pers = [inf, inf, 2], echange = Echange(ajout_max=1, suppression_max=0.5), couts = Couts(changement=90, sur_effectif=100, sous_effectif=300), h_supp = 0.25)"
    )
    
def test_recupere_indice_mois(probleme):
    """Test."""
    grapheD = GrapheD(probleme = probleme)
    sortie = grapheD._recupere_indice_mois("Mars")
    attendu = 1
    assert sortie == attendu

def test_genere_sommets(probleme):
    """Teste la construction des sommets du graphe."""
    grapheD = GrapheD(probleme = probleme)
    sortie = grapheD._genere_sommets()
    attendu = [
        ['Février - 3'], 
        ['Mars - 2', 'Mars - 3', 'Mars - 4'], 
        ['Avril - 1', 'Avril - 2', 'Avril - 3', 'Avril - 4']
    ]
    assert sortie == attendu

def test_genere_sommets_bis(probleme_non_valide):
    """Test bis."""
    grapheD = GrapheD(probleme_non_valide)
    sortie = grapheD._genere_sommets()
    attendu = [
        ["Février - 3"],
        ["Mars - 2", "Mars - 3"]
    ]
    assert sortie == attendu
    
def test_sommets_relies(probleme):
    """Teste la fonction qui crée les arrêtes."""
    grapheD = GrapheD(probleme = probleme)
    sortie = grapheD._sommets_relies()
    attendu = [
        ('Février - 3', 'Mars - 2', 1),
        ('Février - 3', 'Mars - 3', 1),
        ('Février - 3', 'Mars - 4', 1),
        ('Mars - 2', 'Avril - 1', 1),
        ('Mars - 2', 'Avril - 2', 1),
        ('Mars - 2', 'Avril - 3', 1),
        ('Mars - 3', 'Avril - 2', 1),
        ('Mars - 3', 'Avril - 3', 1),
        ('Mars - 3', 'Avril - 4', 1),
        ('Mars - 4', 'Avril - 2', 1),
        ('Mars - 4', 'Avril - 3', 1),
        ('Mars - 4', 'Avril - 4', 1)
    ]
    assert sortie == attendu
    
def test_sommets_relies_bis(probleme_non_valide):
    """Test bis."""
    grapheD = GrapheD(probleme = probleme_non_valide)
    sortie = grapheD._sommets_relies()
    attendu = [
        ('Février - 3', 'Mars - 2', 1),
        ('Février - 3', 'Mars - 3', 1)
    ]
    assert sortie == attendu
    
def test_calcule_couts(probleme):
    """Teste le calcul du poids associé à une arrête."""
    grapheD = GrapheD(probleme = probleme)
    arrete = ('Mars - 4', 'Avril - 3', 1)
    sortie = grapheD._calcule_couts(arrete)
    attendu = ('Mars - 4', 'Avril - 3', 190)
    assert sortie == attendu
    
def test_construit_graphe(probleme):
    """Teste la construction du graphe associé au problème."""
    grapheD = GrapheD(probleme = probleme)
    sortie = grapheD.construit_graphe()
    attendu = [
        ('Février - 3', 'Mars - 2', 540),
        ('Février - 3', 'Mars - 3', 75),
        ('Février - 3', 'Mars - 4', 90),
        ('Mars - 2', 'Avril - 1', 315),
        ('Mars - 2', 'Avril - 2', 0),
        ('Mars - 2', 'Avril - 3', 190),
        ('Mars - 3', 'Avril - 2', 90),
        ('Mars - 3', 'Avril - 3', 100),
        ('Mars - 3', 'Avril - 4', 190),
        ('Mars - 4', 'Avril - 2', 180),
        ('Mars - 4', 'Avril - 3', 190),
        ('Mars - 4', 'Avril - 4', 100)
    ] 
    assert sortie == attendu

def test_construit_graphe_bis(probleme_non_valide):
    """Test bis."""
    grapheD = GrapheD(probleme = probleme_non_valide)
    sortie = grapheD.construit_graphe()
    attendu = [
        ('Février - 3', 'Mars - 2', 360),
        ('Février - 3', 'Mars - 3', 200)
    ] 
    assert sortie == attendu
        
def test_contient_arrivee(probleme):
    """Teste si le graphe contient l'état d'arrivée."""
    grapheD = GrapheD(probleme = probleme)
    sortie = grapheD.contient_arrivee()
    attendu = True
    assert sortie == attendu
    
def test_sans_arrivee(probleme_non_valide):
    """Vérifie le bon fonctionnement de contient_arrivee."""
    sortie = GrapheD(probleme_non_valide).contient_arrivee()
    attendu = False
    assert sortie == attendu

