Résultats 2017-2018
===================

Les replays sont disponibles à l'adresse suivante: http://webia.lip6.fr/~baskiotisn/2I013/2017/

* Pour les visualiser :  `python examples/show_tournoi.py fichier.jz`
* Pour les charger : `tournoi = load_jsonz(fichier)`
* Pour récupérer un match : `match = tournoi.get_match(i,j)` avec `i` et `j` le numéro des équipes
* Pour récupérer tous les matchs de l'équipe `i` : `matches = tournoi.get_matches(i)`
* Pour afficher les scores : `tournoi.print_scores()`
