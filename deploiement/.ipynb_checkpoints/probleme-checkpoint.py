""" Description.

Classes Mois et Probleme permettant de décrire le problème initial de minimisation des coûts de déploiement de personnel.
"""

from typing import List, Generator, Any, Union
from dataclasses import dataclass
from rich.table import Table

Mois = str
Employes = Union[int, float]
Inf = float("inf")
Cout = Union[int, float]

@dataclass
class Couts:
    """Représente les coûts associés au déploiement de personnel.
    
    Exemple:
    
    >>> couts = Couts(100, 300, 200)
    >>> couts
    Couts(changement=100, sur_effectif=300, sous_effectif=200)
   >>> couts.affiche()
    ┌──────────────────────┐
    │ Coûts                │
    ├──────────────────────┤
    │ Changement : 100€    │
    │ Sur-effectif : 200€  │
    │ Sous-effectif : 300€ │
    └──────────────────────┘
    """
    
    changement: Cout
    sur_effectif: Cout
    sous_effectif: Cout
    
    def __post_init__(self):
        """Vérifie que les coûts sont positifs."""
        if self.changement < 0 or self.sur_effectif < 0 or self.sous_effectif < 0:
            raise ValueError("Un coût doit être positif.")
            
    def genere_table_couts(self) -> Table:
        """Renvoie une table rich."""
        resultat = Table()
        resultat.add_column("Coûts")
        resultat.add_row(
            "Changement : " + str(self.changement) + "€"
            )
        resultat.add_row(
            "Sur-effectif : " + str(self.sous_effectif) + "€"
            )
        resultat.add_row(
            "Sous-effectif : " + str(self.sur_effectif) + "€"
            )
        return resultat
    
    def affiche(self):
        """Affiche la table directement."""
        from rich import print
        print(self.genere_table_couts())
            
            
@dataclass
class Prerequis:
    """Représente un mois avec les prérequis sur le nombre d'employés présents."""
    
    mois: Mois
    nb_employes_min: Employes
    nb_employes_max: Employes
        
    def __post_init__(self):
        """Vérifie que le nombre d'employés est positif 
        et que le nombre d'employés max est au moins égal au nombre d'employés min."""
        if self.nb_employes_min < 0 or self.nb_employes_max < 0:
            raise ValueError("Le nombre d'employés doit être positif.")
        if self.nb_employes_min > self.nb_employes_max:
            raise ValueError("Le nombre d'employés maximal doit être au moins égal au nombre d'employés mininimum.")
            

@dataclass
class Echange:
    """Représente les échanges d'employés autorisés."""
    
    ajout_max: Employes
    suppression_max: Employes
        
    def __post_init__(self):
        """Vérifie qu'un échange est positif et qu'on ne peut pas enlever tout le personnel présent."""
        if self.ajout_max < 0 or self.suppression_max < 0:
            raise ValueError("Un changement doit être positif.")
        if self.suppression_max >= 1:
            raise ValueError("On ne peut pas enlever tout le personnel présent.")
    

