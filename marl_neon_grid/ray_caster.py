import math
import itertools
import numpy as np
import pandas as pd
from numba import njit, jit
from typing import List



class RayCaster:
    def __init__(self, agent, degs=360):
        self.agent = agent
        self.n_rays = 100#(agent.view_radius + 1) * 8
        self.degs = degs
        self.ray_targets = self.build_ray_targets()

    def build_ray_targets(self):
        north = np.array([0, -1])*self.agent.view_radius
        thetas = [np.deg2rad(deg) for deg in np.linspace(-self.degs // 2, self.degs // 2, self.n_rays)[::-1]]
        rot_M = [
            [[math.cos(theta), -math.sin(theta)],
             [math.sin(theta), math.cos(theta)]] for theta in thetas
        ]
        rot_M = np.stack(rot_M, 0)
        rot_M = np.unique(np.round(rot_M @ north), axis=0)
        return rot_M

    def visible_entities(self, entities):
        visible = []
        for ray in self.get_rays():
            rx, ry = ray[0]
            for x, y in ray:  # important to exclude own coordinates
                cx, cy = x - rx, y - ry
                try:
                    hits = entities.pos_dict[(x, y)]
                    diag_hits = all([e.blocks_ray for e in entities.pos_dict[(x, y-cy)] + entities.pos_dict[(x-cx, y)]]) \
                        if (cx != 0 and cy != 0) else False
                    visible += hits if not diag_hits else []
                    if any([e.blocks_ray for e in hits]) or diag_hits:
                        break
                except KeyError as e:
                    pass
                rx, ry = x, y
        return visible

    def get_rays(self):
        outline, a_pos = self.get_fov_outline().astype(int), self.agent.pos
        return self.bresenham_loop(a_pos, outline)

    # todo do this once and cache the points!
    def get_fov_outline(self) -> np.ndarray:
        return self.ray_targets + self.agent.pos_np

    def get_square_outline(self):
        agent = self.agent
        x_coords = range(agent.x - agent.view_radius, agent.x + agent.view_radius + 1)
        y_coords = range(agent.y - agent.view_radius, agent.y + agent.view_radius + 1)
        outline = list(itertools.product(x_coords, [agent.y - agent.view_radius, agent.y + agent.view_radius])) \
                  + list(itertools.product([agent.x - agent.view_radius, agent.x + agent.view_radius], y_coords))
        return outline
    #
    @staticmethod
    @njit
    def bresenham_loop(a_pos, points):
        results = []
        for end in points:
            x1, y1 = a_pos
            x2, y2 = end
            dx = x2 - x1
            dy = y2 - y1

            # Determine how steep the line is
            is_steep = abs(dy) > abs(dx)

            # Rotate line
            if is_steep:
                x1, y1 = y1, x1
                x2, y2 = y2, x2

            # Swap start and end points if necessary and store swap state
            swapped = False
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
                swapped = True

            # Recalculate differentials
            dx = x2 - x1
            dy = y2 - y1

            # Calculate error
            error = int(dx / 2.0)
            ystep = 1 if y1 < y2 else -1

            # Iterate over bounding box generating points between start and end
            y = y1
            points = []
            for x in range(int(x1), int(x2) + 1):
                coord = [y, x] if is_steep else [x, y]
                points.append(coord)
                error -= abs(dy)
                if error < 0:
                    y += ystep
                    error += dx

            # Reverse the list if the coordinates were swapped
            if swapped:
                points.reverse()
            results.append(points)
        return results


if __name__ == '__main__':


    from entitites.agent import Agent
    agent = Agent(pos=(9, 9), id=1, view_radius=3)

    points = RayCaster(agent).get_fov_outline()

    def print_grid(grid_outline, rays, width, height, agent):
        size = max(width, height) + 1
        grid = [['.' for _ in range(size)] for _ in range(size)]
        for x, y in grid_outline:
            grid[int(y)][int(x)] = 'X'
        for x, y in rays:
            grid[int(y)][int(x)] = 'O'
        grid[agent.y][agent.x] = 'A'
        grid = [' '.join(row) for row in grid]
        return '\n'.join(grid)

    from time import sleep

    for i, ray in enumerate(RayCaster(agent).get_rays()):
        sleep(1)
        grid = print_grid(points, ray, 20, 20, agent)
        print(grid)





