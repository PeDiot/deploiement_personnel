"""Description.

Module de résolution du problème de déploiement de personnel.
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
from typing import List
import networkx as nx
from rich.table import Table
import matplotlib.pyplot as plt


class Resolution:
    """Classe de résolution du problème de déploiement.
    
    Exemple :
    
    >>> probleme = Probleme(
    ...     personnel = [
    ...         Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf),
    ...         Prerequis(mois = "Mars", nb_employes_min = 4, nb_employes_max = Inf),
    ...         Prerequis(mois = "Avril", nb_employes_min = 6, nb_employes_max = Inf),
    ...         Prerequis(mois = "Mai"


    ...         Prerequis(mois = "Mai", nb_employes_min = 7, nb_employes_max = Inf),
    ...         Prerequis(mois = "Juin", nb_employes_min = 4, nb_employes_max = Inf),
    ...         Prerequis(mois = "Juillet", nb_employes_min = 4, nb_employes_max = Inf),
    ...         Prerequis(mois = "Août", nb_employes_min = 2, nb_employes_max = Inf),
    ...         Prerequis(mois = "Septembre", nb_employes_min = 3, nb_employes_max = 3)
    ...     ],
    ...     echange = Echange(3, 1/3),
    ...     couts = Couts(160, 200, 200),
    ...     h_supp = 1/4
    ... )
    
    >>> grapheD = GrapheD(probleme = probleme)
    
    >>> solution = Resolution(grapheD = grapheD)
    
    >>> solution
    Resolution(grapheD = Départ : 'Février - 3'
    Arrivée : 'Septembre - 3'
    Mois : ['Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre']
    Personnel minimum [3, 4, 6, 7, 4, 4, 2, 3]
    Personnel maximum : nf, inf, inf, inf, inf, inf, inf, 3]
    Echange personnel : Echange(ajout_max=3, suppression_max=0.3333333333333333)
    Coûts : Couts(changement=160, sur_effectif=200, sous_effectif=200)
    Heures supplémentaires maximum : 0.25)
    
    >>> solution._est_resolvable()
    True
    
    >>> solution._trouve_chemin()
    ['Février - 3', 'Mars - 4', 'Avril - 5', 'Mai - 5', 'Juin - 5', 'Juillet - 5', 'Août - 4', 'Se
    ptembre - 3']
    
    >>> solution._couts_optimaux()([0, 160, 160, 150.0, 0, 0, 160, 160], [0, 160, 320, 470.0, 470.0, 470.0, 630.0, 790.0])
    
    >>> solution._bilan()[('Février - 3', 0, 0), ('Mars - 4', 160, 160), ('Avril - 5', 160, 320), ('Mai - 5', 150.0,
470.0), ('Juin - 5', 0, 470.0), ('Juillet - 5', 0, 470.0), ('Août - 4', 160, 630.0), ('Septe
mbre - 3', 160, 790.0)]

    >>> solution.affiche()
    ┌───────────┬───────────────────┬──────────────┬───────────────┐
    │ Mois      │ Nombre d'employés │ Coût mensuel │ Coûts cumulés │
    ├───────────┼───────────────────┼──────────────┼───────────────┤
    │ Février   │ 3                 │ 0€           │ 0€            │
    │ Mars      │ 4                 │ 160€         │ 160€          │
    │ Avril     │ 5                 │ 160€         │ 320€          │
    │ Mai       │ 5                 │ 150.0€       │ 470.0€        │
    │ Juin      │ 5                 │ 0€           │ 470.0€        │
    │ Juillet   │ 5                 │ 0€           │ 470.0€        │
    │ Août      │ 4                 │ 160€         │ 630.0€        │
    │ Septembre │ 3                 │ 160€         │ 790.0€        │
    └───────────┴───────────────────┴──────────────┴───────────────┘
    
    >>> probleme_sans_solution = Probleme(
    ...     personnel = [
    ...         Prerequis(mois = "Février", nb_employes_min = 3, nb_employes_max = Inf),
    ...         Prerequis(mois = "Mars", nb_employes_min = 7, nb_employes_max = 7)
    ...     ],
    ...     echange = Echange(3, 1/3),
    ...     couts = Couts(160, 200, 200),
    ...     h_supp = 1/4
    ... )
    
    >>> sans_solution = Resolution(GrapheD(probleme_sans_solution))
    
    >>> sans_solution._est_resolvable()
    False
    
    >>> sans_solution._trouve_chemin()

    >>> sans_solution._couts_optimaux()
    
    >>> sans_solution._bilan()
    
    >>> print(sans_solution._bilan())
    None
    
    >>> sans_solution.affiche()
    None
    
    >>> print(sans_solution.genere_graphique())
    None
    """
    
    def __init__(self, grapheD: GrapheD):
        """Initialisation à partir d'un objet de classe GrapheD."""
        self._grapheD = grapheD
        
    def _est_resolvable(self) -> bool:
        """Teste si le probleme est résolvable."""
        if self._grapheD.contient_arrivee() == True:
            return True
        return False
        
    def __repr__(self):
        """Affichage."""  
        return f"Resolution(grapheD = {self._grapheD})"

    def _genere_nx_graphe(self) -> nx.DiGraph:
        """Crée le graphe networkx associé au problème."""
        if self._est_resolvable():
            resultat = nx.DiGraph()
            resultat.add_weighted_edges_from(
                self._grapheD.construit_graphe(),
                weight = "coût"
            )
            return resultat

    def _trouve_chemin(self) -> List[str]:
        """Résolution du problème avec l'algorithme de Dijsktra."""
        depart, arrivee, _, _, _, _, _, _ = self._grapheD._inputs_graphe
        if self._est_resolvable():
            return nx.shortest_path(
                G = self._genere_nx_graphe(), 
                source = depart,
                target = arrivee,
                weight = "coût"
            )  

    def _couts_optimaux(self) -> List[float]:
        """Renvoie les coûts associés au chemin optimal et les coûts cumulés."""
        if self._est_resolvable():
            graphe_initial = self._genere_nx_graphe()
            graphe_optimal = nx.path_graph(self._trouve_chemin()) 
            couts_cumules = [0]
            couts = [0]
            for arrete in graphe_optimal.edges():
                couts_cumules.append(
                    couts_cumules[-1] + graphe_initial.edges[arrete[0], arrete[1]]["coût"]
                )
                couts.append(
                    graphe_initial.edges[arrete[0], arrete[1]]["coût"]
                )
            return couts, couts_cumules

    def _bilan(self) -> List[Arrete]:
        """Renvoie un bilan des sommets parcourus avec le coût cumulé associé."""
        if self._est_resolvable():
            sommets = self._trouve_chemin()
            couts, couts_cumules = self._couts_optimaux()
            assert len(sommets) == len(couts) == len(couts_cumules)
            return [
                (sommets[i], couts[i], couts_cumules[i])
                for i in range(len(sommets))
            ]

    def genere_table(self) -> Table:
        """Retourn une table rich."""
        if self._est_resolvable():
            resultat = Table()
            resultat.add_column("Mois")
            resultat.add_column("Nombre d'employés")
            resultat.add_column("Coût mensuel")
            resultat.add_column("Coûts cumulés")
            for sommet, cout, couts_cumules in self._bilan():
                resultat.add_row(
                    Sommet.par_str(sommet).mois,
                    str(Sommet.par_str(sommet).nb_employes),
                    str(round(cout, 2)) + "€",
                    str(round(couts_cumules, 2)) + "€"
                )
            return resultat
        
    def affiche(self):
        """Affiche la table directement."""
        from rich import print
        print(self.genere_table())
        
    def graphique_personnel(self, ax) -> plt.Figure:
        """Renvoie le graphique du nombre d'employés optimal."""
        for sommet, cout, couts_cumules in self._bilan():
            ax.hlines(
                y=Sommet.par_str(sommet).mois, 
                xmin=0, 
                xmax=Sommet.par_str(sommet).nb_employes,
                color='gray', 
                alpha=0.7, 
                linewidth=1, 
                linestyles='dashdot'
            )
            ax.scatter(
                y=Sommet.par_str(sommet).mois,
                x=Sommet.par_str(sommet).nb_employes,
                s=60, 
                color='cadetblue', 
                alpha=0.7
            )
        ax.set_xlim(
            0, max(
                [
                    Sommet.par_str(sommet).nb_employes
                    for sommet, _, _ in self._bilan() 
                ]
            ) + 1
        )
        ax.set_yticklabels(
            [sommet[:3] for sommet, _, _ in self._bilan()]
        )
        ax.set_ylabel(" ")
        ax.set_xlabel(" ")
        ax.set_title("Nombre d'employés optimal")

    def graphique_couts(self, ax) -> plt.Figure:
        """Renvoie le graphique des coûts et coûts cumulés."""
        for sommet, cout, couts_cumules in self._bilan():
            ax.vlines(
                x=Sommet.par_str(sommet).mois,
                ymin=0, 
                ymax=couts_cumules, 
                color='cadetblue',
                alpha=0.5,
                linewidth=20
            )
            ax.vlines(
                x=Sommet.par_str(sommet).mois,
                ymin=0, 
                ymax=cout, 
                color='blue',
                alpha=0.3,
                linewidth=20
            )
            ax.text(
                x=Sommet.par_str(sommet).mois,
                y=cout+.3,
                s=str(round(cout, 2))+"€",
                horizontalalignment='center', 
                verticalalignment='bottom',
                color='blue', 
                alpha=.7
            )
            ax.text(
                x=Sommet.par_str(sommet).mois,
                y=couts_cumules+.3,
                s=str(round(couts_cumules, 2))+"€",
                horizontalalignment='center', 
                verticalalignment='bottom',
                color='cadetblue'
                )
        ax.set_ylim(
            0, max(
                [
                    couts_cumules
                    for sommet, _, _ in self._bilan() 
                ]
            ) + 100
        )
        ax.set_xticklabels(
            [sommet[:3] for sommet, _, _ in self._bilan()]
        )
        ax.set_ylabel("Coûts en €")
        ax.set_title("Coûts minimisés")
        ax.legend(["Coûts cumulés", "Coût mensuel"], loc='upper left')
    
    def genere_graphique(self) -> plt.Figure:
        """Renvoie une figure matplotlib pour visualiser la solution."""
        if self._est_resolvable():
            figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
            self.graphique_personnel(ax1)
            self.graphique_couts(ax2)
            plt.show()
