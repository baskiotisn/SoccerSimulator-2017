# coding: utf-8
from __future__ import print_function, division
from soccersimulator import SoccerTeam, Simulation, Strategy, show_simu, Vector2D
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT
from .strategies import FonceurTestStrategy

class SimpleParamSearch(object):
    def __init__(self, trials=5, max_round_step=40,discret = 5):
        self.trials = trials
        self.max_round_step = max_round_step
        self.list_forces = [0,0.5,1.,1.5,2,2.5,3,3.5]
        self.list_grille = []
        #Fabrication de la grille de discretisation du terrain
        stepx = GAME_WIDTH/(2.*discret)
        stepy = GAME_HEIGHT/(1.*discret)
        for i in range(discret):
            for j in range(discret):
                self.list_grille.append(Vector2D(GAME_WIDTH/2.+stepx*i,stepy*j))
        self.strategy= FonceurTestStrategy()
    def start(self, show=True):
        team1 = SoccerTeam("Team 1")
        team1.add("Test tire", self.strategy)
        self.simu = Simulation(team1, max_steps=100000)
        self.simu.listeners += self
        if show:
            show_simu(self.simu)
        else:
            self.simu.start()

    def begin_match(self, team1, team2, state):
        self.last = 0  # Step of the last round
        self.crit = 0  # Criterion to maximize (here, number of goals)
        self.cpt = 0  # Counter for trials
        self.res = dict()  # Dictionary of results
        self.idx_force = 0 # counter for parameter index
        self.idx_grille = 0
    def begin_round(self, team1, team2, state):
        # On fixe la position de la balle et du joueur
        ball_pos = self.list_grille[self.idx_grille]
        self.simu.state.states[(1, 0)].position = ball_pos.copy()  
        self.simu.state.states[(1, 0)].vitesse = Vector2D() 
        self.simu.state.ball.position = ball_pos.copy() 
        
        # Set the current value for the current parameter
        self.strategy.strength = self.list_forces[self.idx_force]

        # Last step of the game
        self.last = self.simu.step

    def update_round(self, team1, team2, state):
        # Stop the round if it is too long
        if state.step > self.last + self.max_round_step:
            self.simu.end_round()

    def end_round(self, team1, team2, state):
        # A round ends when there is a goal
        if state.goal > 0:
            self.crit += 1  # Increment criterion
        self.cpt += 1  # Increment number of trials
        if self.cpt >= self.trials:
            key = (self.list_grille[self.idx_grille].x,self.list_grille[self.idx_grille].y,self.list_forces[self.idx_force])
            self.res[key] = self.crit * 1. / self.trials
            print("Res pour  position %s force %f : %f" % (str(self.list_grille[self.idx_grille]),self.list_forces[self.idx_force],self.res[key]))
            # Reset parameters
            self.crit = 0
            self.cpt = 0
            # Go to the next parameter value to try
            self.idx_force+=1
            if self.idx_force >= len(self.list_forces):
                self.idx_grille+=1
                self.idx_force = 0
                if self.idx_grille>=len(self.list_grille):
                    self.simu.end_match()
    def get_res(self):
        return self.res

if __name__=="__main__":
    psearch = SimpleParamSearch()
    psearch.start()