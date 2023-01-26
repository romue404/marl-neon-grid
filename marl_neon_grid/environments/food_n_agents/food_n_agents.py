from marl_neon_grid.environments.gridworld import GridWorld
from marl_neon_grid.entitites import Wall, Agent, Food, Entities, Floor
from marl_neon_grid.commands import MovementCommand, OpenDoorCommand
from pathlib import Path
from marl_neon_grid.environments.food_n_agents.game_state import FoodNAgentsGameState


class FoodNAgents(GridWorld):
    ENTITY_POS = {Floor: 0, Wall: 1, Agent: 2, Food: 3}

    def __init__(self, n_agents, n_food=10, max_steps=128):
        self.n_food = n_food
        super().__init__(Path(__file__).parent / 'levels' / f'10x10.txt', n_agents)
        self.max_steps = max_steps
        self._renderer = None

    def prepare_gamestate(self):
        self.game_state = FoodNAgentsGameState(
            entities=Entities(self.lvl_entities),
            n_agents=self.n_agents,
            max_steps=self.max_steps,
            n_food=self.n_food
        )

    def step(self, actions):
        self.game_state.tick()
        commands = []
        agents = self.game_state.agents

        for agent, action in zip(agents, actions):
            if action in self.MOVEMENT_ACTIONS_MAPPING:
                c = MovementCommand(self.game_state, agent, self.MOVEMENT_ACTIONS_MAPPING[action])
                commands.append(c)
            elif action == 9:
                pass
            else:
                raise NotImplementedError('Use actions from 0-9.')

        for c in commands:
            c.run()

        success = False
        obs = {f'agent_{i}': self.local_obs(i) for i in range(len(agents))}
        done = self.game_state.is_game_over() or success
        reward = [1.0]*len(agents) if success else [0.0] * len(agents)
        info = {}
        return obs, reward, [done]*len(agents), info


if __name__ == '__main__':
    gw = FoodNAgents(n_agents=2)
    from tqdm import trange
    print(gw)

    for t in trange(100):
        s = gw.reset()
        for _ in range(200):
            gw.render()
            ns, r, d, _ = gw.step([gw.action_space.sample(), gw.action_space.sample()])
            if all(d):
                #print('DONE', gw.game_state.current_step, gw.game_state.max_steps)
                break
