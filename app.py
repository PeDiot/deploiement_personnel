"""Description.

Libraire pour un gui de la librairie deploiement.
"""
import ipywidgets as ipw
from IPython.display import display
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

class Application:
    def __init__(self):
        self.bouton = ipw.Button(description="Résoudre")
        self.zone_entree_personnel = ipw.Textarea(
            description="Personnel",
            value="Février / 3 /  \nMars / 4 /  \nAvril / 6 /  \nMai / 7 /  \nJuin / 4 /  \nJuillet / 6 /  \nAoût / 2 /", 
            layout=ipw.Layout(height="200px", width="250px")
        )
        self.zone_entree_objectif = ipw.Textarea(
            description="Objectif",
            value="Septembre / 3 / 3", 
            layout=ipw.Layout(width="250px")
        )
        self.zone_entree_ajout_max = ipw.BoundedIntText(
            value=3,
            min=0,
            max=10000000,
            step=1,
            disabled=False,
            layout=ipw.Layout(width="50px")
        )
        self.zone_entree_suppression_max = ipw.BoundedFloatText(
            value=33.0,
            min=0,
            max=100.0,
            step=1,
            disabled=False,
            layout=ipw.Layout(width="50px")
        )
        self.zone_entree_echange = ipw.HBox(
            [
                ipw.Label(value = "Ajout / Suppression (%)"),
                self.zone_entree_ajout_max,
                self.zone_entree_suppression_max
            ],
            layout=ipw.Layout(width="250px")
        )
        self.zone_entree_couts_changement = ipw.FloatText(
            value=160.0,
            disabled=False,
            layout=ipw.Layout(width="50px")
        )       
        self.zone_entree_couts_sur_effectif = ipw.FloatText(
            value=200.0,
            disabled=False,
            layout=ipw.Layout(width="50px")
        )
        self.zone_entree_couts_sous_effectif = ipw.FloatText(
            value=200.0,
            disabled=False,
            layout=ipw.Layout(width="50px")
        )
        self.zone_entree_couts = ipw.HBox(
            [
                ipw.Label(value = "Coûts (€)"),
                self.zone_entree_couts_changement,
                self.zone_entree_couts_sur_effectif,
                self.zone_entree_couts_sous_effectif
            ],
            layout=ipw.Layout(width="250px")
        )
        self.zone_entree_h_supp = ipw.BoundedFloatText(
            value=25.0,
            min=0,
            max=100.0,
            step=1,
            layout=ipw.Layout(width="50px"),
            disabled=False
        )
        self.zone_donnees = ipw.VBox(
            [
                ipw.Label(value='Entrer vos données'),
                self.bouton, 
                self.zone_entree_objectif,
                self.zone_entree_personnel,
                self.zone_entree_echange,
                ipw.HBox(
                    [
                        ipw.Label(value = "Heures supplémentaires (%)"),
                        self.zone_entree_h_supp
                    ],
                    layout=ipw.Layout(width="250px")
                ),
                self.zone_entree_couts
            ],
            layout=ipw.Layout(width="350px")
        )
        self.zone_probleme = ipw.Output(layout={'width': '400px'})
        self.zone_solution = ipw.Output()
        self.zone_graphique = ipw.Output()
        self.total = ipw.HBox(
            [
                self.zone_donnees,
                ipw.VBox(
                    [
                        ipw.Label(value='Problème de déploiement associé'),
                        self.zone_probleme
                    ]
                ),
                ipw.VBox(
                    [
                        ipw.Label(value='Solution du problème de déploiement'),
                        self.zone_solution,
                        self.zone_graphique
                    ]
                )
            ]
        ) 
        self._sur_clique(self.bouton)
        self.bouton.on_click(self._sur_clique)
        
    def affichage(self):    
        display(self.total)
    
    def _sur_clique(self, b):
        self.zone_probleme.clear_output()
        self.zone_solution.clear_output()
        self.zone_graphique.clear_output()
        echange_str = f"""
        {str(self.zone_entree_ajout_max.value)} / {str(self.zone_entree_suppression_max.value/100)}
        """
        couts_str = f"""
        {str(self.zone_entree_couts_changement.value)} / {str(self.zone_entree_couts_sur_effectif.value)} / {str(self.zone_entree_couts_sous_effectif.value)}
        """
        try:
            probleme = Probleme.par_str(
                self.zone_entree_personnel.value + "   \n" + self.zone_entree_objectif.value,
                echange_str,
                couts_str,
                str(self.zone_entree_h_supp.value/100)
            )       
            solution = Resolution(
                grapheD=GrapheD(probleme=probleme)
            )
        except ValueError:
            probleme = None
        with self.zone_probleme:
            if probleme is not None:
                display(probleme.genere_table_personnel())
                display(probleme.genere_table_contraintes())
                display(probleme._couts.genere_table_couts())
            else:
                print(f"Veuillez relire le mode d'emploi \npour rentrer les données correctement !")
        with self.zone_solution:
            if probleme is not None:
                if solution._est_resolvable():
                    display(solution.genere_table())
                    solution.genere_graphique()
                else:
                    print(f"Configuration incorrecte ! \nIl ne peut pas y avoir {probleme[probleme.mois[-1]].nb_employes_min} employé(s) présent(s) au mois de {probleme[probleme.mois[-1]].mois}.")