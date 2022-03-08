#!usr\bin\python



import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from crate import ExplosiveCrate
from crate import ExplosiveCrateVONE
from explosion import Explosion
from powerup import PowerUp
from hud import HUD
import toolbox
print("This is the developer console DO NOT CLOSE OR game will CRASH.")
# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

b_g_img = pygame.image.load("assets/BG_SciFi.png")

print("Controls: WASD to move, SPACE to place a crate, Left Click shoot a water balloon to the mouse pointer, Right Click place an explosive crate.")
playerGroup = pygame.sprite.Group()
projectilesGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
cratesGroup = pygame.sprite.Group()
explosionsGroup = pygame.sprite.Group()
powerupsGroup = pygame.sprite.Group()

Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Crate.containers = cratesGroup
Explosion.containers = explosionsGroup
PowerUp.containers = powerupsGroup

enemy_spawn_timer_max = 320 # 1 is testing only 320 is what is sopposed to be there
enemy_spawn_timer = 0
e_s_t_m_s_t_max = 400
e_s_t_m_s_t = e_s_t_m_s_t_max

game_started = False


mr_player = Player(screen, game_width/2, game_height/2)
hud = HUD(screen, mr_player)

def StartGame():
    global game_started
    global hud
    global mr_player
    global enemiesGroup
    global cratesGroup
    global powerupsGroup
    global explosionsGroup
    global enemy_spawn_timer_max
    global e_s_t_m_s_t
    global e_s_t_m_s_t_max
    global enemy_spawn_timer
    e_s_t_m_s_t = e_s_t_m_s_t_max
    enemy_spawn_timer_max = 320
    enemy_spawn_timer = enemy_spawn_timer_max
    for exp in explosionsGroup:
        exp.kill()
    for powerup in powerupsGroup:
        powerup.kill()
    for crate in cratesGroup:
        crate.kill()
    for enemy in enemiesGroup:
        enemy.kill()
    game_started = True
    hud.state = "ingame"
    mr_player.__init__(screen, game_width/2, game_height/2)
    for i in range(0, 10):
        j = 0
        for j in range(0, 6):
            ExplosiveCrateVONE(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)
            ExplosiveCrateVONE(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)
    i = 0
    j = 0
    for i in range(0, 10):
        j = 0
        for j in range(0, 6):
            Crate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(b_g_img,(0,0))
    if game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            mr_player.move(1, 0, cratesGroup)
        if keys[pygame.K_a]:
            mr_player.move(-1, 0, cratesGroup)
        if keys[pygame.K_s]:
            mr_player.move(0, 1, cratesGroup)
        if keys[pygame.K_w]:
            mr_player.move(0, -1, cratesGroup)
        if pygame.mouse.get_pressed() [0]:
            mr_player.shoot()
        if keys[pygame.K_SPACE]:
            mr_player.placeCrate()
        if pygame.mouse.get_pressed() [2]:
            mr_player.placeExplosiveCrate()

        enemy_spawn_timer -= 1
        e_s_t_m_s_t -= 1
        if e_s_t_m_s_t <= 0:
            e_s_t_m_s_t = e_s_t_m_s_t_max
            if enemy_spawn_timer_max < 30:
                enemy_spawn_timer -= 10
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, mr_player)
            side_to_spawn = random.randint(0, 3)
            if side_to_spawn == 0:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = -new_enemy.image.get_height()
            elif side_to_spawn == 1:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = game_height + new_enemy.image.get_height()
            elif side_to_spawn == 3:
                new_enemy.y = random.randint(0, game_height)
                new_enemy.x = game_width + new_enemy.image.get_width()
            elif side_to_spawn == 2:
                new_enemy.y = random.randint(0, game_height)
                new_enemy.x = -new_enemy.image.get_width()
            enemy_spawn_timer = enemy_spawn_timer_max




        for enemy in enemiesGroup:
            enemy.update(projectilesGroup, mr_player, cratesGroup, explosionsGroup)
        for crate in cratesGroup:
            crate.update(projectilesGroup, explosionsGroup)
        for explosion in  explosionsGroup:
            explosion.update()
        for powerup in powerupsGroup:
            powerup.update(mr_player)
        for projectile in projectilesGroup:
            projectile.update()
        mr_player.update(enemiesGroup, explosionsGroup)
        if not mr_player.alive:
            if hud.state == "ingame":
                hud.state = "gameover"

        elif hud.state == "mainmenu":
            game_started = False
    hud.update()
    if game_started == False or hud.state == "mainmenu":
        reset_button = pygame.image.load("assets/BtnPlay.png")
        bx, by = toolbox.centeringCoords(reset_button, screen)
        by += 160

        screen.blit(reset_button, (bx, by))
        btn_rect = screen.blit(reset_button, (bx, by))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                if btn_rect.collidepoint(mpos):
                    StartGame()



    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(int(clock.get_fps())) + " Controls: WASD to move, SPACE to place a crate, Left Click shoot a water balloon to the mouse pointer, Right Click place an explosive crate")
