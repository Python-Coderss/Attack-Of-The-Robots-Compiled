import pygame
from explosion import Explosion

class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("assets/Crate.png")
        self.image_hurt = pygame.image.load("assets/Crate_hurt.png")
        self.exp_images = [pygame.image.load("assets/CrateRubble.png")]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 20
        self.hurt_timer = 0
        self.just_placed = True
    def update(self, projectiles, exps):
        if not self.rect.colliderect(self.player.rect):
            self.just_placed = False
        img = self.image
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                projectile.explode()
                self.getHit(projectile.damage)
        for exp in exps:
            if exp.damage > 0:
                if self.rect.colliderect(exp.rect):
                    self.getHit(exp.damage)
        if self.hurt_timer:
            self.hurt_timer -= 1
            img = self.image_hurt
        self.screen.blit(img, self.rect)
    def getHit(self, damage):
        self.health -=  damage
        self.hurt_timer = 10
        if self.health <= 0:
            self.health = 9999999
            Explosion(self.screen, self.x, self.y, self.exp_images, 640, 0, False)
            self.kill()
class ExplosiveCrate(Crate):
    def __init__(self, screen, x, y, player):
        Crate.__init__(self, screen, x, y, player)
        self.image = pygame.image.load("assets/ExplosiveCrate.png")
        self.image_hurt = pygame.image.load("assets/ExplosiveCrateHurt.png")
        self.health = 20
        self.exp_images = [pygame.image.load("assets/LargeExplosion1.png"), pygame.image.load("assets/LargeExplosion2.png"), pygame.image.load("assets/LargeExplosion3.png")]
    def getHit(self, damage):
        self.health -=  damage
        self.hurt_timer = 10
        if self.health <= 0:
            self.health = 9999999
            Explosion(self.screen, self.x, self.y, self.exp_images, 5, 4, True)
            self.kill()
class ExplosiveCrateVONE(Crate):
    def __init__(self, screen, x, y, player):
        Crate.__init__(self, screen, x, y, player)
        self.image = pygame.image.load("assets/ExplosiveCrate.png")
        self.image_hurt = pygame.image.load("assets/ExplosiveCrateHurt.png")
        self.health = 20
        self.exp_images = [pygame.image.load("assets/LargeExplosion1.png"), pygame.image.load("assets/LargeExplosion2.png"), pygame.image.load("assets/LargeExplosion3.png")]
    def getHit(self, damage):
        self.health -=  damage
        self.hurt_timer = 10
        if self.health <= 0:
            self.health = 9999999
            Explosion(self.screen, self.x, self.y, self.exp_images, 5, 4, False)
            self.kill()
