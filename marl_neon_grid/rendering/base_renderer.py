import sys
from pathlib import Path
import pygame
from functools import singledispatchmethod
from marl_neon_grid.entitites import Agent, Door, Floor, Wall


class BaseRenderer:
    BG_COLOR = (178, 190, 195)         # (99, 110, 114)
    WHITE = (233, 60, 172)  # (200, 200, 200)
    AGENT_VIEW_COLOR = (255, 249, 166)
    BLACK = (75, 54, 95)
    ASSETS = Path(__file__).parent / 'assets'

    def __init__(self,
                 lvl_shape=(16, 16),
                 lvl_padded_shape=None,
                 cell_size=60,
                 fps=7,
                 view_radius=2):
        self.grid_h, self.grid_w = lvl_shape
        self.lvl_padded_shape = lvl_padded_shape if lvl_padded_shape is not None else lvl_shape
        self.cell_size = cell_size
        self.fps = fps
        self.view_radius = view_radius
        self.screen_size = (self.grid_w*cell_size, self.grid_h*cell_size)

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        pygame.init()
        self.assets = {path.stem: self.load_asset(str(path), 1) for path in self.ASSETS.rglob('*.png')}

        self.fill_bg()
        self.font = pygame.font.Font(None, 20)
        self.font.set_bold(True)

    @classmethod
    def quit(cls):
        pygame.quit()
        sys.exit()

    def fill_bg(self):
        self.screen.fill(self.BLACK)
        w, h = self.screen_size
        for x in range(0, w, self.cell_size):
            for y in range(0, h, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, BaseRenderer.WHITE, rect, 1)

    def get_xy(self, entity):
        offset_r, offset_c = (self.lvl_padded_shape[0] - self.grid_h) // 2, \
                             (self.lvl_padded_shape[1] - self.grid_w) // 2

        r, c = entity.pos
        r, c = r - offset_r, c - offset_c

        o = self.cell_size // 2
        r_, c_ = r * self.cell_size + o, c * self.cell_size + o
        return r_, c_

    def load_asset(self, path, factor=1.0):
        scale = int(factor*self.cell_size)
        asset = pygame.image.load(path).convert_alpha()
        asset = pygame.transform.smoothscale(asset, (scale, scale))
        return asset

    def visibility_rects(self, entities):
        rects = []
        for e in entities:
            rect = pygame.Rect((0, 0), (self.cell_size, self.cell_size))
            rect.centerx, rect.centery = self.get_xy(e)
            shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, self.AGENT_VIEW_COLOR, shape_surf.get_rect())
            shape_surf.set_alpha(64)
            rects.append(dict(source=shape_surf, dest=rect))
        return rects

    @singledispatchmethod
    def blit_params(self, entity):
        blits = []
        name = f'{entity.__class__.__name__.lower()}_{entity.state}'.rstrip('_')
        img = self.assets[name]
        rect = img.get_rect()
        rect.centerx, rect.centery = self.get_xy(entity)
        blits.append(dict(source=img, dest=rect))

        if hasattr(entity, 'id'):
            textsurface = self.font.render(str(entity.id), False, (0, 0, 0))
            text_blit = dict(source=textsurface, dest=(rect.center[0] - .07 * self.cell_size,
                                                       rect.center[1]))
            blits.append(text_blit)

        return blits

    @blit_params.register
    def blit_params_list(self, entities: list):
        return sum([self.blit_params(e) for e in entities], [])

    def render(self, game_state, order):
        pass