import math
import itertools
import numpy as np


class RayCaster:
    def __init__(self, agent):
        self.agent = agent

    def visible_entities(self, entities):
        visible = []
        for ray in self.get_rays():
            rx, ry = ray[0]
            for x, y in ray:  # important to exclude own coordinates
                cx, cy = x - rx, y - ry
                try:
                    hits = entities[(x, y)]
                    diag_hits = all(self.are_blocking(entities[(x, y-cy)] + entities[(x-cx, y)])) \
                        if (cx != 0 and cy != 0) else False
                    visible += hits if not diag_hits else []
                    if any(self.are_blocking(hits)) or diag_hits:
                        break  # todo use hooks, e.g. to see through open doors!
                except KeyError as e:
                    pass
                rx, ry = x, y
        return visible

    def are_blocking(self, entities):
        return [e.blocks_ray for e in entities]

    def get_rays(self):
        outline = self.get_fov_outline(np.array([0, -1]), degs=360, discretize=True).astype(int)
        return [self.bresenham(start=self.agent.pos, end=p) for p in outline]

    # todo do this once and cache the points!
    def get_fov_outline(self, move_vec, degs=90, discretize=True) -> np.ndarray:
        points = [self.rot(move_vec*self.agent.view_radius, deg) + self.agent._pos_np \
                  for deg in np.linspace(-degs // 2, degs // 2, 100)[::-1]]
        if discretize:
            rounded_points = np.round(points)
            _, ind = np.unique(rounded_points, axis=0, return_index=True)
            return rounded_points[np.sort(ind)]

        return np.array(points)

    def get_square_outline(self):
        agent = self.agent
        x_coords = range(agent.x - agent.view_radius, agent.x + agent.view_radius + 1)
        y_coords = range(agent.y - agent.view_radius, agent.y + agent.view_radius + 1)
        outline = list(itertools.product(x_coords, [agent.y - agent.view_radius, agent.y + agent.view_radius])) \
                  + list(itertools.product([agent.x - agent.view_radius, agent.x + agent.view_radius], y_coords))
        return outline

    def get_circle_outline(self):
        x, y = self.agent.view_radius, 0
        decision_over2 = 1 - x
        points = []
        while x >= y:
            points += [(self.agent.x + x, self.agent.y + y) for x, y in
                       ((x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x))]
            y += 1
            if decision_over2 <= 0:
                decision_over2 += 2 * y + 1
            else:
                x -= 1
                decision_over2 += 2 * (y - x) + 1
        return points

    @classmethod
    def rot(cls, v, deg):
        theta = np.deg2rad(deg)
        M = np.array([[math.cos(theta), -math.sin(theta)],
                      [math.sin(theta), math.cos(theta)]])
        return np.dot(M, v)

    @classmethod
    def bresenham(cls, start, end):
        # Setup initial conditions
        x1, y1 = start
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
        return np.array(points)


if __name__ == '__main__':

    from entitites.agent import Agent
    agent = Agent(pos=(4, 6), id=1, view_radius=4)

    s, e = np.array([3, 0]), np.array([6, 7])
    lines = RayCaster.bresenham(s, e)

    points = RayCaster(agent).get_fov_outline(move_vec=Agent.NORTH, degs=360)

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




    print_grid(points, [], 10, 10, agent)

    from time import sleep
    from tqdm import trange
    import sys

    square = RayCaster(agent).get_circle_outline()
    grid = print_grid(square, [], 10, 10, agent)
    print(grid)


    for i, ray in enumerate(RayCaster(agent).get_rays()):
        sleep(1)
        grid = print_grid(points, ray, 10, 10, agent)
        print(grid)





