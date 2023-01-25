from marl_neon_grid.environments.gridworld import GridWorld
from marl_neon_grid.entitites import Wall, Agent, Door, Entities
from pathlib import Path
from marl_neon_grid.commands import MovementCommand, OpenDoorCommand
from marl_neon_grid.ray_caster import RayCaster


class RedBlueDoors(GridWorld):
    def __init__(self, n_agents, max_steps=128):
        super().__init__(Path(__file__).parent / 'levels' / f'10x10_{n_agents}A.txt', n_agents)
        self.max_steps = max_steps
        self._renderer = None

    def reset(self):
        return super().reset()

    def step(self, actions):
        self.game_state.tick()
        commands = []
        agents = self.game_state.agents

        for agent, action in zip(agents, actions):
            if action in self.MOVEMENT_ACTIONS_MAPPING:
                c = MovementCommand(self.game_state, agent, self.MOVEMENT_ACTIONS_MAPPING[action])
                commands.append(c)
            elif action == 9:
                commands.append(OpenDoorCommand(self.game_state, agent))
            else:
                raise NotImplementedError('Use actions from 0-9.')

        for c in commands:
            c.run()

        doors_hits = [door for door in self.game_state.entities[Door.SYMBOL] if door.open]
        success = len(doors_hits) == len(agents)
        obs = {f'agent_{i}': self.local_obs(agent) for i, agent in enumerate(agents)}
        done = self.game_state.is_game_over() or success
        reward = [1.0]*len(agents) if success else [0.0] * len(agents)
        info = {}
        return obs, reward, [done]*len(agents), info


if __name__ == '__main__':
    gw = RedBlueDoors(n_agents=2)

    print(gw)

    s = gw.reset()
    for _ in range(200):
        gw.render()
        ns, r, d, _ = gw.step([gw.action_space.sample(), gw.action_space.sample()])
        if all(d):
            print('DONE', gw.game_state.current_step, gw.game_state.max_steps)
            break

    print(gw)

    #print(gw.tmp_agents[0])
    #gw.raycast_check(gw.tmp_agents[0])