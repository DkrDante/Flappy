import pygame
import random
import os
import time
import neat
import pickle
import math

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 30)
BIG_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Enhanced Flappy Bird")

# Load images
pipe_img = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha()
)
bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900)
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

# Create power-up images (colored circles for now)
power_up_img = pygame.Surface((20, 20))
power_up_img.fill((255, 255, 0))  # Yellow for power-ups

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type  # 'slow', 'shield', 'double_points'
        self.img = power_up_img
        self.vel = 3
        self.active = True
        
    def move(self):
        self.x -= self.vel
        
    def draw(self, win):
        if self.active:
            win.blit(self.img, (self.x, self.y))
            
    def collide(self, bird):
        if not self.active:
            return False
        bird_rect = pygame.Rect(bird.x, bird.y, bird.img.get_width(), bird.img.get_height())
        power_rect = pygame.Rect(self.x, self.y, 20, 20)
        return bird_rect.colliderect(power_rect)

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
        self.shield = False
        self.shield_timer = 0
        self.slow_motion = False
        self.slow_timer = 0

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
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

        # Update power-up timers
        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False
                
        if self.slow_motion:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.slow_motion = False

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
        
        # Draw shield effect
        if self.shield:
            pygame.draw.circle(win, (0, 255, 255), (int(self.x + self.img.get_width()/2), int(self.y + self.img.get_height()/2)), 30, 3)

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
        self.vel = 5 + (difficulty - 1) * 1  # Speed increases with difficulty
        self.gap = max(150, 200 - (difficulty - 1) * 5)  # Gap decreases with difficulty
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        if bird.shield:  # Shield protects from collision
            return False
            
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

def draw_window(win, bird, pipes, base, power_ups, score, high_score, difficulty, double_points):
    win.blit(bg_img, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
        
    for power_up in power_ups:
        power_up.draw(win)

    base.draw(win)
    bird.draw(win)

    # Score
    score_text = f"Score: {score}"
    if double_points:
        score_text += " (2x)"
    score_label = STAT_FONT.render(score_text, 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # High Score
    high_score_label = STAT_FONT.render("High Score: " + str(high_score), 1, (255, 255, 255))
    win.blit(high_score_label, (WIN_WIDTH - high_score_label.get_width() - 10, 40))

    # Difficulty
    difficulty_label = STAT_FONT.render(f"Difficulty: {difficulty}", 1, (255, 255, 255))
    win.blit(difficulty_label, (10, 10))
    
    # Power-up status
    if bird.shield:
        shield_label = STAT_FONT.render("Shield Active!", 1, (0, 255, 255))
        win.blit(shield_label, (10, 40))
        
    if bird.slow_motion:
        slow_label = STAT_FONT.render("Slow Motion!", 1, (255, 255, 0))
        win.blit(slow_label, (10, 70))

    pygame.display.update()

def load_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

def main():
    bird = Bird(230, 350)
    base = Base(FLOOR)
    pipes = [Pipe(700, 1)]
    power_ups = []
    score = 0
    high_score = load_high_score()
    difficulty = 1
    double_points = False
    double_points_timer = 0
    
    clock = pygame.time.Clock()
    run = True
    power_up_counter = 0

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()
        base.move()

        # Update double points timer
        if double_points:
            double_points_timer -= 1
            if double_points_timer <= 0:
                double_points = False

        # Generate power-ups randomly
        power_up_counter += 1
        if power_up_counter > 300:  # Every 10 seconds at 30 FPS
            if random.random() < 0.3:  # 30% chance
                power_type = random.choice(['slow', 'shield', 'double_points'])
                power_ups.append(PowerUp(WIN_WIDTH, random.randint(100, 600), power_type))
            power_up_counter = 0

        # Move and check power-ups
        for power_up in power_ups[:]:
            power_up.move()
            
            if power_up.collide(bird):
                if power_up.power_type == 'shield':
                    bird.shield = True
                    bird.shield_timer = 180  # 6 seconds
                elif power_up.power_type == 'slow':
                    bird.slow_motion = True
                    bird.slow_timer = 120  # 4 seconds
                elif power_up.power_type == 'double_points':
                    double_points = True
                    double_points_timer = 300  # 10 seconds
                power_up.active = False
                power_ups.remove(power_up)
            elif power_up.x < -50:
                power_ups.remove(power_up)

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()

            if pipe.collide(bird, WIN):
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                run = False

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 2 if double_points else 1
            # Increase difficulty every 10 points
            if score % 10 == 0:
                difficulty += 1
            pipes.append(Pipe(WIN_WIDTH, difficulty))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            run = False

        draw_window(WIN, bird, pipes, base, power_ups, score, high_score, difficulty, double_points)

    # Game Over screen
    game_over_label = END_FONT.render("Game Over!", 1, (255, 255, 255))
    WIN.blit(game_over_label, (WIN_WIDTH//2 - game_over_label.get_width()//2, WIN_HEIGHT//2 - 100))
    
    final_score_label = BIG_FONT.render(f"Final Score: {score}", 1, (255, 255, 255))
    WIN.blit(final_score_label, (WIN_WIDTH//2 - final_score_label.get_width()//2, WIN_HEIGHT//2 - 50))
    
    difficulty_label = STAT_FONT.render(f"Difficulty Reached: {difficulty}", 1, (255, 255, 255))
    WIN.blit(difficulty_label, (WIN_WIDTH//2 - difficulty_label.get_width()//2, WIN_HEIGHT//2))
    
    restart_label = STAT_FONT.render("Press SPACE to restart", 1, (255, 255, 255))
    WIN.blit(restart_label, (WIN_WIDTH//2 - restart_label.get_width()//2, WIN_HEIGHT//2 + 50))
    
    pygame.display.update()
    
    # Wait for restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()  # Restart game
                    waiting = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
