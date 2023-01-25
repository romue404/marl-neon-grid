import numpy as np
import gym
from marl_neon_grid.entitites import Agent, Door, Floor, Wall, GameState, Entities
from marl_neon_grid.ray_caster import RayCaster


class GridWorld(gym.Env):
    ENTITY_POS = {Floor: 0, Wall: 1, Agent: 2, Door: 3}
    MOVEMENT_ACTIONS_MAPPING = {
        0: Agent.NORTH, 1: Agent.NORTH_EAST, 2: Agent.EAST, 3: Agent.SOUTH_EAST,
        4: Agent.SOUTH, 5: Agent.SOUTH_WEST, 6: Agent.WEST, 7: Agent.NORTH_WEST,
        8: Agent.NO_OP
    }

    def __init__(self, level_path, n_agents, max_steps=128):
        self.n_agents = n_agents
        self.max_steps = max_steps
        self.lvl_entities, self.shape = self.parse_level(level_path)
        self.action_space = gym.spaces.Discrete(9)
        self._renderer = None
        self.reset()
        self.observation_space = None # todo

    def reset(self):
        self.game_state = GameState(Entities(self.lvl_entities),
                                    self.n_agents,
                                    self.max_steps)

        if self._renderer is not None:
            self._renderer.quit()
            self._renderer = None

        return {f'agent_{i}': self.local_obs(agent) for i, agent in enumerate(self.game_state.agents)}

    def parse_level(self, path):
        with path.open('r') as f:
            grid_string = f.read()
        rows = grid_string.strip().split('\n')
        rows =  [list(row) for row in rows]
        entities = []
        for y, row in enumerate(rows):
            kv = {e.SYMBOL: e for e in self.ENTITY_POS.keys()}
            for x, entity_char in enumerate(row):
                entities.append(kv[entity_char](pos=(x, y)))
        return entities, (len(rows), len(rows[0]))

    def local_obs(self, agent):
        entities = RayCaster(agent).visible_entities(self.game_state.entities)
        obs = np.zeros((len(self.ENTITY_POS), agent.view_radius*2+1, agent.view_radius*2+1))
        for e in set(entities):
            x, y = (e._pos_np - agent._pos_np) + np.array([agent.view_radius, agent.view_radius])
            obs[self.ENTITY_POS[e.__class__], y, x] += 1.0
        return obs

    def local_str_view(self, agent):
        #entities = [self.entities[tuple(pos)] for pos in agent.observable_coords if tuple(pos) in self.entities]
        entities = RayCaster(agent).visible_entities(self.game_state.entities)
        view = [['/' for _ in range(agent.view_radius*2+1)] for _ in range(agent.view_radius*2+1)]
        for e in entities:
            v = (e._pos_np - agent._pos_np) + np.array([agent.view_radius, agent.view_radius])
            view[v[1]][v[0]] = e.SYMBOL
        return view

    def __str__(self):
        lvl = [['-' for _ in range(self.shape[0])] for _ in range(self.shape[1])]
        for e in self.game_state.entities.values():
            lvl[e.y][e.x] = e.SYMBOL
        return '\n'.join([''.join(row) for row in lvl])

    def check_around(self, agent):
        entities_around = [self.game_state.entities[tuple(agent.pos_np + dir_v)] \
                           for dir_v in self.MOVEMENT_ACTIONS_MAPPING.values()]
        return sum(entities_around, [])  # flatten

    def step(self, actions):
        pass

    def render(self, mode="human"):
        if not self._renderer:
            from marl_neon_grid.rendering import Renderer
            h, w = max(self.lvl_entities, key=lambda e: e.y).y, max(self.lvl_entities, key=lambda e: e.x).x
            self._renderer = Renderer(lvl_shape=(h+1, w+1), fps=4)
        self._renderer.render(self.game_state)

