"""Description.

Modélisation du déploiement de personnel.
"""

from typing import List, Tuple, Generator, Any, Union
from math import floor
from dataclasses import dataclass
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


@dataclass
class Sommet:
    """Représente un mois et le nb d'employés associé.
    
    Exemple :
    
    >>> sommet = Sommet("Février", 6)
    >>> sommet
    Sommet(mois='Février', nb_employes=6)
    >>> sommet._convertit_str
    'Février - 6'
    >>> Sommet.par_str("Février / 6")
    Sommet(mois='Février', nb_employes=6)
    """
    
    mois: Mois
    nb_employes: Employes
    
    def __post_init__(self):
        """Vérifie que le nombre d'employés est positif."""
        if int(self.nb_employes) < 0:
            raise ValueError("Le nombre d'employés doit être positif.")  
    
    @property
    def _convertit_str(self) -> str:
        """Convertit un objet de type Sommet en chaine de caractères."""
        return self.mois + " - " + str(self.nb_employes)
    
    @classmethod
    def par_str(cls, message: str) -> "Sommet":
        """Constructeur alternatif."""
        mois = message.split()[0]
        nb_employes = int(message.split()[2])
        return cls(mois, nb_employes)

Arrete = Tuple[Sommet, Sommet, Union[int, float]]
    
