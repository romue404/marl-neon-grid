import random
from collections import defaultdict
from marl_neon_grid.entitites import Agent, Floor


class GameState(object):
    def __init__(self, entities, n_agents, max_steps):
        super().__init__()
        self.max_steps = max_steps
        self.n_agents = n_agents
        self.current_step = 0
        self.entities = entities
        for agent in self.get_agents():
            self.entities.append(agent)

    def get_agents(self):
        floor_tiles = self.entities[Floor.SYMBOL]
        random.shuffle(floor_tiles)
        agents = [Agent(id=agent_id, pos=ft.pos) for agent_id, ft in enumerate(floor_tiles[:self.n_agents])]
        return agents

    @property
    def agents(self):
        return list(sorted(self.entities[Agent.SYMBOL]))

    def tick(self):
        self.current_step += 1
        for e in self.entities.values():
            e.tick()

    def is_game_over(self):
        return self.current_step >= self.max_steps