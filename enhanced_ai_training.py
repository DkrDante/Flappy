import pygame
import random
import os
import time
import neat
import visualize
import pickle
import json

pygame.font.init()

WIN_WIDTH = 800  # Wider window for more info
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 30)
BIG_FONT = pygame.font.SysFont("comicsans", 50)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Enhanced Flappy Bird AI Training")

pipe_img = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha()
)
bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (800, 900)
)
bird_images = [
    pygame.transform.scale2x(
        pygame.image.load(os.path.join("imgs", "bird" + str(x) + ".png"))
    )
    for x in range(1, 4)
]
base_img = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha()
)

gen = 0
ai_high_score = 0
training_stats = {
    "generations": [],
    "best_fitness": [],
    "avg_fitness": [],
    "species_count": []
}

def load_ai_high_score():
    global ai_high_score
    try:
        with open("ai_high_score.txt", "r") as f:
            ai_high_score = int(f.read())
    except:
        ai_high_score = 0

def save_ai_high_score():
    global ai_high_score
    with open("ai_high_score.txt", "w") as f:
        f.write(str(ai_high_score))

def save_training_stats():
    with open("training_stats.json", "w") as f:
        json.dump(training_stats, f, indent=2)

class Bird:
    MAX_ROTATION = 25
    IMGS = bird_images
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.alive_time = 0
        self.pipes_passed = 0

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        self.alive_time += 1

        displacement = self.vel * (self.tick_count) + 0.5 * (3) * (self.tick_count) ** 2

        if displacement >= 16:
            displacement = (displacement / abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    def __init__(self, x, difficulty=1):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img
        self.passed = False
        self.difficulty = difficulty
        
        # Dynamic gap based on difficulty
        self.gap = max(200, 300 - (difficulty - 1) * 10)
        self.vel = 5 + (difficulty - 1) * 0.5
        
        self.set_height()

    def set_height(self):
        # Easier height range for early learning
        min_height = max(50, 150 - (self.difficulty - 1) * 20)
        max_height = min(450, 350 + (self.difficulty - 1) * 20)
        self.height = random.randrange(min_height, max_height)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, pipe_ind, hgscore, difficulty, best_fitness, avg_fitness):
    if gen == 0:
        gen = 1
    
    # Draw background
    win.blit(bg_img, (0, 0))

    # Draw pipes
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    
    # Draw birds
    for bird in birds:
        bird.draw(win)

    # Main game info (left side)
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))

    ai_best_label = STAT_FONT.render("AI Best: " + str(hgscore), 1, (255, 255, 255))
    win.blit(ai_best_label, (10, 40))

    gen_label = STAT_FONT.render("Generation: " + str(gen - 1), 1, (255, 255, 255))
    win.blit(gen_label, (10, 70))

    alive_label = STAT_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(alive_label, (10, 100))

    difficulty_label = STAT_FONT.render("Difficulty: " + str(difficulty), 1, (255, 255, 255))
    win.blit(difficulty_label, (10, 130))

    # Training stats (right side)
    best_fit_label = SMALL_FONT.render(f"Best Fitness: {best_fitness:.1f}", 1, (255, 255, 255))
    win.blit(best_fit_label, (WIN_WIDTH - 200, 10))

    avg_fit_label = SMALL_FONT.render(f"Avg Fitness: {avg_fitness:.1f}", 1, (255, 255, 255))
    win.blit(avg_fit_label, (WIN_WIDTH - 200, 30))

    # Instructions
    instructions = [
        "ESC: Exit Training",
        "S: Save Best AI",
        "D: Toggle Debug Lines"
    ]
    
    for i, instruction in enumerate(instructions):
        text = SMALL_FONT.render(instruction, 1, (200, 200, 200))
        win.blit(text, (WIN_WIDTH - 200, 200 + i * 20))

    pygame.display.update()

def eval_genomes(genomes, config):
    global WIN, gen, ai_high_score, training_stats
    win = WIN
    gen += 1

    nets = []
    birds = []
    ge = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700, 1)]  # Start with difficulty 1
    score = 0
    current_ai_high = ai_high_score
    difficulty = 1

    clock = pygame.time.Clock()
    run = True

    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        for x, bird in enumerate(birds):
            # Enhanced fitness function
            ge[x].fitness += 0.1  # Survival bonus
            bird.move()

            # Enhanced inputs
            next_pipe = pipes[pipe_ind]
            pipe_gap_center = next_pipe.height + next_pipe.gap / 2
            
            next_pipe_distance = 0
            if len(pipes) > pipe_ind + 1:
                next_pipe_distance = pipes[pipe_ind + 1].x - bird.x
            
            inputs = (
                bird.y,
                abs(bird.y - next_pipe.bottom),
                abs(bird.y - next_pipe.top),
                bird.vel,
                next_pipe_distance,
                pipe_gap_center,
                difficulty  # Add difficulty as input
            )

            output = nets[birds.index(bird)].activate(inputs)

            if output[0] > 0.5:
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()

            for bird in birds:
                if pipe.collide(bird, win):
                    # Penalize based on how long bird survived
                    penalty = -1 - (bird.alive_time / 1000)
                    ge[birds.index(bird)].fitness += penalty
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            
            # Increase difficulty every 10 pipes
            if score % 10 == 0:
                difficulty += 1
            
            if score > current_ai_high:
                current_ai_high = score
                ai_high_score = score
                save_ai_high_score()

            # Reward for passing pipes
            for genome in ge:
                genome.fitness += 5 + difficulty  # More reward for higher difficulty

            pipes.append(Pipe(WIN_WIDTH, difficulty))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        # Calculate fitness statistics
        if ge:
            best_fitness = max(g.fitness for g in ge)
            avg_fitness = sum(g.fitness for g in ge) / len(ge)
        else:
            best_fitness = 0
            avg_fitness = 0

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind, current_ai_high, difficulty, best_fitness, avg_fitness)

        # Save best model periodically
        if score > 50 and score % 10 == 0:
            if nets:
                pickle.dump(nets[0], open("best.pickle", "wb"))

    # Record generation statistics
    if ge:
        training_stats["generations"].append(gen - 1)
        training_stats["best_fitness"].append(max(g.fitness for g in ge))
        training_stats["avg_fitness"].append(sum(g.fitness for g in ge) / len(ge))
        save_training_stats()

def run(config_file):
    load_ai_high_score()
    
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    print("\nBest genome:\n{!s}".format(winner))
    print(f"Final AI High Score: {ai_high_score}")

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-enhanced.txt")
    run(config_path)
