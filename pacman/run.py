import os
import pickle
import pygame 
import neat
from text import Score
from tiles import TileCollection
from pellets import Pellet, PowerPellet, Fruit
from agent import Agent
from ghost import Blinky, Pinky, Inky, Clyde
from neat_utils import get_largest_checkpoint

SCREEN_SIZE = (720, 864)
BLACK = (0, 0, 0)

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.display = pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.background = pygame.Surface(SCREEN_SIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.surivalTime = 0 #TODO: implement in agent class
        self.score = Score(0, (SCREEN_SIZE[0] // 2, 50))

        # Load the tile collection
        self.tileCollection = TileCollection(os.path.join("pacman", "Assets", "Levels", "level1.txt"))

        # Set the portal tiles #TODO: create a function for this
        self.tileCollection.lookup_table[(24, 408)].portal = self.tileCollection.lookup_table[(672, 408)]
        self.tileCollection.lookup_table[(672, 408)].portal = self.tileCollection.lookup_table[(24, 408)]


        self.agent = Agent(self.tileCollection.lookup_table[(360, 624)]) 
        
        # Set the starting positions for the ghosts
        self.blinky = Blinky(self.tileCollection.lookup_table[(408, 384)])
        self.pinky = Pinky(self.tileCollection.lookup_table[(288, 384)])
        self.inky = Inky(self.tileCollection.lookup_table[(408, 432)])
        self.clyde = Clyde(self.tileCollection.lookup_table[(288, 432)])
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def get_game_state_inputs(self):
        # Create a dictionary to store game state information
        game_state = {}

        # Define a mapping of tile types to numerical values
        tile_type_mapping = {
            'empty': 0.0,
            'pellet': 1.0,
            'power_pellet': 2.0,
            'fruit': 3.0,
            'wall': 4.0,  
        }

        direction_mapping = {
            None : 0.0,
            'up': 1.0,
            'down': 2.0,
            'left': 3.0,
            'right': 4.0,
        }

        mode_mapping = {
            'chase': 0.0,
            'scatter': 1.0,
            'frightened': 2.0,
            'eaten': 3.0,
            'escape': 4.0,
        }

        # Retrieve relevant game state information and store it in the dictionary
        game_state["agent_position.x"] = int(self.agent.position.x)
        game_state["agent_position.y"] = int(self.agent.position.y)
        game_state["agent_direction"] = direction_mapping[self.agent.current_direction]

        # Get agent's tile neighbors using the mapping
        game_state["up_neighbor"] = tile_type_mapping[self.agent.tile.neighbors['up'].tile_type]
        game_state["down_neighbor"] = tile_type_mapping[self.agent.tile.neighbors['down'].tile_type]
        game_state["left_neighbor"] = tile_type_mapping[self.agent.tile.neighbors['left'].tile_type]
        game_state["right_neighbor"] = tile_type_mapping[self.agent.tile.neighbors['right'].tile_type]

        game_state['blinky_position.x'] = int(self.blinky.position.x)
        game_state['blinky_position.y'] = int(self.blinky.position.y)
        game_state["blinky_direction"] = direction_mapping[self.blinky.current_direction]
        game_state["blinky_mode"] = mode_mapping[self.blinky.mode]

        game_state["pinky_position.x"] = int(self.pinky.position.x)
        game_state["pinky_position.y"] = int(self.pinky.position.y)
        game_state["pinky_direction"] = direction_mapping[self.pinky.current_direction]
        game_state["pinky_mode"] = mode_mapping[self.pinky.mode]

        game_state["inky_position.x"] = int(self.inky.position.x)
        game_state["inky_position.y"] = int(self.inky.position.y)
        game_state["inky_direction"] = direction_mapping[self.inky.current_direction]
        game_state["inky_mode"] = mode_mapping[self.inky.mode]

        game_state["clyde_position.x"] = int(self.clyde.position.x)
        game_state["clyde_position.y"] = int(self.clyde.position.y)
        game_state["clyde_direction"] = direction_mapping[self.clyde.current_direction]
        game_state["clyde_mode"] = mode_mapping[self.clyde.mode]

        # Return the collected game state information as a list with numerical values
        game_state_values = list(game_state.values())
        return game_state_values


    def interpret_action_outputs(self, action_outputs):
        best_action_index = action_outputs.index(max(action_outputs))
        if best_action_index == 0:
            return 'up'
        elif best_action_index == 1:
            return 'down'
        elif best_action_index == 2:
            return 'left'
        elif best_action_index == 3:
            return 'right'
        else:
            return None

    def get_final_score(self):
        return(0.8 * self.agent.score) + (0.2 * self.agent.survival_time)

    def update(self, neural_network):
        delta_time = self.clock.tick(30) / 1000.0

        game_state_inputs = self.get_game_state_inputs()
        action_outputs = neural_network.activate(game_state_inputs) #mabey its the positon stuff
        agent_action = self.interpret_action_outputs(action_outputs)

        self.agent.update(agent_action, delta_time)

        for ghost in self.ghosts:
            ghost.update(delta_time, self.agent, self.tileCollection.lookup_table)

        self.handle_item_collisions(self.agent)
        self.manage_ghost_modes(delta_time, self.tileCollection.lookup_table)
        self.update_flashing_events(delta_time)
        self.check_events()
        self.render(self.screen)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def handle_item_collisions(self, agent):
        # First, check pellet collisions
        if isinstance(agent.tile.tile_item, Pellet) or isinstance(agent.tile.tile_item, Fruit):
            if not agent.tile.tile_item.is_eaten:
                    points = agent.tile.tile_item.points
                    agent.tile.tile_item.eat()
                    agent.score += points
                    self.score.addPoints(points)

        elif isinstance(agent.tile.tile_item, PowerPellet):
            if not agent.tile.tile_item.is_eaten:
                points = agent.tile.tile_item.points #TODO: set attribute name to 'item' instead of 'tile_item'
                agent.tile.tile_item.eat()
                agent.score += points #TODO: implement this eat() method
                self.score.addPoints(points)
                for ghost in self.ghosts:
                    ghost.mode = 'frightened'
                    ghost.speed = 50
                    ghost.timer = 0
        
        # Next, check ghost collisions
        for ghost in self.ghosts:
            if agent.tile == ghost.tile:
                ghost.timer = 0
                if ghost.mode == 'frightened':
                    ghost.mode = 'eaten'
                    ghost.can_pass_doors = True #TODO: rename this attribute to 'can_pass_gates'
                    ghost.speed = 125
                    agent.score += 200
                    self.score.addPoints(200)
                elif ghost.mode in ['escape', 'scatter', 'chase']: #TODO: look at escape mode may not be necessary
                    agent.lives -= 1
                    agent.resetPosition()
                    for ghost in self.ghosts:
                        ghost.resetPosition()
                        ghost.mode = 'escape'
                        ghost.can_pass_doors = True #TODO: if mode is escape or eaten, then can_pass_doors is True
                        ghost.timer = 0
                    if agent.lives == 0:
                        self.is_game_over() #TODO: implement this function
                          
    def manage_ghost_modes(self, delta_time, lookup_table): #TODO: randomize timer for scatter and chase modes
        for ghost in self.ghosts:
            if ghost.mode == 'chase':
                ghost.timer += delta_time
                if ghost.timer >= ghost.chase_timer_max:
                    ghost.timer -= ghost.chase_timer_max
                    ghost.mode = 'scatter'

            elif ghost.mode == 'scatter':
                ghost.timer += delta_time
                if ghost.timer >= ghost.scatter_timer_max:
                    ghost.timer -= ghost.scatter_timer_max
                    ghost.mode = 'chase'

            elif ghost.mode == 'frightened':
                ghost.timer += delta_time
                if ghost.timer >= ghost.frightened_timer_max:
                    ghost.timer -= ghost.frightened_timer_max
                    ghost.mode = 'chase'
                    ghost.speed = 100

            elif ghost.mode == 'eaten':
                if ghost.tile.tile_item is None:
                    ghost.timer += delta_time
                    if ghost.timer >= ghost.eaten_timer_max:
                        ghost.timer -= ghost.eaten_timer_max
                        ghost.can_pass_doors = True
                        ghost.mode = 'escape'

            elif ghost.mode == 'escape':
                if ghost.tile.tile_item is not None:
                    ghost.can_pass_doors = False
                    ghost.mode = 'chase'
                    ghost.speed = 100

    def update_flashing_events(self, delta_time):
        self.agent.flash(delta_time)
        for tile in self.tileCollection.lookup_table.values():
            if tile.tile_item and isinstance(tile.tile_item, PowerPellet):
                tile.tile_item.flash(delta_time)

    def render(self, screen):
        self.screen.blit(self.background, (0, 0))
        self.tileCollection.render(self.screen)
        self.score.render(self.screen)

        self.agent.render(self.screen)
        for ghost in self.ghosts:
            ghost.render(self.screen)

        pygame.display.update()

    def is_game_over(self):
        self.agent.is_dead = True
        return self.get_final_score()

def evaluate_genome(genome, config):
    for genome_id, genome in genome:
        neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        game_controller = GameController()
        game_controller.startGame()
        while not game_controller.agent.is_dead:
            game_controller.update(neural_network)

        game_score = game_controller.get_final_score()
        genome.fitness = game_score


'''def run(config):
    # To restore a checkpoint, use the following code:
    # population = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")

    checkpoint_dir = "Check_Points"  # Change this to the directory where your checkpoint files are located
    largest_checkpoint_file = get_largest_checkpoint(checkpoint_dir)

    if largest_checkpoint_file is not None:
        population = neat.Checkpointer.restore_checkpoint(largest_checkpoint_file)
    else:
        population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Specify the full path to the checkpoint directory
    checkpoint_dir_path = os.path.join(os.path.dirname(__file__), checkpoint_dir)
    checkpoint_saver = neat.Checkpointer(generation_interval=1, time_interval_seconds=None,
                                         filename_prefix=os.path.join(checkpoint_dir_path, "neat-checkpoint-"))

    population.add_reporter(checkpoint_saver)

    winner = population.run(evaluate_genome, 100)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)'''

def run(config):

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)


    winner = population.run(evaluate_genome, 100)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                            config_path)
    run(config)
