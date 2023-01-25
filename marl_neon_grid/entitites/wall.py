from marl_neon_grid.entitites.entity import Entity


class Wall(Entity):
    SYMBOL = '#'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._blocks_ray = True