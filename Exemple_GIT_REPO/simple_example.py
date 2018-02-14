from soccersimulator import SoccerTeam, Simulation, show_simu
from profAI import FonceurStrategy,DefenseurStrategy,get_team


## Creation d'une equipe
pyteam = get_team(2)
thon = SoccerTeam(name="ThonTeam")
thon.add("PyPlayer",FonceurStrategy()) #Strategie qui ne fait rien
thon.add("ThonPlayer",DefenseurStrategy())   #Strategie aleatoire

#Creation d'une partie
simu = Simulation(pyteam,thon)
#Jouer et afficher la partie
show_simu(simu)
