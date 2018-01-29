from .strategies import RandomStrategy
from soccersimulator import SoccerTeam

def get_team(nb_players):
    myteam = SoccerTeam(name="MaTeam")
    for i in range(nb_players):
        myteam.add("Joueur "+str(i) ,RandomStrategy())
    return myteam