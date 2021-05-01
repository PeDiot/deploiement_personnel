"""Description.

Tests pour la classe Probleme du module probleme.
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
    Probleme
)

@pytest.fixture
def personnel():
    """5 prérequis pour les tests suivants."""
    fevrier = Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf)
    mars = Prerequis(mois = "Mars", nb_employes_min = 4, nb_employes_max = Inf)
    avril = Prerequis(mois = "Avril", nb_employes_min = 7, nb_employes_max = Inf)
    mai = Prerequis(mois = "Mai", nb_employes_min = 7, nb_employes_max = Inf)
    juin = Prerequis(mois = "Juin", nb_employes_min = 5, nb_employes_max = 5)
    return [fevrier, mars, avril, mai, juin]

@pytest.fixture
def echange():
    """Contraintes sur les échanges d'employés."""
    return Echange(3, .33)

@pytest.fixture
def couts():
    """Coûts utilisés dans les tests."""
    return Couts(160, 200, 200)

@pytest.fixture
def h_supp():
    return .25

def test_verification_nb_employes_min():
    """Le nombre d'employés minimal doit être positif."""
    with pytest.raises(ValueError):
        Prerequis(mois = "Janvier", nb_employes_min = -5, nb_employes_max = 10)
              
def test_verification_nb_employes_max():
    """Le nombre d'employés maximal doit être positif."""
    with pytest.raises(ValueError):
        Prerequis(mois = "Mars", nb_employes_min = 5, nb_employes_max = -1)
        
def test_verification_ajout_max():
    """Vérifie qu'un ajout d'employés doit être positif."""
    with pytest.raises(ValueError):
        Echange(-2, 1/2)
        
def test_verification_suppression_max():
    """Vérifie qu'on ne peut pas enlever tout le personnel présent."""
    with pytest.raises(ValueError):
        Echange(2, 5/4)

def test_couts():
    """Vérifie qu'un cout doit être positif."""
    with pytest.raises(ValueError):
            Couts(-30, 100, 40)
            with pytest.raises(ValueError):
                Couts(30, -100, 40)
                with pytest.raises(ValueError):
                    Couts(30, 100, -40)
        
def test_instanciation(personnel, echange, couts, h_supp):
    """Création."""
    probleme = Probleme(personnel, echange, couts, h_supp)
    assert isinstance(probleme, Probleme)
    assert probleme._personnel == {prerequis.mois: prerequis for prerequis in personnel}
    
def test_egalite(personnel, echange, couts, h_supp):
    """Doit être différent de l'identité."""
    probleme1 = Probleme(personnel, echange, couts, h_supp)
    probleme2 = Probleme(personnel, echange, couts, h_supp)
    assert probleme1 == probleme2

def test_validation_doublon(personnel, echange, couts, h_supp):
    """Vérifie la détection de deux prérequis associés au même mois."""
    a, b, c, d, e = personnel
    f = Prerequis(mois = "Mars", nb_employes_min = 2, nb_employes_max = 8)
    with pytest.raises(ValueError):
        Probleme(
            [a, b, c, d, e, f],
            echange,
            couts, 
            h_supp
        )    
    
def test_personnel(personnel, echange, couts, h_supp):
    """Teste la propriété personnel.
    La propriété personnel ne doit pas faire partie des attributs de la classe Probleme."""
    probleme = Probleme(personnel, echange, couts, h_supp)
    assert "personnel" not in vars(probleme)
    assert personnel == list(probleme.personnel)

def test_mois(personnel, echange, couts, h_supp):
    """Teste la propriété mois. 
    La propriété mois ne doit pas faire partie des attributs de la classe Probleme."""
    probleme = Probleme(personnel, echange, couts, h_supp)
    assert "mois" not in vars(probleme)
    assert ("Février Mars Avril Mai Juin").split() == list(probleme.mois)

def test_getitem(personnel, echange, couts, h_supp):
    """Utilisation de []."""
    probleme = Probleme(personnel, echange, couts, h_supp)
    assert probleme["Février"] == personnel[0]

def test_repr():
    """Teste le repr."""
    probleme = Probleme(
        personnel = [
            Prerequis(mois = "Mars", nb_employes_min = 2, nb_employes_max = Inf),
            Prerequis(mois = "Avril", nb_employes_min = 4, nb_employes_max = 4)
        ],
        echange = Echange(3, .33),
        couts = Couts(160, 200, 200),
        h_supp = 1/4
    )
    assert (
        repr(probleme)
        == "Probleme(personnel = [Prerequis(mois='Mars', nb_employes_min=2, nb_employes_max=inf), Prerequis(mois='Avril', nb_employes_min=4, nb_employes_max=4)], echange = Echange(ajout_max=3, suppression_max=0.33), couts = Couts(changement=160, sur_effectif=200, sous_effectif=200), h_supp = 0.25)"
    )

def test_encode_prerequis():
    """Teste l'encodage d'une ligne en un objet de classe Prerequis."""
    correspondance = {
        "Février / 1 / 6": Prerequis(mois = "Février", nb_employes_min = 1, nb_employes_max = 6),
        "Mars / 2 / 9": Prerequis(mois = "Mars", nb_employes_min = 2, nb_employes_max = 9)
    }
    for entree, attendu in correspondance.items():
        assert attendu == Probleme._encode_prerequis(entree)
        
def test_encode_echange():
    """Teste l'encodage d'une ligne en un objet de classe Echange."""
    correspondance = {
        "3 / .33" : Echange(ajout_max = 3, suppression_max = .33),
        "2 / .25" : Echange(ajout_max = 2, suppression_max = .25)
    }
    for entree, attendu in correspondance.items():
        assert attendu == Probleme._encode_echange(entree)
        
def test_encode_couts():
    """Teste l'encodage d'une ligne en objet de classe Couts."""
    correspondance = {
        "100 / 200 / 40" : Couts(changement=100, sur_effectif=200, sous_effectif=40),
        "10 / 2000 / 400" : Couts(changement=10, sur_effectif=2000, sous_effectif=400)
    }
    for entree, attendu in correspondance.items():
        assert attendu == Probleme._encode_couts(entree)


def test_constructeur(personnel, echange, couts, h_supp):
    """Constructeur alternatif."""
    personnel_str = """
    Février / 3 /
    Mars / 4 /
    Avril / 7 /
    Mai / 7 /
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
    probleme = Probleme.par_str(personnel_str, echange_str, couts_str, h_supp_str)
    assert probleme == Probleme(personnel, echange, couts, h_supp)
    
def test_probleme_encodage():
    """Test."""
    personnel_str_1 = """
    Février / 3 /
    Mars / 4 /
    
    Avril / 7 / 7
    """
    personnel_str_2 = """
    Février / 3 /
    Mars / 4 /
    Avril / 7 / 8
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
    with pytest.raises(ValueError):
        Probleme.par_str(personnel_str_1, echange_str, couts_str, h_supp_str)
    with pytest.raises(ValueError):
        Probleme.par_str(personnel_str_2, echange_str, couts_str, h_supp_str)