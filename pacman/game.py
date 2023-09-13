import pygame, sys, random
from constants import *
from tiles import TileCollection
from pacman import Pacman
from ghost import Blinky, Pinky, Inky, Clyde
from items import *
from text import Score

class GameController(object):
    '''
    A class that controls the game loop and game state
    '''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.max_phase_intervals = {
            'scatter' : (7, 10),
            'chase' : (7, 10),
        }
    
    def set_background(self):
        '''Sets the background of the screen'''
        self.background = pygame.Surface(SCREEN_SIZE).convert()
        self.screen.fill(BLACK)

    def start(self):
        '''Starts the game'''
        self.set_background()
        self.phase = SCATTER
        self.phase_timer, self.phase_interval = 0, random.randint(*self.max_phase_intervals[self.phase])
        self.tiles = TileCollection()
        self.special_items = [Cherry, Strawberry, Orange, Apple, Pretzel, GalaxianFlagship, Bell, Key]
        self.pacman = Pacman(self.tiles.get_tile(14, 26))
        self.blinky = Blinky(self.tiles.get_tile(16, 16))
        self.pinky = Pinky(self.tiles.get_tile(11, 16))
        self.inky = Inky(self.tiles.get_tile(16, 18))
        self.clyde = Clyde(self.tiles.get_tile(11, 18))
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        self.score = Score((SCREEN_WIDTH // 2, 25))

    def update(self):
        '''Updates the game state'''
        delta_time = self.clock.tick(60) / 1000.0
        self.pacman.update(delta_time)
        for ghost in self.ghosts:
            ghost.update(delta_time, self.pacman, self.tiles.look_up_table)
        self.check_collisions()
        self.score.update(self.pacman.score)
        self.update_game_phase(delta_time)
        self.update_ghosts_phase(delta_time)
        self.handle_flashing_events(delta_time)
        self.spawn_special_item()
        if self.pacman.lives == 0:
            pygame.quit()
        self.check_events()

    def spawn_special_item(self):
        '''Selects a random tile and spawns an item on it'''
        if len(self.pacman.collected_items) % 38 == 0 and self.tiles.unique_item is None:
            if len(self.special_items) == 0:
                return
            empty_tiles = []
            for tile in self.tiles.look_up_table.values():
                if tile.type == PATH and tile.item in self.pacman.collected_items:
                    empty_tiles.append(tile)
            if empty_tiles:
                random_tile = random.choice(empty_tiles)
                item = self.special_items.pop(0)(random_tile.position.as_tuple())
                self.tiles.unique_item = item
                self.tiles.items.append(item)
                random_tile.item = item
             
    def check_events(self):
        '''Checks for events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def check_collisions(self):
        '''Checks for collisions'''
        pacman = self.pacman 
        for item in self.tiles.items:
            distance_to_pacman = item.position.distance(pacman.position)
            
            if distance_to_pacman <= item.collision_radius and not item.collected:
                item.collected = True
                item.is_visible = False
                pacman.score += item.POINTS
                
                if item.name in ['pellet', 'power_pellet']:
                    pacman.collected_items.append(item)
                    if item.name == 'power_pellet':
                        for ghost in self.ghosts:
                            if ghost.phase not in [EATEN, LEAVE_GHOST_HOUSE]:
                                ghost.phase = FRIGHTENED
                                ghost.speed = 50
                                ghost.elapsed_time = 0

                elif item.name in ['cherry', 'strawberry', 'orange', 'apple', 'pretzel', 'galaxian_flagship', 'bell', 'key']:
                    pacman.special_items.append(item)
                    self.tiles.unique_item = None

        for ghost in self.ghosts:
            if ghost.position.distance(self.pacman.position) <= ghost.collision_radius:
                if ghost.phase == FRIGHTENED:
                    ghost.phase = EATEN
                    ghost.speed = 150
                    ghost.elapsed_time = 0
                    pacman.score += 200
                elif ghost.phase == CHASE or ghost.phase == SCATTER:
                    self.pacman.lives -= 1
                    self.pacman.reset_position()
                    for ghost in self.ghosts:
                        ghost.reset()
                        ghost.phase = LEAVE_GHOST_HOUSE
                    self.phase_timer = 0
                    self.phase_interval = random.randint(*self.max_phase_intervals[self.phase])        

    def switch_phase(self):
        '''Switches the phase'''
        if self.phase == SCATTER:
            self.phase = CHASE
        elif self.phase == CHASE:
            self.phase = SCATTER
        self.phase_interval = random.randint(*self.max_phase_intervals[self.phase])
        self.phase_timer = 0

    def update_game_phase(self, delta_time: float):
        self.phase_timer += delta_time  
        if self.phase_timer >= self.phase_interval:
            self.switch_phase()

    def update_ghosts_phase(self, delta_time: float):
        '''Updates the phase of the ghosts'''
        for ghost in self.ghosts:
            if ghost.phase == FRIGHTENED:
                ghost.elapsed_time += delta_time
                if ghost.elapsed_time >= 7:
                    ghost.phase = CHASE
                    ghost.elapsed_time = 0
                    ghost.speed = 75
            elif ghost.phase == EATEN:
                if ghost.tile.type == GHOST_HOUSE:
                    ghost.elapsed_time += delta_time
                    if ghost.elapsed_time >= 3:
                        ghost.phase = LEAVE_GHOST_HOUSE
                        ghost.elapsed_time = 0
                        ghost.speed = 75
            elif ghost.phase == LEAVE_GHOST_HOUSE:
                if ghost.tile.type == PATH:
                    ghost.phase = SCATTER
                    ghost.speed = 75
                    ghost.elapsed_time = 0

            if self.phase == CHASE:
                if ghost.phase == SCATTER:
                    ghost.phase = CHASE
                    ghost.speed = 75
            elif self.phase == SCATTER:
                if ghost.phase == CHASE:
                    ghost.phase = SCATTER
                    ghost.speed = 75

    def handle_flashing_events(self, delta_time: float):
        for power_pellet in self.tiles.power_pellets:
            power_pellet.flash(delta_time)

    def render(self):
        '''Renders the game'''
        self.screen.blit(self.background, (0, 0))
        self.tiles.render(self.screen)
        self.pacman.render(self.screen)
        self.score.render(self.screen)
        for ghost in self.ghosts:
            ghost.render(self.screen)
        pygame.display.update()

    def game_over(self):
        '''Ends the game'''
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = GameController()
    game.start()
    while True:
        game.update()
        game.render()
