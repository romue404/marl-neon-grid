import random

from marl_neon_grid.environments.gridworld import GridWorld
from marl_neon_grid.entitites import Wall, Agent, Food, Entities, Floor, Zone
from marl_neon_grid.commands import MovementCommand
from pathlib import Path
from marl_neon_grid.environments.closed_rooms.game_state import ClosedRoomsGameState
import gym


class ClosedRooms(GridWorld):
    ENTITY_POS = {Floor: 0, Wall: 1, Agent: 2, Food: 3, Zone: 4}

    def __init__(self, max_steps=32):
        self.lvl_entities_left, _ = self.parse_level(Path(__file__).parent / 'levels' / f'10x10_left.txt')
        self.lvl_entities_right, _ = self.parse_level(Path(__file__).parent / 'levels' / f'10x10_right.txt')
        super().__init__(Path(__file__).parent / 'levels' / f'10x10_left.txt', n_agents=2)
        self.max_steps = max_steps
        self._renderer = None
        self.action_space = gym.spaces.Discrete(9)

    def prepare_gamestate(self):
        entities = random.choice([self.lvl_entities_left, self.lvl_entities_right])
        self.lvl_entities = entities.copy()

        self.game_state = ClosedRoomsGameState(
            entities=Entities(self.lvl_entities),
            n_agents=self.n_agents,
            max_steps=self.max_steps,
        )

    def step(self, actions):
        self.game_state.tick()
        commands = []
        agents = self.game_state.agents
        reward = [0]*len(agents)

        for ag_i, (agent, action) in enumerate(zip(agents, actions)):
            if action in self.MOVEMENT_ACTIONS_MAPPING:
                c = MovementCommand(self.game_state, agent, self.MOVEMENT_ACTIONS_MAPPING[action])
                commands.append(c)

            else:
                raise NotImplementedError('Use actions from 0-9.')

        for c in commands:
            c.run()

        reward = [int(agent.pos in [e.pos for e in self.game_state.entities[agent.pos] if isinstance(e, Zone)])
                  for agent in agents]
        success = False#sum(reward) == self.n_agents
        reward =  [0.25*r -0.01 for r in reward]

        #reward = [2.0]*len(agents) if success else [0.05*r - 0.01 for r in reward]

        obs = self.local_obs()
        obs[1][self.ENTITY_POS[Zone]] = 0.0  # goal is invisible to second agent
        done = self.game_state.is_game_over() or success

        info = {}
        return obs, reward, [done]*len(agents), info