import pygame
import toolbox
import math
from explosion import Explosion

class WaterBalloon(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, angle):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.x = x
         self.y = y
         self.screen = screen
         self.angle = angle
         self.image = pygame.image.load("assets/BalloonSmall.png")
         self.exp_images = [pygame.image.load("assets/SplashSmall1.png"), pygame.image.load("assets/SplashSmall2.png"), pygame.image.load("assets/SplashSmall3.png")]
         self.rect = self.image.get_rect()
         self.rect.center = (self.x, self.y)
         self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
         self.speed = 10
         self.angle_rads = math.radians(self.angle)
         self.x_m = math.cos(self.angle_rads) * self.speed
         self.y_m = -math.sin(self.angle_rads) * self.speed
         self.damage = 5
    def update(self):
        self.x += self.x_m
        self.y += self.y_m
        self.rect.center = (self.x, self.y)
        if self.x < -self.image.get_width():
            self.kill()
        elif self.x > self.screen.get_width() + self.image.get_width():
            self.kill()
        elif self.y < -self.image.get_height():
            self.kill()
        elif self.y > self.screen.get_height() + self.image.get_height():
            self.kill()

        
        self.screen.blit(self.image, self.rect)
    def explode(self):
        Explosion(self.screen, self.x, self.y, self.exp_images, 4, 0, False)
        self.kill()
class SplitWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("assets/BalloonSplit.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.damage = 20
class WaterDroplet(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("assets/DropSmall.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.damage = 5
class ExplosiveWaterBalloon(WaterBalloon):
    def __init__(self, screen, x, y, angle):
        WaterBalloon.__init__(self, screen, x, y, angle)
        self.image = pygame.image.load("assets/Balloon.png")
        self.rect = self.image.get_rect()
        self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.exp_images = [pygame.image.load("assets/SplashLarge1.png"), pygame.image.load("assets/SplashLarge2.png"), pygame.image.load("assets/SplashLarge3.png")]
    def explode(self):
        Explosion(self.screen, self.x, self.y, self.exp_images, 4, 2, False)
        self.kill()
