import sys
from pathlib import Path
import pygame


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

        #self.fill_bg()
        self.font = pygame.font.Font(None, 20)
        self.font.set_bold(True)

    @classmethod
    def quit(cls):
        pygame.quit()
        sys.exit()

    def fill_bg(self):
        self.screen.fill(self.BLACK)
        w, h = self.screen_size
        for x in range(self.cell_size, w-self.cell_size, self.cell_size):
            for y in range(self.cell_size, h-self.cell_size, self.cell_size):
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

    def render(self, game_state):
        pass