class GrapheD:
    """Classe permettant la construction du graphe associé au problème de déploiement.
    
    Exemple:
    
    >>> probleme = Probleme(
    ...     personnel = [
    ...         Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf),
    ...         Prerequis(mois = "Mars", nb_employes_min = 4, nb_employes_max = Inf),
    ...         Prerequis(mois = "Avril", nb_employes_min = 7, nb_employes_max = Inf),
    ...         Prerequis(mois = "Mai", nb_employes_min = 7, nb_employes_max = Inf),
    ...         Prerequis(mois = "Juin", nb_employes_min = 5, nb_employes_max = 5)
    ...     ],
    ...     echange = Echange(3, 1/3),
    ...     couts = Couts(160, 200, 200),
    ...     h_supp = 1/4
    ... )
    
    >>> grapheD = GrapheD(probleme = probleme)
    
    >>> grapheD._inputs_graphe
    ('Février - 3', 'Juin - 5', ['Février', 'Mars', 'Avril', 'Mai', 'Juin'], [3, 4, 7, 7, 5], [inf, inf
    , inf, inf, 5], Echange(ajout_max=3, suppression_max=0.3333333333333333), Couts(changement=160, sur
    _effectif=200, sous_effectif=200), 0.25)
    
    >>> grapheD
    GrapheD(depart = Février - 3, arrivee = Juin - 5, mois = ['Février', 'Mars', 'Avril', 'Mai'
    , 'Juin'], min_pers = [3, 4, 7, 7, 5], max_pers = [inf, inf, inf, inf, 5], echange = Echang
    e(ajout_max=3, suppression_max=0.3333333333333333), couts = Couts(changement=160, sur_effec
    tif=200, sous_effectif=200), h_supp = 0.25)
    
    >>> print(grapheD)
    Départ : 'Février - 3'
    Arrivée : 'Juin - 5'
    Mois : ['Février', 'Mars', 'Avril', 'Mai', 'Juin']
    Personnel minimum [3, 4, 7, 7, 5]
    Personnel maximum : [inf, inf, inf, inf, 5]
    Echange personnel : Echange(ajout_max=3, suppression_max=0.3333333333333333)
    Coûts : Couts(changement=160, sur_effectif=200, sous_effectif=200)
    Heures supplémentaires maximum : 0.25
    
    >>> grapheD._genere_sommets()
    [
        ['Février - 3'], 
        ['Mars - 2', 'Mars - 3', 'Mars - 4', 'Mars - 5', 'Mars - 6'], 
        ['Avril - 2', 'Avril - 3', 'Avril - 4', 'Avril - 5', 'Avril - 6', 'Avril - 7'], 
        ['Mai - 2', 'Mai - 3', 'Mai - 4', 'Mai - 5', 'Mai - 6', 'Mai - 7'], 
        ['Juin - 2', 'Juin - 3', 'Juin - 4', 'Juin - 5', 'Juin - 6', 'Juin - 7']
    ]    
    
    >>> grapheD._sommets_relies()
    [
        ('Février - 3', 'Mars - 2', 1), 
        ('Février - 3', 'Mars - 3', 1),
        ...,
        ('Mai - 7', 'Juin - 6', 1), 
        ('Mai - 7', 'Juin - 7', 1)
    ]
    
    >>> grapheD._calcule_couts(('Mai - 7', 'Juin - 6', 1))
    ('Mai - 7', 'Juin - 6', 360)
    
    >>> grapheD.construit_graphe()
    [
        ('Février - 3', 'Mars - 2', 460.0), 
        ('Février - 3', 'Mars - 3', 50.0),
        ...,
        ('Mars - 4', 'Avril - 7', 480), 
        ('Mars - 5', 'Avril - 4', 560.0), 
        ...,
        ('Mai - 7', 'Juin - 6', 360),
        ('Mai - 7', 'Juin - 7', 200)
    ] 
    
    >>> grapheD.contient_arrivee()
    True
    >>>
    
    >>> probleme = Probleme(
    ...     personnel = [
    ...         Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf),
    ...         Prerequis(mois = "Mars", nb_employes_min = 1, nb_employes_max = 1)
    ... ],
    ...  echange = Echange(3, .33),
    ...     couts = Couts(160, 200, 200),
    ...     h_supp = 1/4
    ... )
    
    >>> sans_arrivee = GrapheD(probleme)
    >>> sans_arrivee.contient_arrivee()
    False

    """
    
    def __init__(self, probleme: Probleme):
        """Initialisation à partir d'un objet de classe Probleme."""
        self._probleme = probleme
    
    @property
    def _inputs_graphe(self):
        """Renvoie les éléments nécessaires pour la construction du graphe."""
        depart = self._probleme.mois[0] + " - " + str(self._probleme[self._probleme.mois[0]].nb_employes_min)
        arrivee = self._probleme.mois[-1] + " - " + str(self._probleme[self._probleme.mois[-1]].nb_employes_max)
        mois = [mois for mois in self._probleme.mois]
        min_pers = [
            prerequis.nb_employes_min for prerequis in self._probleme.personnel
        ]
        max_pers = [
            prerequis.nb_employes_max for prerequis in self._probleme.personnel
        ]
        echange = self._probleme._echange
        couts = self._probleme._couts
        h_supp = self._probleme._h_supp
        return (
            depart, 
            arrivee,
            mois, 
            min_pers,
            max_pers,
            echange, 
            couts, 
            h_supp
        ) 
    
    def __repr__(self) -> str:
        """Affichage."""
        depart, arrivee, mois, min_pers, max_pers, echange, couts, h_supp = self._inputs_graphe
        return f"GrapheD(depart = {depart}, arrivee = {arrivee}, mois = {mois}, min_pers = {min_pers}, max_pers = {max_pers}, echange = {echange}, couts = {couts}, h_supp = {h_supp})"
    
    def __str__(self) -> str:
        """Affiche le graphe initial lisiblement."""
        depart, arrivee, mois, min_pers, max_pers, echange, couts, h_supp = self._inputs_graphe
        return f"Départ : " + repr(depart) + "\nArrivée : " + repr(arrivee) + "\nMois : " + repr(mois) + "\nPersonnel minimum " + repr(min_pers) + "\nPersonnel maximum : " + repr(max_pers) + "\nEchange personnel : " + repr(echange) + "\nCoûts : " + repr(couts) + "\nHeures supplémentaires maximum : " + repr(h_supp)
    
    def _recupere_indice_mois(self, mois_en_cours) -> int:
        """Récupère l'indice du mois en cours."""
        mois = self._inputs_graphe[2]
        for indice, mois in enumerate(mois):
            if mois == mois_en_cours:
                return indice        
    
    def _genere_sommets(self) -> List[List["Sommet"]]:
        """Construit tous les sommets du graphe de déploiement de personnel."""
        depart, _, mois, min_pers, _, echange, _, _ = self._inputs_graphe
        sommets = [
            [depart]
        ]
        for sommet in sommets:
            sommet_min = Sommet.par_str(sommet[0])
            sommet_max = Sommet.par_str(sommet[len(sommet)-1])
            mois_en_cours = sommet_min.mois
            if mois_en_cours == mois[-1]:
                return sommets
            else:
                indice_mois = self._recupere_indice_mois(mois_en_cours)
                employes_max = sommet_max.nb_employes + echange.ajout_max
                if employes_max > max(min_pers):
                    employes_max = max(min_pers)
                if floor(sommet_min.nb_employes * echange.suppression_max) >= 1:
                    employes_min = sommet_min.nb_employes - floor(sommet_min.nb_employes * echange.suppression_max) 
                else:
                    employes_min = sommet_min.nb_employes
                sommets.append(
                    [
                        mois[indice_mois+1] + " - " + str(k)
                        for k in range(employes_min, employes_max+1)
                    ]
                )
                   
    def _sommets_relies(self) -> List[List["Sommet"]]:
        """Renvoie l'ensemble des sommets reliés."""
        echange = self._inputs_graphe[5]
        sommets = self._genere_sommets()
        sommets_relies = []
        for indice_mois, _ in enumerate(sommets):
            if indice_mois < len(sommets)-1:
                for sommet_1 in sommets[indice_mois]:
                    for sommet_2 in sommets[indice_mois+1] :
                        indice_mois_1 = self._recupere_indice_mois(
                            Sommet.par_str(sommet_1).mois
                        )
                        indice_mois_2 = self._recupere_indice_mois(
                            Sommet.par_str(sommet_2).mois
                        )
                        employes_mois_1 = Sommet.par_str(sommet_1).nb_employes
                        employes_mois_2 = Sommet.par_str(sommet_2).nb_employes
                        if indice_mois_2 - indice_mois_1 == 1:
                            if employes_mois_2 >= employes_mois_1*(1 - echange.suppression_max) and employes_mois_2 <= employes_mois_1 + echange.ajout_max:
                                sommets_relies.append(
                                    (sommet_1, sommet_2, 1)
                                )
        return sommets_relies

    def _calcule_couts(self, arrete: Arrete) -> "Arrete":
        """Applique les contraintes de coûts aux sommets reliés."""
        _, _, _, min_pers, max_pers, _, couts, h_supp = self._inputs_graphe
        depart, arrivee, cout = arrete
        employes_dep = Sommet.par_str(depart).nb_employes
        employes_arr = Sommet.par_str(arrivee).nb_employes
        indice_mois_arr = self._recupere_indice_mois(
            Sommet.par_str(arrivee).mois
        )
        cout = abs(employes_arr - employes_dep) * couts.changement  
        if employes_arr < min_pers[indice_mois_arr]:
            if min_pers[indice_mois_arr] - (1 + h_supp) * employes_arr > 0:
                cout += couts.sous_effectif * (min_pers[indice_mois_arr] - (1 + h_supp) * employes_arr)
        else:
            if employes_arr > max_pers[indice_mois_arr]:
                cout += couts.sur_effectif
        return depart, arrivee, cout

    def construit_graphe(self) -> List["Arrete"]:
        """Renvoie le graphe pondéré avec pour chaque arrête :
            - le mois de départ et le nombre d'employés,
            - le mois d'arrivée et le nombre d'employés,
            - le coût pour passer de l'état de départ à l'état d'arrivée.
        """
        return [
            self._calcule_couts(arrete)
            for arrete in self._sommets_relies()
        ]
    
    def contient_arrivee(self) -> bool:
        """Vérifie si le graphe contient le mois de départ et le mois d'arrivée sont reliés."""
        objectif = self._inputs_graphe[1]
        for depart, arrivee, cout in self.construit_graphe():
            if arrivee == objectif:
                return True
        return False
        
    