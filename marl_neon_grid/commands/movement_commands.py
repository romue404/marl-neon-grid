import numpy as np
from marl_neon_grid.commands import Command, Event, EmptyEvent
from marl_neon_grid.entitites import GameState, Agent, Wall, Door, EntityStates


class MovementCommand(Command):
    def __init__(self, game_state: GameState, agent: Agent, dir_vec: np.ndarray):
        super().__init__(game_state)
        self.entities = self.game_state.entities
        self.agent = agent
        self.dir_vec = dir_vec

    def run(self):
        new_pos = self.agent.pos_np + self.dir_vec
        es = self.game_state.entities[tuple(new_pos)]
        valid = not any([isinstance(e, (Wall, Door)) for e in es]) and not len(es) == 0
        if valid:
            self.agent.pos_np = new_pos
            return Event('agent_moved', agent=self.agent, old_pos=self.agent.pos_np, new_pos=new_pos)
        return EmptyEvent()