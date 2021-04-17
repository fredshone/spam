import numpy as np
import pandas as pd
from pam.activity import Activity, Leg
from pam.utils import minutes_to_datetime as mtdt


class State:
    
    def __init__(self, person):
        self.person = person
    
    def seed_state(self, state, start_time=0):
        self.state = state
        self.start_time = start_time
        
    def add_activity(self, end_time, leg=True):
        self.person.add(
            Activity(
                act=self.state,
                start_time=mtdt(self.start_time),
                end_time=mtdt(end_time)
            )
        )
        if leg:
            self.person.add(Leg(mode="stumble", start_time=mtdt(end_time), end_time=mtdt(end_time)))

    def update(self, time, state):
        if state == self.state:
            return None
        
        self.add_activity(time)
        self.state = state
        self.start_time = time
        
    def close(self):
        self.add_activity(24*60, leg=False)


class BabyMarkovChain:
    
    possible_states = [
        'sleeping',
        'awake',
        'hungry',
        'crying!',
        "that smell?",
        "peekaboo!"
    ]
    source = 'data/transitions.xls'
    transitions = {
        "sleeping": pd.read_excel(source, sheet_name = 'sleeping').set_index('time'),
        "awake": pd.read_excel(source, sheet_name = 'awake').set_index('time'),
        "hungry": pd.read_excel(source, sheet_name = 'hungry').set_index('time'),
        "crying!": pd.read_excel(source, sheet_name = 'crying').set_index('time'),
        "that smell?": pd.read_excel(source, sheet_name = "what's that smell").set_index('time'),
        "peekaboo!": pd.read_excel(source, sheet_name = 'peekaboo').set_index('time')
    }
    
    def __init__(self, steps=24*60, step_size=15, initial="sleeping"):
        self.steps = steps-step_size
        self.step_size=step_size
        self.time = 0 # first time step
        self.initial_state = initial
        self.state = initial
        self.state_history = [(self.time, self.state)] # states visited
    
    def step(self):
        yield self.time, self.state
        for time in range(1, self.steps, self.step_size):
            self.time += self.step_size
            self.state = self.new_state()
            self.state_history.append((self.time, self.state))
            yield self.time, self.state

    def get_probs(self):
        p = self.transitions[self.state_history[-1][1]].loc[self.time].values
        return p / sum(p)
    
    def new_state(self):
        return np.random.choice(self.possible_states, p=self.get_probs())


class WakeMeUp:
    
    def __init__(self, units, initial, fairness=2, insomnia=.6, tiredness=.2):
        self.units = units
        self.initial_state = self.seed()
        self.last_up = None
        self.fairness = fairness
        self.insomnia = insomnia
        self.tiredness = tiredness
        
    def seed(self):
        for unit in self.units:
            if np.random.random() > 0.2:
                unit.seed_state("sleeping")
            else:
                unit.seed_state("awake")
        
    def update(self, time, baby_state):
        if not baby_state == "sleeping":
            if not self.anyone_awake():
                self.decide_who_gets_up(time)
            else:
                for unit in self.units:
                    if unit.state == "sleeping":
                        if np.random.random() > self.insomnia:
                            unit.update(time, "awake")
        else:
            if self.anyone_awake():
                for unit in self.units:
                    if unit.state == "awake":
                        if np.random.random() > self.tiredness:
                            unit.update(time, "sleeping")
            
    def anyone_awake(self):
        for unit in self.units:
            if unit.state == "awake":
                return True
            
    def decide_who_gets_up(self, time):
        for attempts in range(self.fairness):
            candidate = self.random_choose()
            if not self.last_up == candidate:
                self.last_up = candidate
                candidate.update(time, "awake")
                return None
        self.random_choose().update(time, "awake")
            
    def random_choose(self):
        return np.random.choice(self.units)