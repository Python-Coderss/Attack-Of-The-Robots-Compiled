import pygame
import random
import toolbox

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.pick_power = random.randint(0, 5)
        rand = random.randint(0, 1)
        if self.pick_power == 0:
            self.image = pygame.image.load("assets/powerupCrate.png")
            self.power_type = "crateammo"
        elif self.pick_power == 1:
            self.image = pygame.image.load("assets/powerupExplosiveCrate.png")
            self.power_type = "explosivecrateammo"
        elif self.pick_power == 2:
            self.image = pygame.image.load("assets/heart.png")
            self.power_type = "hp"
        elif self.pick_power == 3:
            self.image = pygame.image.load("assets/powerupSplitmd.png")
            self.power_type = "split"
        elif self.pick_power == 4:
            self.image = pygame.image.load("assets/powerupDrop.png")
            self.power_type = "stream"
        elif self.pick_power == 5:
            self.image = pygame.image.load("assets/SplashSmall1.png")
            self.power_type = "burst"
        if rand:
            self.background_image = pygame.image.load("assets/powerupBackgroundBlue.png")
        if not rand:
            self.background_image = pygame.image.load("assets/powerupBackgroundRed.png")
            if self.pick_power == 3:
                self.background_image = pygame.image.load("assets/powerupBackgroundBlue.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.background_angle = 0
        self.spin_speed = 2
        self.despawn_timer_max = 800
        self.despawn_timer = self.despawn_timer_max
    def update(self, player):
        self.despawn_timer -= 1
        if self.despawn_timer <= 0:
            self.kill()
        if self.rect.colliderect(player.rect):
            player.powerUp(self.power_type)
            self.kill()
        self.background_angle += self.spin_speed
        if self.background_angle >= 360:
            self.background_angle = 0
        bg_image_to_draw, bg_rect = toolbox.getRotatedImage(self.background_image, self.rect, self.background_angle)
        if self.despawn_timer % 10 >= 5 or self.despawn_timer > 200:
            self.screen.blit(bg_image_to_draw, bg_rect)
            self.screen.blit(self.image, self.rect)