class Probleme:
    """Représente un problème initial de déploiement de personnel.
    
    Exemple :

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
    
    >>> probleme
    Probleme(
        personnel = [
            Prerequis(mois='Février', nb_employes_min=3, nb_employes_max=inf),
            Prerequis(mois='Mars', nb_employes_min=4, nb_employes_max=inf),
            Prerequis(mois='Avril', nb_employes_min=7, nb_employes_max=inf),
            Prerequis(mois='Mai', nb_employes_min=7, nb_employes_max=inf),
            Prerequis(mois='Juin', nb_employes_min=5, nb_employes_max=5)], 
        echange = Echange(ajout_max=3, suppression_max=0.3333333333333333), 
        couts = Couts(changement=160, sur_effectif=200, sous_effectif=200),
        h_supp = 0.25
    )
    
    >>> print(probleme)
    Personnel :
    Prerequis(mois='Février', nb_employes_min=3, nb_employes_max=inf)
    Prerequis(mois='Mars', nb_employes_min=4, nb_employes_max=inf)
    Prerequis(mois='Avril', nb_employes_min=7, nb_employes_max=inf)
    Prerequis(mois='Mai', nb_employes_min=7, nb_employes_max=inf)
    Prerequis(mois='Juin', nb_employes_min=5, nb_employes_max=5)
    Echange :
    Echange(ajout_max=3, suppression_max=0.3333333333333333)
    Coûts :
    Couts(changement=160, sur_effectif=200, sous_effectif=200)
    Heures supplémentaires :
    0.25
    
    >>> for prerequis in probleme.personnel: print(prerequis)
    ...
    Prerequis(mois='Février', nb_employes_min=3, nb_employes_max=inf)
    Prerequis(mois='Mars', nb_employes_min=4, nb_employes_max=inf)
    Prerequis(mois='Avril', nb_employes_min=7, nb_employes_max=inf)
    Prerequis(mois='Mai', nb_employes_min=7, nb_employes_max=inf)
    Prerequis(mois='Juin', nb_employes_min=5, nb_employes_max=5)
    
    >>> for mois in probleme.mois: print(mois)
    ...
    Février
    Mars
    Avril
    Mai
    Juin
        
    >>> probleme["Avril"]
    Prerequis(mois='Avril', nb_employes_min=7, nb_employes_max=inf)

    >>> personnel_str = '''
    ... Février / 3 /
    ... Mars / 4 /
    ... Avril / 7 /
    ... Mai / 7 /
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
    >>> probleme_bis = Probleme.par_str(personnel_str, echange_str, couts_str,
    h_supp_str)
    
    >>> probleme_bis == probleme
    True
    
    >>> probleme.affiche()
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
    """
    
    def __init__(self, personnel: List[Prerequis], echange: Echange, couts: Cout, h_supp: float):
        """Initialisation du problème. 
        Stocke la liste des prérequis sur le personnel sous forme de dictionnaire.
        Vérifie que les mois sont bien consécutifs."""
        self._couts = couts
        self._echange = echange
        self._h_supp = h_supp
        self._personnel: Dict[Mois, Prerequis] = dict()
        for prerequis in personnel:
            if prerequis.mois in self._personnel:
                raise ValueError(f"{prerequis.mois} apparait 2 fois!")
            self._personnel[prerequis.mois] = prerequis
        mois = [key for key in self._personnel.keys()]
        if self._personnel[mois[-1]].nb_employes_min != self._personnel[mois[-1]].nb_employes_max:
            raise ValueError(f"Il faut indiquer 2 fois le nombre d'employés présents au mois de {mois[-1]}.")
               
    @staticmethod
    def _encode_prerequis(ligne) -> Prerequis:
        """Encode une ligne en prérequis."""
        mois, nb_employes_min, nb_employes_max = ligne.split("/")
        mois_valide = mois.strip()
        nb_employes_min_valide: Employes = int(nb_employes_min.strip())
        try:
            nb_employes_max_valide: Employes = int(nb_employes_max.strip())
        except ValueError:
            nb_employes_max_valide: Employes = Inf         
        return Prerequis(
            mois = mois_valide,
            nb_employes_min = nb_employes_min_valide,
            nb_employes_max = nb_employes_max_valide
        )

    @staticmethod
    def _encode_echange(ligne) -> Echange:
        """Encode une ligne en objet de classe Echange."""
        ajout_max, suppression_max = ligne.split("/")
        ajout_max_valide = int(ajout_max.strip())
        suppression_max_valide = float(suppression_max)
        return Echange(ajout_max_valide, suppression_max_valide)
    
    @staticmethod
    def _encode_couts(ligne) -> Couts:
        """Encode une ligne en objet de classe Echange."""
        changement, sur_effectif, sous_effectif = ligne.split("/")
        changement_valide = float(changement.strip())
        sur_effectif_valide = float(sur_effectif.strip())
        sous_effectif_valide = float(sous_effectif.strip())
        return Couts(changement_valide, sur_effectif_valide, sous_effectif_valide) 

    @classmethod
    def par_str(cls, personnel_str: str, echange_str: str, couts_str: str, h_supp_str: str) -> "Probleme":
        """Constructeur alternatif.""" 
        personnel_valide = list()
        try: 
            for prerequis in personnel_str.strip().splitlines():
                personnel_valide.append(cls._encode_prerequis(prerequis))
        except ValueError:
            raise ValueError("Il ne faut pas sauter de ligne entre les prérequis !")
        echange_valide = cls._encode_echange(echange_str)
        couts_valide = cls._encode_couts(couts_str)
        h_supp_valide = float(h_supp_str.strip())
        return cls(personnel_valide, echange_valide, couts_valide, h_supp_valide)
        
    @property
    def personnel(self) -> Generator[Prerequis, None, None]:
        """Itére sur les prérequis portant sur le personnel."""
        yield from self._personnel.values()
    
    @property
    def mois(self) -> List[Mois]:
        """Liste des mois."""
        return [
            key for key in self._personnel.keys()
        ]        
    
    def __eq__(self, autre: Any) -> bool:
        """Egalite."""
        if type(autre) != type(self):
            return False
        return self._personnel == autre._personnel

    def __repr__(self) -> str:
        """Renvoie la liste de construction."""
        return f"Probleme(personnel = {list(self.personnel) !r}, echange = {self._echange}, couts = {self._couts}, h_supp = {self._h_supp})"

    def __str__(self) -> str:
        """Affiche le problème lisiblement."""
        return "Personnel : \n" + "\n".join(repr(prerequis) for prerequis in self.personnel) + "\n" + "Echange : \n" + repr(self._echange) + "\n" + "Coûts : \n" + repr(self._couts) + "\n" + "Heures supplémentaires : \n" + repr(self._h_supp)
    
    def __getitem__(self, mois: Mois) -> Prerequis:
        """Accès aux prérequis par le mois correspondant."""
        return self._personnel[mois]
    
    def genere_table_personnel(self) -> Table:
        """Renvoie une table rich des prérequis."""
        resultat = Table()
        resultat.add_column("Mois")
        resultat.add_column("Nombre d'employés minimal")
        for contrainte in self.personnel:
            resultat.add_row(
                contrainte.mois, str(contrainte.nb_employes_min)
            )
        return resultat
               
    def genere_table_contraintes(self) -> Table:
        """Renvoie une table rich."""
        resultat = Table()
        resultat.add_column("Contraintes")
        resultat.add_row(
            "Ajout maximal d'employés : " + str(self._echange.ajout_max)
        )
        resultat.add_row(
            "Suppression maximale d'employés : " + str(100*round(self._echange.suppression_max, 2)) + "%"
        )
        resultat.add_row(
            str(100 * self._h_supp) + "% d'heures supplémentaires"
        )
        return resultat
    
    def affiche(self):
        """Affiche la table directement."""
        from rich import print
        print(self.genere_table_personnel())
        print(self._couts.genere_table_couts())
        print(self.genere_table_contraintes())