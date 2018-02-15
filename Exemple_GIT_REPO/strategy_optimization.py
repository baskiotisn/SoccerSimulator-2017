from profAI import ParamSearch
from profAI import FonceurTestStrategy


expe = ParamSearch(strategy=FonceurTestStrategy(),
                   params={'strength': [0.1, 1]})
expe.start()
print(expe.get_res())




#from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
#
#
### Creation d'une equipe
#py = SoccerTeam(name="PyTeam")
#thon = SoccerTeam(name="ThonTeam")
#py.add("PyPlayer",FonceurTestStrategy())
#thon.add("ThonPlayer",Strategy())
#
##Creation d'une partie
#simu = Simulation(py,thon)
##Jouer et afficher la partie
#show_simu(simu)
