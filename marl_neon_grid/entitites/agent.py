import numpy as np
import itertools
from marl_neon_grid.entitites.entity import DynamicEntity


class Agent(DynamicEntity):
    SYMBOL = 'A'

    def __init__(self, *args, id, view_radius=2, **kwargs):
        super().__init__(*args, **kwargs)
        #self.SYMBOL = f'A{id}'
        self.view_radius = view_radius
        self.id = id

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return f'{self.__class__.__name__}{self.id}@{self._pos_np}'

    @property
    def observable_coords(self):
        xy = itertools.product(range(-self.view_radius, self.view_radius+1),
                               range(-self.view_radius, self.view_radius+1))
        return self._pos_np + np.array(list(xy))





