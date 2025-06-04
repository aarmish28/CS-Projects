import pygame as pg
import math
from settings import *
WIDTH = 800
HEIGHT = 600

# Define constants for the fire animation
FIRE_WIDTH = 50
FIRE_HEIGHT = 50
FIRE_ANIMATION_SPEED = 0.1

class FireAnimation:
    def __init__(self):
        self.fire_images = []  # List to store the fire animation frames
        self.current_frame = 0  # Index of the current frame
        self.frame_timer = 0.0  # Timer to control the frame rate

        # Load the fire animation frames from image files
        for i in range(10):
            image = pg.image.load(f"fire_frame_{1}.png")
            image = pg.transform.scale(image, (FIRE_WIDTH, FIRE_HEIGHT))
            self.fire_images.append(image)

    def update(self, dt):
        self.frame_timer += dt

        # Check if it's time to switch to the next frame
        if self.frame_timer >= FIRE_ANIMATION_SPEED:
            self.frame_timer -= FIRE_ANIMATION_SPEED
            self.current_frame = (self.current_frame + 1) % len(self.fire_images)

    def render(self, surface, x, y):
        image = self.fire_images[self.current_frame]
        surface.blit(image, (x, y))

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures
        self.fire_animation = FireAnimation()

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
        dt = pg.time.Clock().tick(60) / 1000.0
        self.fire_animation.update(dt)

    def render(self, surface):
        # Render the fire animation in the background
        fire_x = 0  # Adjust the x-coordinate as needed
        fire_y = 0  # Adjust the y-coordinate as needed
        self.fire_animation.render(surface, fire_x, fire_y)

        # Render the objects to render (walls, etc.) on top of the fire animation
        for depth, wall_column, wall_pos in self.objects_to_render:
            surface.blit(wall_column, wall_pos)