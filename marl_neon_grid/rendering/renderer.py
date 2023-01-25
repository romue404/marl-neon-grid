import numpy as np
from marl_neon_grid.rendering.base_renderer import BaseRenderer
from functools import singledispatchmethod
from marl_neon_grid.entitites import Agent, Door, Floor, Wall, GameState
from marl_neon_grid.rendering.base_renderer import BaseRenderer
from marl_neon_grid.ray_caster import RayCaster
import pygame


class Renderer(BaseRenderer):
    DEFAULT_ORDER = ('#', 'D', 'V', 'A')
    AGENT_VIEW_COLOR = (243, 230, 0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @singledispatchmethod
    def blit_params(self, entity):
        return super().blit_params(entity)

    @blit_params.register
    def blit_params_wall(self, wall: Wall):
        inner =  1 <= wall.y < self.grid_h - 1
        img = self.assets['wall']
        if wall.x == 0 and inner:
            img = pygame.transform.rotate(img, 90)
        elif wall.x == self.grid_w - 1 and inner:
            img = pygame.transform.rotate(img, -90)
        rect = img.get_rect()
        rect.centerx, rect.centery = self.get_xy(wall)
        return [dict(source=img, dest=rect)]

    @blit_params.register
    def blit_params_floor(self, floor: Floor):
        return []

    def render(self, game_state: GameState, order=DEFAULT_ORDER):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        viz_symbol = 'V'

        blits = [self.blit_params(game_state.entities[symbol]) for symbol in order if symbol != viz_symbol]
        viz_entities = sum([list(set(RayCaster(a).visible_entities(game_state.entities))) for a in game_state.agents], [])
        blits.insert(order.index(viz_symbol), self.visibility_rects(viz_entities))

        self.fill_bg()

        for blit in sum(blits, []):
            self.screen.blit(**blit)

        pygame.display.flip()
        self.clock.tick(self.fps)

