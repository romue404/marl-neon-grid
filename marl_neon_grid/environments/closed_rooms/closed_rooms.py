import random

from marl_neon_grid.environments.gridworld import GridWorld
from marl_neon_grid.entitites import Wall, Agent, Food, Entities, Floor, Zone
from marl_neon_grid.commands import MovementCommand
from pathlib import Path
from marl_neon_grid.environments.closed_rooms.game_state import ClosedRoomsGameState
import gym


class ClosedRooms(GridWorld):
    ENTITY_POS = {Floor: 0, Wall: 1, Agent: 2, Food: 3, Zone: 4}

    def __init__(self, max_steps=128):
        self.lvl_entities_left, _ = self.parse_level(Path(__file__).parent / 'levels' / f'10x10_left.txt')
        self.lvl_entities_right, _ = self.parse_level(Path(__file__).parent / 'levels' / f'10x10_right.txt')
        super().__init__(Path(__file__).parent / 'levels' / f'10x10_left.txt', n_agents=2)
        self.max_steps = max_steps
        self._renderer = None
        self.action_space = gym.spaces.Discrete(9)

    def reset(self):
        super().reset()

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

        for agent, action in zip(agents, actions):
            if action in self.MOVEMENT_ACTIONS_MAPPING:
                c = MovementCommand(self.game_state, agent, self.MOVEMENT_ACTIONS_MAPPING[action])
                commands.append(c)

            else:
                raise NotImplementedError('Use actions from 0-9.')

        for c in commands:
            c.run()

        success = all(agent.pos in [e.pos for e in self.game_state.entities[agent.pos] if isinstance(e, Zone)] for agent in agents)
        obs = {f'agent_{i}': self.local_obs(i) for i in range(len(agents))}
        obs['agent_1'][self.ENTITY_POS[Zone]] = 0.0  # goal is invisible to second agent

        done = self.game_state.is_game_over() or success
        reward = [1.0]*len(agents) if success else [0.0] * len(agents)
        info = {}
        return obs, reward, [done]*len(agents), info


if __name__ == '__main__':
    gw = ClosedRooms()
    from tqdm import trange

    for t in trange(100):
        s = gw.reset()
        for _ in range(200):
            gw.render()
            ns, r, d, _ = gw.step([gw.action_space.sample(), gw.action_space.sample()])
            if all(d):
                #print('DONE', gw.game_state.current_step, gw.game_state.max_steps)
                break
