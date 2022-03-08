import pygame
import toolbox
import math
import random
from powerup import PowerUp
from explosion import Explosion

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("assets/Enemy_05.png")
        self.image_hurt = pygame.image.load("assets/Enemy_05_hurt.png")
        self.exp_images = [pygame.image.load("assets/MediumExplosion1.png"), pygame.image.load("assets/MediumExplosion2.png"), pygame.image.load("assets/MediumExplosion3.png")]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.health = 20
        self.hurt_timer = 0
        self.damage = 1
        self.speed = 1
        self.obstacle_anger = 0
        self.obstacle_anger_max = 200
        self.powerup_drop_chance = 101
    def update(self, projectiles, player, crates, exps):
        
        self.rect.center = (self.x, self.y)
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)
        if self.hurt_timer > 0:
            self.image_to_draw, self.rect_to_use = toolbox.getRotatedImage(self.image_hurt, self.rect, self.angle)
            self.hurt_timer -= 1
        else:
            self.image_to_draw, self.rect_to_use = toolbox.getRotatedImage(self.image, self.rect, self.angle)
        self.angle_rads = math.radians(self.angle)
        self.x_m = math.cos(self.angle_rads) * 1
        self.y_m = -math.sin(self.angle_rads) * 1
        
        for projectile in projectiles:
                if self.rect.colliderect(projectile):
                    self.getHit(projectile.damage, 1, player)
                    projectile.explode()
        for exp in exps:
            if exp.damage:
                if self.rect.colliderect(exp.rect):
                    self.getHit(exp.damage, 1, player)
        
        self.screen.blit(self.image_to_draw, self.rect_to_use)
        test_rect = self.rect
        test_rect.x += self.speed * self.x_m
        test_rect.y += self.speed * self.y_m
        collision = False
        
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                collision = True
                self.getAngry(crate)
        if not collision:
            self.x += self.x_m * self.speed
            self.y += self.y_m * self.speed
        if not player.alive:
            self.kill()
        
    def getHit(self, damage, mult, player):
        if damage:
            self.hurt_timer = 10
            self.x -= self.x_m * (mult * 10)
            self.y -= self.y_m * (mult * 10)
            self.health -= damage
            self.screen.blit(self.image_to_draw, self.rect_to_use)
            if self.health <= 0:
                self.health = 999999
                player.getScore(50)
                Explosion(self.screen, self.x, self.y, self.exp_images, 5, 0, False)
                if random.randint(0, 100) < self.powerup_drop_chance:
                    PowerUp(self.screen, self.x, self.y)
                self.kill()
    def getAngry(self, crate):
        self.obstacle_anger += 1
        if self.obstacle_anger >= self.obstacle_anger_max:
            crate.getHit(self.damage)
            self.obstacle_anger = 0
