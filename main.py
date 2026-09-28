
'''''
Emmanuel Garcia 

Mental growth game.

This game help players choose the rights words for they to say
to themself, and learn how to have a growth mindset instead of a fixed
mindset. To play this game you need to use the space bar to jump and
the letters A and D to move.
The license is: CC BY-NC-ND 4.0
'''

import pygame 
import random 
from sys import exit

#create screen

pygame.init() 
screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption("Mental Growth Game")
clock = pygame.time.Clock()
start_font = pygame.font.Font(None,50)


#create background 
ground = pygame.image.load("assets/ground.png").convert()
sky = pygame.image.load("assets/sky.png").convert()

#Player 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load("assets/pixil-frame-0.png").convert_alpha()
        walk2 = pygame.image.load("assets/pixil-frame-1.png").convert_alpha()
        walk3 = pygame.image.load("assets/pixil-frame-2.png").convert_alpha()
        walk4 = pygame.image.load("assets/pixil-frame-3.png").convert_alpha()
        walk5 = pygame.image.load("assets/pixil-frame-4.png").convert_alpha()
        walk6 = pygame.image.load("assets/pixil-frame-5.png").convert_alpha()
        self.player_index = 0
        self.player_walk = [walk1, walk2, walk3, walk4, walk5, walk6]
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,750))
        self.gravity = 0


    def animation(self):
        if self.rect.bottom < 750:
            self.image = pygame.image.load("assets/pixil-frame-1.png").convert_alpha()
        else:
            self.player_index += 0.2
        if self.player_index >= len(self.player_walk):
            self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 750:
            self.gravity = -28

    def right(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += 8

    def left(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 10

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 750:
            self.rect.bottom = 750

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
        self.right()
        self.left()

# target

class Target(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = random.randint(1600, 2000)
        if type == "growth1":
            self.image = pygame.image.load("assets/growth-1.png").convert_alpha()
        elif type == "growth2":
            self.image = pygame.image.load("assets/growth-2.png").convert_alpha()
        elif type == "growth3":
            self.image = pygame.image.load("assets/growth-3.png").convert_alpha()
        elif type == "growth4":
            self.image = pygame.image.load("assets/growth-4.png").convert_alpha()
        else: 
            self.image = pygame.image.load("assets/growth-5.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.start, 400))

    def update(self):
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

#obsticle class
class Obsticle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = random.randint(1600, 2000)
        if type == "rock1":
            self.image = pygame.image.load("assets/rock-1.png").convert_alpha()
        elif type == "rock2":
            self.image = pygame.image.load("assets/rock-2.png").convert_alpha()
        elif type == "rock3":
            self.image = pygame.image.load("assets/rock-3.png").convert_alpha()
        elif type == "rock4": 
            self.image = pygame.image.load("assets/rock-4.png").convert_alpha()
        else:
            self.image = pygame.image.load("assets/rock-5.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.start, 775))

    def update(self):
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


#check for collision
def check_collision():
    global score
    if player.sprites(): 
        collided_target = pygame.sprite.spritecollide(player.sprites()[0], target_group, True)
        collided_obsticle = pygame.sprite.spritecollide(player.sprites()[0], obsticle_group, True)
        if collided_target:
            score += 1
        if collided_obsticle:
            global health
            health -= 1

#display score
def display_score():
    score_surf = score_font.render("Score:" + str(score), True, (50,50,50))
    score_rect = score_surf.get_rect(center = (100,50))
    screen.blit(score_surf, score_rect)

#display health
def display_health():
    health_surf = health_font.render("Health:" + str(health), True, (50,50,50))
    health_rect = health_surf.get_rect(center = (100,100))
    screen.blit(health_surf, health_rect)

#target group
target_group = pygame.sprite.Group()

#player group
player = pygame.sprite.GroupSingle()
player.add(Player()) 

#obstacle group
obsticle_group = pygame.sprite.Group()

#start screen
start_screen = pygame.image.load("assets/start_screen-1.png").convert()
play_button = pygame.image.load("assets/start_b.png").convert_alpha()
play_rect = play_button.get_rect(center = (800, 600))

#lose/win screen
lose = pygame.image.load("assets/lose_screen-3.png").convert()
win = pygame.image.load("assets/win_screen-2.png").convert()
replay_button = pygame.image.load("assets/replay_b-2.png").convert_alpha()
replay_rect = replay_button.get_rect(center = (800, 600))
exit_button = pygame.image.load("assets/quit_b-3.png").convert_alpha()
exit_rect = exit_button.get_rect(center = (800, 700))

#initialize variables 
game_screen = 0
score = 0 
health = 10
health_font = pygame.font.Font(None, 30)
score_font = pygame.font.Font(None, 30)

pygame.mixer.init()
pygame.mixer.music.load("assets/song.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

#game loop
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)

    #show background

    screen.blit(ground,(0,700))
    screen.blit(sky, (0,0))

    #decide which screen to show
    if game_screen == 0:
        screen.blit(start_screen, (0,0))
        screen.blit(play_button, play_rect)

    elif game_screen == 1:
        screen.blit(ground,(0,700))
        screen.blit(sky, (0,0))

        #player draw and update 

        player.draw(screen)
        player.update()
        #target draw and update

        target_group.draw(screen)
        target_group.update()
        if not target_group:
            i = random.randint(0,1)
            choices = ["growth1", "growth2", "growth3", "growth4", "growth5"]
            target_group.add(Target(choices[i]))

        #obstacle draw and update

        obsticle_group.draw(screen)
        obsticle_group.update()
        if not obsticle_group:
            i = random.randint(0,1)
            choices = ["rock1", "rock2", "rock3", "rock4", "rock5"]
            obsticle_group.add(Obsticle(choices[i]))

        display_score()
        display_health()

        if health <= 0:
            game_screen = 2
        if score >= 10:
            game_screen = 3

    elif game_screen == 2:
        screen.blit(lose, (0,0))
        screen.blit(replay_button, replay_rect)
        screen.blit(exit_button, exit_rect)

    else: 
        screen.blit(win, (0,0))
        screen.blit(replay_button, replay_rect)
        screen.blit(exit_button, exit_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #check if mouse cliclks 
            if event.button == 1:
                if play_rect.collidepoint(event.pos) and game_screen == 0:
                    game_screen = 1
                if replay_rect.collidepoint(event.pos) and game_screen in [2,3]:
                    score = 0
                    health = 10
                    game_screen = 1

                if exit_rect.collidepoint(event.pos) and game_screen in [2,3]:
                    pygame.quit()
                    exit()

    check_collision()

    pygame.display.update()