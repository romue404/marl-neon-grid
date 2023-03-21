from marl_neon_grid.environments.gridworld import GridWorld
from marl_neon_grid.entitites import Wall, Agent, Food, Entities, Floor
from marl_neon_grid.commands import MovementCommand, EatFoodCommand
from pathlib import Path
from marl_neon_grid.environments.food_n_agents.game_state import FoodNAgentsGameState
import gym


class FoodNAgents(GridWorld):
    ENTITY_POS = {Floor: 0, Wall: 1, Agent: 2, Food: 3}

    def __init__(self, n_agents, n_food=8, max_steps=128, agents_must_coordinate=True):
        self.n_food = n_food
        self.agents_must_coordinate = agents_must_coordinate
        super().__init__(Path(__file__).parent / 'levels' / f'10x10.txt', n_agents)
        self.max_steps = max_steps
        self._renderer = None

        self.action_space = gym.spaces.Discrete(10)

    def prepare_gamestate(self):
        self.game_state = FoodNAgentsGameState(
            entities=Entities(self.lvl_entities),
            n_agents=self.n_agents,
            max_steps=self.max_steps,
            n_food=self.n_food,
            agents_must_coordinate=self.agents_must_coordinate
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
                c = EatFoodCommand(self.game_state, agent)
                commands.append(c)
            else:
                raise NotImplementedError(f'Action {action} is not supported. Use actions from 0-9.')

        events = [c.run() for c in commands]

        reward = self.reward_coordination() if self.agents_must_coordinate else \
            self.reward_no_coordination(events)

        done = self.game_state.is_game_over()

        info = {}
        return self.local_obs(), reward, [done]*len(agents), info

    def reward_no_coordination(self, events):
        reward = [-0.01]*self.n_agents
        for e in events:
            if e.name == 'food_consumed':
                reward[e.agent.id] += 1
        return reward

    def reward_coordination(self):
        consumed_food = [
            food for food in self.game_state.entities.symbol_dict[Food.SYMBOL] \
            if food.current_capacity <= 0
        ]
        reward = [len(consumed_food) - 0.01]*self.n_agents
        return reward


if __name__ == '__main__':
    from marl_neon_grid import FoodNAgents

    n_agents = 2
    gw = FoodNAgents(n_agents=n_agents, n_food=8, max_steps=128, agents_must_coordinate=False)

    for t in range(100):  # simulate 100 episodes
        observations = gw.reset()
        dones = [False] * n_agents
        while not all(dones):
            gw.render()  # render with pygame
            observations, rewards, dones, info = gw.step([gw.action_space.sample(),
                                                          gw.action_space.sample()])  # perform random actions
            # observations, rewards, dones are lists where each entry i belongs to agent i.