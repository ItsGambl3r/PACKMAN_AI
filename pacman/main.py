import math
import os
import numpy as np
from neat.math_util import softmax

import pygame, sys, time, random, neat

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 100000

# Window size
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# Score
def show_score(win, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (int(WINDOW_WIDTH / 10), int(15))
    else:
        score_rect.midtop = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 1.25))
    win.blit(score_surface, score_rect)
    # pygame.display.flip()


def wallCollide(snake_pos):
    if snake_pos[0] < 0 or snake_pos[0] > WINDOW_WIDTH - 10:
        return True
    if snake_pos[1] < 0 or snake_pos[1] > WINDOW_HEIGHT - 10:
        return True


def bodyCollide(snake_body, snake_pos):
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            return True


def withinRadiusOfFood(snake_pos, food_pos):
    return math.sqrt((snake_pos[0] - food_pos[0]) ** 2 + (snake_pos[1] - food_pos[1]) ** 2)


def getDistances(win, snake_pos, snake_body, food_pos):
    pos = []
    directions = ['NORTH', 'SOUTH', 'WEST', 'EAST', 'NORTHWEST', 'NORTHEAST', 'SOUTHWEST', 'SOUTHEAST']
    distances = []
    for mode in range(3):
        for x, direction in enumerate(directions):
            distance = 0
            pos.clear()
            pos.append(snake_pos[0])
            pos.append(snake_pos[1])
            while not wallCollide(pos):
                if direction == 'NORTH':
                    pos[1] -= 10
                elif direction == 'SOUTH':
                    pos[1] += 10
                elif direction == 'WEST':
                    pos[0] -= 10
                elif direction == 'EAST':
                    pos[0] += 10
                elif direction == 'NORTHWEST':
                    pos[1] -= 10
                    pos[0] -= 10
                elif direction == 'NORTHEAST':
                    pos[1] -= 10
                    pos[0] += 10
                elif direction == 'SOUTHWEST':
                    pos[1] += 10
                    pos[0] -= 10
                elif direction == 'SOUTHEAST':
                    pos[1] += 10
                    pos[0] += 10
                if withinRadiusOfFood(snake_pos, food_pos) == 0 and mode == 1:
                    break
                if bodyCollide(snake_body, pos) and mode == 2:
                    break
                # if mode == 1:
                #     pygame.draw.rect(win, green, pygame.Rect(pos[0], pos[1], 10, 10))
                # pygame.display.update()
                distance += 1
            distances.append(distance)

    return distances


def main(genomes, config):
    global score, WINDOW_HEIGHT, WINDOW_WIDTH, black, white, red, green, blue, difficulty

    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    # Checks for errors encountered
    check_errors = pygame.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        quit(-1)
    else:
        print('[+] Game successfully initialised')

    # Initialise game window
    pygame.display.set_caption('Snake Eater')
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    for x, g in enumerate(ge):
        # Main logic

        # FPS (frames per second) controller
        fps_controller = pygame.time.Clock()

        # Game variables
        snake_pos = [100, 50]
        snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

        food_pos = [random.randrange(1, (WINDOW_WIDTH // 10)) * 10, random.randrange(1, (WINDOW_HEIGHT // 10)) * 10]
        food_spawn = True

        direction = 'RIGHT'
        change_to = direction

        score = 0
        running = True
        ticks = 0
        max_ticks = 500
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            inputs = getDistances(win, snake_pos, snake_body, food_pos)
            net_output = nets[x].activate(inputs)
            softmax_result = softmax(net_output)
            index = softmax_result.index(max(softmax_result))

            if index == 0:
                change_to = 'UP'
            elif index == 1:
                change_to = 'DOWN'
            elif index == 2:
                change_to = 'LEFT'
            elif index == 3:
                change_to = 'RIGHT'

            # Making sure the snake cannot move in the opposite direction instantaneously
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                snake_pos[1] -= 10
            if direction == 'DOWN':
                snake_pos[1] += 10
            if direction == 'LEFT':
                snake_pos[0] -= 10
            if direction == 'RIGHT':
                snake_pos[0] += 10
            # Snake body growing mechanism
            snake_body.insert(0, list(snake_pos))

            if withinRadiusOfFood(snake_pos, food_pos) == 0:
                score += 1
                print("Scored!")
                g.fitness += 5
                max_ticks += 300
                food_spawn = False
            elif withinRadiusOfFood(snake_pos, food_pos) < 1:
                g.fitness += 0.1
            elif withinRadiusOfFood(snake_pos, food_pos) < 2:
                g.fitness += 0.05
            else:
                g.fitness -= 0.01
                snake_body.pop()

            # Spawning food on the screen
            if not food_spawn:
                food_pos = [random.randrange(1, (WINDOW_WIDTH // 10)) * 10,
                            random.randrange(1, (WINDOW_HEIGHT // 10)) * 10]
            food_spawn = True

            # GFX
            win.fill(black)
            for pos in snake_body:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                pygame.draw.rect(win, red, pygame.Rect(pos[0], pos[1], 10, 10))

            # Snake food
            pygame.draw.rect(win, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

            # Game Over conditions
            # Getting out of bounds

            if wallCollide(snake_pos):
                g.fitness -= 5
                running = False
            # Touching the snake body
            if bodyCollide(snake_body, snake_pos):
                g.fitness -= 5
                running = False

            show_score(win, 1, white, 'consolas', 20)
            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            fps_controller.tick(difficulty)
            if ticks > max_ticks:
                running = False
            ticks += 1


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main, 1000)
    print('\nBest genome:\n{!s}'.format(winner))
    print("Pop Size: " + str(len(pop.population)))

    pygame.quit()
    quit()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)