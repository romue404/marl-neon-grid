from marl_neon_grid.rendering.render_groups import AgentRenderGroup, WallRenderGroup, RenderGroup
from marl_neon_grid.entitites import Agent, Door, Zone, Wall, GameState, Food
from marl_neon_grid.rendering.base_renderer import BaseRenderer
from marl_neon_grid.ray_caster import RayCaster
import pygame


class Renderer(BaseRenderer):
    AGENT_VIEW_COLOR = (220, 220, 220)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, game_state: GameState):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

        wall_blits  =  WallRenderGroup(self, game_state.entities[Wall.SYMBOL]).blits()
        agent_blits =  AgentRenderGroup(self, game_state.entities[Agent.SYMBOL]).blits()
        door_blits  =  RenderGroup(self, game_state.entities[Door.SYMBOL]).blits()
        food_blits  =  RenderGroup(self, game_state.entities[Food.SYMBOL]).blits()
        zone_blits  =  RenderGroup(self, game_state.entities[Zone.SYMBOL]).blits()

        viz_entities = sum([list(set(RayCaster(a).visible_entities(game_state.entities))) for a in game_state.agents], [])

        self.fill_bg()

        for blit in wall_blits + zone_blits +\
                    door_blits + food_blits + \
                    self.visibility_rects(viz_entities) + agent_blits:
            self.screen.blit(**blit)

        pygame.display.flip()
        self.clock.tick(self.fps)

