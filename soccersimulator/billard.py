from . import settings
from .utils import Vector2D, MobileMixin
from .mdpsoccer import SoccerState, Simulation, Ball,PlayerState
from .utils import dict_to_json
import math

MAX_SHOOT_SPEED = 0.1
settings.BALL_RADIUS=1.5
MAX_BALL_SHOOT_SPEED = 0.01
def get_collision(a,b):
    ### a, b MobileMixin
    vdir = (b.position-a.position).normalize()
    vnorm = Vector2D(norm=1.,angle = vdir.angle+math.pi/2.)
    newa = b.vitesse.dot(vdir)*vdir+a.vitesse.dot(vnorm)*vnorm
    newb = a.vitesse.dot(vdir)*vdir+b.vitesse.dot(vnorm)*vnorm
    return newa,newb

class PlayerStateBillard(PlayerState):
    def __init__(self,position=None,vitesse=None,**kwargs):
        super(PlayerStateBillard,self).__init__(position,vitesse,**kwargs)
    def next(self,ball,action=None):
        res = super(PlayerStateBillard,self).next(ball,action)
        if res.norm ==0:
            return res
        if self.vitesse.norm>MAX_SHOOT_SPEED or ball.vitesse.norm>MAX_BALL_SHOOT_SPEED:
            return Vector2D()
        return self.shoot

class BillardState(SoccerState):
    def __init__(self,states=None,ball=None,balls=None,**kwargs):
        self.states = states or dict()
        self.balls  = balls
        self.ball = ball
        self.strategies = kwargs.pop('strategies',dict())
        self.score = kwargs.pop('score',{1:0,2:0})
        self.step = kwargs.pop('step',0)
        self.max_steps = kwargs.pop('max_steps',settings.MAX_GAME_STEPS)
        self.goal = kwargs.pop('goal',0)
        self.__dict__.update(kwargs)
    def to_dict(self):
        return dict(states = dict_to_json(self.states), strategies = dict_to_json(self.strategies), ball = self.ball,score=dict_to_json(self.score),step=self.step,max_steps=self.max_steps,goal=self.goal,balls=self.balls)
    def apply_actions(self,actions=None,strategies=None):
        if strategies: self.strategies.update(strategies)
        sum_of_shoots = Vector2D()
        self.goal = 0
        if actions:
            for k, c in self.states.items():
                if k in actions:
                    sum_of_shoots += c.next(self.ball, actions[k])
        self.ball.next(sum_of_shoots)
        lballs = self.balls+[self.ball]
        djvu = []
        newlballs = []
        for b in lballs:
            ball_col = [bb for bb in lballs if b!=bb and b.position.distance(bb.position)<=(2*settings.BALL_RADIUS) and  bb not in djvu]
            if len(ball_col)>0:
                vball,vb=get_collision(b,ball_col[0])
                b.vitesse=vball
                ball_col[0].vitesse=vb
               
            if b != self.ball:
                if b.inside_goal() and b.position.x>settings.GAME_WIDTH:
                    self.score[1]+=1
                else:
                    newlballs.append(b)     
                
            if b.position.x < 0:
                b.position.x = -b.position.x
                b.vitesse.x = -b.vitesse.x
            if b.position.y < 0:
                b.position.y = -b.position.y
                b.vitesse.y = -b.vitesse.y
            if b.position.x > settings.GAME_WIDTH:
                b.position.x = 2 * settings.GAME_WIDTH - b.position.x
                b.vitesse.x = -b.vitesse.x
            if b.position.y > settings.GAME_HEIGHT:
                b.position.y = 2 * settings.GAME_HEIGHT - b.position.y
                b.vitesse.y = -b.vitesse.y
            djvu.append(b)
        self.balls = newlballs
        for b in self.balls:
            b.next(Vector2D())
        self.step += 1

    def stop(self):
        return len(self.balls)<=0       
    @classmethod
    def create_initial_state(cls,type_game=0):
        state = cls()
        state.reset_state(type_game=type_game)
        return state       
    def reset_state(self,type_game=0):
        self.states =dict()
        self.states[(1,0)] = PlayerStateBillard(position=Vector2D(settings.GAME_WIDTH*0.1,settings.GAME_HEIGHT*0.5))
        self.ball = Ball(Vector2D(settings.GAME_WIDTH*0.25,settings.GAME_HEIGHT*0.5))
        self.balls = []
        if type_game==0:
            self.balls=[Ball(Vector2D(settings.GAME_WIDTH*0.75,settings.GAME_HEIGHT*0.75))]
        if type_game==1:
            self.balls=[Ball(Vector2D(settings.GAME_WIDTH*0.75,settings.GAME_HEIGHT*0.7)), 
            Ball(Vector2D(settings.GAME_WIDTH*0.8,settings.GAME_HEIGHT*0.5))]
        if type_game==2:
            self.balls = [Ball(Vector2D(settings.GAME_WIDTH*0.5,settings.GAME_HEIGHT*0.75)), 
            Ball(Vector2D(settings.GAME_WIDTH*0.5,settings.GAME_HEIGHT*0.25)),
            Ball(Vector2D(settings.GAME_WIDTH*0.75,settings.GAME_HEIGHT*0.5))]
        self.goal = 0

class Billard(Simulation):
    def __init__(self,team1=None,max_steps=20000,initial_state = None,type_game=0,**kwarg):
        init_state = initial_state or BillardState.create_initial_state(type_game)
        super(Billard,self).__init__(team1=team1,initial_state = init_state,max_steps=max_steps,**kwarg)
    def stop(self):
        return super(Billard,self).stop() or self.state.stop()
