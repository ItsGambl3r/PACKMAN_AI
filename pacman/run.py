import pygame, sys, random, pickle, neat, os
from pygame.locals import *
from constants import *
from tiles import TileCollection
from agent import Agent
from ghost import Blinky, Pinky, Inky, Clyde
from items import *
from text import Score
from neat_utils import get_largest_checkpoint

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
            'chase' : (2, 5),
        }
    
    def set_background(self):
        '''Sets the background of the screen'''
        self.background = pygame.Surface(SCREEN_SIZE).convert()
        self.screen.fill(BLACK)

    def start(self, genomes, config):
        '''Starts the game'''
        self.set_background()
        self.phase = SCATTER
        self.phase_timer, self.phase_interval = 0, random.randint(*self.max_phase_intervals[self.phase])
        self.tiles = TileCollection()
        self.special_items = [Cherry, Strawberry, Orange, Apple, Pretzel, GalaxianFlagship, Bell, Key]
        self.score = Score((SCREEN_WIDTH // 2, 25))
        self.high_score = Score((SCREEN_WIDTH // 2, 25))

        self.agents = []
        self.agent_ghost_pairs = {}

        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            agent = Agent(self.tiles.get_tile(14, 26), net)
            self.agents.append(agent)
            self.agent_ghost_pairs[agent] = {
                'blinky' : Blinky(self.tiles.get_tile(16, 16)),
                'pinky' : Pinky(self.tiles.get_tile(11, 16)),
                'inky' : Inky(self.tiles.get_tile(16, 18)),
                'clyde' : Clyde(self.tiles.get_tile(11, 18))
            }
            self.alive_agents = len(self.agents)
            
            self.best_agent = self.find_best_agent()

        self.show_best_agent = False
    
    def find_best_agent(self):
        '''Finds the best agent'''

        highest_score = 0
        best_agent = None

        # Iterate through all the agents
        for agent in self.agents:
            # Check if the agent has a higher score than the current highest score
            # and if the agent is alive
            if agent.score > highest_score and agent.alive:
                # Update the highest score and set the best_agent to this agent
                highest_score = agent.score
                best_agent = agent

            # Check if the agent's score is higher than the overall high score
            if agent.score > self.high_score.score:
                # Update the overall high score
                self.high_score.score = agent.score

        # Set self.best_agent to the best_agent found in the loop
        self.best_agent = best_agent


    def get_game_state(self, agent):
        """Get the game state information for a given agent.

        Args:
            agent: The agent for which to retrieve the game state.

        Returns:
            game_state: A list containing the game state information.
        """
        # Define a dictionary to map constants to numerical values
        constants_dict = {
            UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3, SCATTER: 4,
            CHASE: 5, FRIGHTENED: 6, EATEN: 7, LEAVE_GHOST_HOUSE: 8,
            EMPTY: 9, WALL: 10, GHOST_DOOR: 11, GHOST_HOUSE: 12,
            None: 13
        }

        # Initialize the game state list
        game_state = []

        # Add information about the game phase
        game_state.append(constants_dict[self.phase])

        # Get the agent's position and add it to the game state
        agent_position = agent.position.as_tuple()
        game_state.append(int(agent_position[0]))
        game_state.append(int(agent_position[1]))

        # Add the agent's current direction, idle timer, score, and lives
        game_state.append(constants_dict[agent.current_direction])
        game_state.append(int(agent.idle_timer))
        game_state.append(agent.score)
        game_state.append(agent.lives)

        for direction in [UP, DOWN, LEFT, RIGHT]:
            try:
                if agent.can_move_in_direction(direction):
                    game_state.append(1)
                else:
                    game_state.append(0)
            except:
                game_state.append(0)

        # Iterate over the ghosts associated with the agent
        for ghost in self.agent_ghost_pairs[agent].values():    
            # Get the ghost's position and add it to the game state
            ghost_position = ghost.position.as_tuple()
            game_state.append(int(ghost_position[0]))
            game_state.append(int(ghost_position[1]))

            # Add the distance between the agent and the ghost
            game_state.append(int(agent.position.distance(ghost.position)))

            # Add the ghost's current direction and phase
            game_state.append(constants_dict[ghost.current_direction])
            game_state.append(constants_dict[ghost.phase])

        # Return the populated game state list
        return game_state

    def interpret_action(self, action_outputs):
        """_summary_

        Args:
            action_outputs (_type_): _description_
        """
        best_action = action_outputs.index(max(action_outputs))
        if best_action == 0:
            return UP
        elif best_action == 1:
            return DOWN
        elif best_action == 2:
            return LEFT
        elif best_action == 3:
            return RIGHT
        else:
            raise ValueError('Invalid action output')
        
    def get_fitness(self, agent):
        '''Returns the fitness of the agent'''
        return agent.score
    
    def update(self):
        '''Updates the game state'''
        delta_time = self.clock.tick(60) / 1000.0
        for agent in self.agents:
            if agent.alive:
                game_state = self.get_game_state(agent)
                action_outputs = agent.neural_network.activate(game_state)
                direction = self.interpret_action(action_outputs)
                agent.update(direction, delta_time)
                for ghost in self.agent_ghost_pairs[agent].values():
                    ghost.update(delta_time, agent, self.tiles.look_up_table)
                self.check_collisions(agent)
                self.score.update(agent)
                self.update_game_phase(delta_time)
                self.update_ghosts_phase(agent, delta_time)
                if agent.is_idle:
                    agent.alive = False
        self.check_alive_agents()
        self.handle_flashing_events(delta_time)
        self.find_best_agent()
        try:
            self.score.update(self.best_agent.score)
        except:
            self.score.update(0)
        self.high_score.text = 'HIGH SCORE: ' + str(self.high_score.score)
        self.check_events()
        # print(self.high_score.score, self.best_agent.score)

    def check_events(self):
        '''Checks for events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.show_best_agent = not self.show_best_agent

    def spawn_special_item(self):
        '''Selects a random tile and spawns an item on it'''
        raise NotImplementedError
        '''if len(self.pacman.collected_items) % 38 == 0 and self.tiles.unique_item is None:
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
                random_tile.item = item'''
        
    def check_collisions(self, agent):
        for item in self.tiles.items:
            distance_to_agent = agent.position.distance(item.position)

            if distance_to_agent <= item.collision_radius and item not in agent.collected_items:
                agent.collected_items.append(item)
                agent.score += item.POINTS

                if item.name == 'power_pellet':
                    for ghost in self.agent_ghost_pairs[agent].values():
                        if ghost.phase not in [EATEN, LEAVE_GHOST_HOUSE]:
                            ghost.phase = FRIGHTENED
                            ghost.speed = 50
                            ghost.elapsed_time = 0

            for ghost in self.agent_ghost_pairs[agent].values():
                if ghost.position.distance(agent.position) <= ghost.collision_radius:
                    if ghost.phase == FRIGHTENED:
                        ghost.phase = EATEN
                        ghost.speed = 150
                        ghost.elapsed_time = 0
                        agent.score += 200
                    elif ghost.phase == CHASE or ghost.phase == SCATTER:
                        agent.lives -= 1
                        agent.reset_position()
                        for ghost in self.agent_ghost_pairs[agent].values():
                            ghost.reset()
                            ghost.phase = LEAVE_GHOST_HOUSE
                        return   

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

    def update_ghosts_phase(self, agent, delta_time: float):
        '''Updates the phase of the ghosts'''
        for ghost in self.agent_ghost_pairs[agent].values():
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

    def handle_flashing_events(self, delta_time: float):
        for power_pellet in self.tiles.power_pellets:
            power_pellet.flash(delta_time)

    def check_alive_agents(self):
        '''Checks if there are any alive agents'''
        self.alive_agents = 0
        for agent in self.agents:
            if agent.alive:
                self.alive_agents += 1

    def render(self):
        '''Renders the game state'''
        if self.show_best_agent or self.alive_agents == 1:
            if self.best_agent is None:
                return
            for tile in self.tiles.look_up_table.values():
                if tile.item in self.best_agent.collected_items:
                    tile.render(self.screen, False)
                else:
                    tile.render(self.screen, True)
            self.best_agent.render(self.screen)

            for ghost in self.agent_ghost_pairs[self.best_agent].values():
                ghost.render(self.screen)
            self.score.render(self.screen)
        else:
            self.screen.blit(self.background, (0, 0))
            self.tiles.render(self.screen)
            for agent in self.agents:
                if agent.alive:
                    for ghost in self.agent_ghost_pairs[agent].values():
                        ghost.render(self.screen)
                    agent.render(self.screen)
            self.high_score.render(self.screen)
            # self.high_score.render(self.screen)
        
        pygame.display.update()

    def is_game_over(self):
        '''Returns True if the game is over'''
        return all([not agent.alive for agent in self.agents])

    # ------------------ NEAT ------------------ #
def eval_genomes(genomes, config):
    '''Evaluates the genomes'''
    game_controller = GameController()
    game_controller.start(genomes, config)
    while not game_controller.is_game_over():
        game_controller.update()
        game_controller.render()

    for genome_id, genome in genomes:
        for agent in game_controller.agents:
            if agent.neural_network is genome:
                genome.fitness = game_controller.get_fitness(agent)


def run(config_file):
    '''Runs the NEAT algorithm'''
    checkpoint_dir = os.path.join(os.getcwd(), 'checkpoints')
    larget_checkpoint = get_largest_checkpoint(checkpoint_dir)

    if larget_checkpoint is not None:
        p = neat.Checkpointer.restore_checkpoint(larget_checkpoint)
    else:
        p = neat.Population(config_file)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    checkpoint_dir_path = os.path.join(os.getcwd(), 'checkpoints')
    checkpoint_saver = neat.Checkpointer(generation_interval=1, time_interval_seconds=None, filename_prefix=checkpoint_dir_path + '/neat-checkpoint-')

    p.add_reporter(checkpoint_saver)

    winner = p.run(eval_genomes, 1000)
    with open(os.path.join(checkpoint_dir_path, 'winner.pkl'), 'wb') as output:
        pickle.dump(winner, output, 1)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    run(config)




    



  

        







