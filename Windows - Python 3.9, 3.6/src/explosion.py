import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, images, duration, damage, damage_player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.images = images
        self.duration = duration
        self.damage = damage
        self.damage_player = damage_player
        self.rect = self.images[0].get_rect()
        self.rect.center = (self.x, self.y)
        self.a_timer = duration
        self.frame_to_draw = 0
        self.last_frame = len(self.images) - 1
        self.animation_timer = self.duration
    def update(self):
        self.animation_timer -= 1
        if self.animation_timer <= 0:
            if self.frame_to_draw < self.last_frame:
                self.frame_to_draw += 1
                self.animation_timer = self.duration
            else:
                self.kill()
        self.screen.blit(self.images[self.frame_to_draw], self.rect)
