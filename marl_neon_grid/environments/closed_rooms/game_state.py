import random
from marl_neon_grid.entitites import Agent, Food, Floor, GameState


class ClosedRoomsGameState(GameState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_agents(self):
        floor_tiles = self.entities[Floor.SYMBOL]
        ys = list(sorted([e.y for e in floor_tiles]))
        t1 = list(sorted([e for e in floor_tiles if e.y == min(ys)], key=lambda e: e.x))
        t2 = list(sorted([e for e in floor_tiles if e.y == max(ys)], key=lambda e: e.x))
        agents = [Agent(id=1, pos=t1[int(0.5*len(t1))].pos), Agent(id=2, pos=t2[int(0.5*len(t2))].pos)]
        return agents