from marl_neon_grid.entitites.entity import Entity


class Zone(Entity):
    SYMBOL = 'Z'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)