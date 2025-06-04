import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

def show_loading_screen(screen):
    progress = 0

  
    logo = pg.image.load("logo.png")

    
    while progress < 100:
       
        progress += 1

       
        screen.fill((0, 0, 0))

        
        logo_rect = logo.get_rect()
        logo_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)  
        screen.blit(logo, logo_rect)

       
        loader_width = int(progress * WIDTH / 100)
        loader_rect = pg.Rect(0, HEIGHT // 2 + 300, loader_width, 20)
        pg.draw.rect(screen, (255, 255, 255), loader_rect)

        
        pg.display.flip()

       
        pg.time.delay(40)
class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()
    

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
       
        self.object_renderer.draw()
        self.weapon.draw()
       
        

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':

    game = Game()
    show_loading_screen(game.screen)
    game.run()
