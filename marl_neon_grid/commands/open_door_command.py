import numpy as np
from marl_neon_grid.entitites import GameState, Agent, Door, DoorStates


class OpenDoorCommand(object):
    def __init__(self, game_state: GameState, agent: Agent, **kwargs):
        super().__init__()
        self.game_state = game_state
        self.entities = self.game_state.entities
        self.agent = agent

    def check_around(self, agent):
        points = [np.array([i, j]) for i in range(-1, 2) for j in range(-1, 2)]
        entities_around = [self.game_state.entities[tuple(agent.pos_np + dir_v)] for dir_v in points]
        return sum(entities_around, [])  # flatten

    def run(self):
        doors = [e for e in self.check_around(self.agent) if isinstance(e, Door)]
        for door in doors:
            door.state = DoorStates.OPEN