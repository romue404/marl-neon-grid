import numpy as np
import gymnasium as gym
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
        vrs = [(agent.view_radius)**2+1 for agent in self.game_state.agents]
        self.observation_space = gym.spaces.Box(
            shape=(self.n_agents, len(self.ENTITY_POS), vrs[0], vrs[0]),
            high=1, low=-1
        ) # todo support var. obs between agents

    def prepare_gamestate(self):
        self.game_state = GameState(Entities(self.lvl_entities), self.n_agents, self.max_steps)

    def reset(self):
        self.prepare_gamestate()
        self.ray_caster = [RayCaster(agent) for agent in self.game_state.agents]
        if self._renderer is not None:
            self._renderer.quit()
            self._renderer = None

        return self.local_obs()

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

    def local_obs(self):
        observations = []
        for agent_i in range(self.n_agents):
            agent = self.game_state.agents[agent_i]
            entities = self.ray_caster[agent_i].visible_entities(self.game_state.entities)
            obs = np.zeros((len(self.ENTITY_POS), agent.view_radius*2+1, agent.view_radius*2+1))
            for e in set(entities):
                x, y = (e.pos_np - agent.pos_np) + np.array([agent.view_radius, agent.view_radius])
                obs[self.ENTITY_POS[e.__class__], y, x] += e.value
            observations.append(obs)
        return observations

    def local_str_view(self, agent):
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

