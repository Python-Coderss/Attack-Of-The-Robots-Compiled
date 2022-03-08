import pygame
import toolbox
import projectile
import crate

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/Player_02.png")
        self.image_hurt = pygame.image.load("assets/Player_02_hurt.png")
        self.image_defeat = pygame.image.load("assets/Enemy_01.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 2
        self.angle = 0
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 10
        self.health_max = 90
        self.health = self.health_max
        self.health_bar_width = self.image.get_width()
        self.health_bar_height = 8
        self.health_bar_green = pygame.Rect(0,0, self.health_bar_width, self.health_bar_height)
        self.health_bar_red = pygame.Rect(0,0, self.health_bar_width, self.health_bar_height)
        self.alive = True
        self.hurt_timer = 0
        self.crate_ammo = 10
        self.exp_crate_ammo = 20
        self.crate_cooldown = 0
        self.crate_cooldown_max = 10
        self.shot_type = "normal"
        self.specail_ammo = 0
        self.exp_balloon = False
        self.score = 0
    def update(self, enemies, exps):
        
        if self.alive:
            self.rect.center = (self.x, self.y)
            for enemy in  enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.getHit(0, 40, self)
                    self.getHit(enemy.damage)
            for exp in exps:
                if exp.damage and exp.damage_player:
                    if self.rect.colliderect(exp.rect):
                        self.getHit(exp.damage)
            if self.crate_cooldown > 0:
                self.crate_cooldown -= 1
            if self.hurt_timer > 0:
                image_to_draw, image_rect = toolbox.getRotatedImage(self.image_hurt, self.rect, self.angle)
                self.hurt_timer -= 1
            else:
                image_to_draw, image_rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
            self.screen.blit(image_to_draw, image_rect)
            m_x, m_y = pygame.mouse.get_pos()
            self.angle = toolbox.angleBetweenPoints(self.x, self.y, m_x, m_y)
            self.shoot_cooldown -= 1
            
        else:
            self.rect.center = (self.x, self.y)
            image_to_draw, image_rect = toolbox.getRotatedImage(self.image_defeat, self.rect, self.angle)
            self.screen.blit(image_to_draw, image_rect)
            #m_x, m_y = pygame.mouse.get_pos()
            #self.angle = toolbox.angleBetweenPoints(self.x, self.y, m_x, m_y)
        if self.x < 0:
            self.x = 0
        if self.x > 1000:
            self.x = 1000
        if self.y < 0:
            self.y = 0
        if self.y > 650:
            self.y = 650
        
        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 10
        
        pygame.draw.rect(self.screen, (255, 0, 0), self.health_bar_red)
        
        self.health_bar_green.topleft = self.health_bar_red.topleft
        
        health_percentage = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_percentage
        if self.alive:
            pygame.draw.rect(self.screen, (0, 255, 0), self.health_bar_green)
    def move(self, x_m, y_m, crates):
        if self.alive:
            test_rect = self.rect
            test_rect.x += self.speed * x_m
            test_rect.y += self.speed * y_m
            collision = False
            
            for crate in crates:
                if test_rect.colliderect(crate.rect) and not crate.just_placed:
                    collision = True
            
            if not collision:
                self.x += self.speed * x_m
                self.y += self.speed * y_m
    def shoot(self):
        if self.shoot_cooldown <= 0 and self.alive:
            if self.specail_ammo <= 0:
                self.powerUp("normal")
            if self.shot_type == "normal":
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
            else:
                if self.exp_balloon:
                    if self.shot_type == "split":
                        j = 0
                        for i in range(0, 16):
                            j += 1
                            h = self.angle + (j * 22.5)
                            projectile.ExplosiveWaterBalloon(self.screen, self.x, self.y, h)
                    projectile.ExplosiveWaterBalloon(self.screen, self.x, self.y, self.angle)
                
                else:
                    if self.shot_type == "split":
                        j = 0
                        for i in range(0, 16):
                            j += 1
                            h = self.angle + (j * 22.5)
                            projectile.SplitWaterBalloon(self.screen, self.x, self.y, h)
                    if self.shot_type == "stream":
                        projectile.WaterDroplet(self.screen, self.x, self.y, self.angle)
                self.specail_ammo -= 1
            self.shoot_cooldown = self.shoot_cooldown_max
    def getHit(self, damage):
        if self.alive:
            self.hurt_timer = 10
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.alive = False
    
    def placeCrate(self):
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:
            crate.Crate(self.screen, self.x, self.y, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
    def placeExplosiveCrate(self):
        if self.alive and self.exp_crate_ammo > 0 and self.crate_cooldown <= 0:
            crate.ExplosiveCrateVONE(self.screen, self.x, self.y, self)
            self.exp_crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
    def powerUp(self, power_type):
        if power_type == "crateammo":
            self.crate_ammo += 10
            self.getScore(10)
        elif power_type == "explosivecrateammo":
            self.exp_crate_ammo += 10
            self.getScore(10)
        elif power_type == "hp":
            self.health = 90
            self.getScore(4)
        elif power_type == "split":
            self.shot_type = "split"
            self.specail_ammo = 40
            self.shoot_cooldown_max = 15
            self.getScore(20)
        elif power_type == "normal":
            self.shot_type = "normal"
            self.shoot_cooldown_max = 10
            self.exp_balloon = False
        elif power_type == "stream":
            self.shot_type = "stream"
            self.specail_ammo = 400
            self.shoot_cooldown_max = 0
            self.exp_balloon = False
            self.getScore(20)
        elif power_type == "burst":
            self.specail_ammo = 35
            self.shoot_cooldown_max = 30
            self.exp_balloon = True
            self.getScore(30)
    def getScore(self, score):
        if self.alive:
            self.score += score
