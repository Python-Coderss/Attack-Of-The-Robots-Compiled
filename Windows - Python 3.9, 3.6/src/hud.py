import pygame
import toolbox

class HUD():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        
        self.state = "mainmenu"
        
        self.hud_font = pygame.font.SysFont("century", 30)
        self.r_font = pygame.font.SysFont("arial_black", 30)
        self.r_font_big = pygame.font.SysFont("arial_black", 80)
        
        self.score_text = self.hud_font.render("Sucsesful", True, (255, 255, 255))
        
        self.title_image = pygame.image.load("assets/title.png")
        self.start_text = self.r_font.render("Press any key to start", True, (255, 255, 255))
        self.gameover_text = self.r_font_big.render("Game Over", True, (255, 0, 0))
        self.reset_button = pygame.image.load("assets/BtnReset.png")
         
        self.crate_icon = pygame.image.load("assets/Crate.png")
        self.explosive_crate_icon = pygame.image.load("assets/ExplosiveCrate.png")
        self.split_shot_icon = pygame.image.load("assets/iconSplitBlue.png")
        self.stream_shot_icon = pygame.image.load("assets/iconStream.png")
        self.burst_shot_icon = pygame.image.load("assets/iconBurst.png")
        self.normal_shot_icon = pygame.image.load("assets/BalloonSmall.png")
        self.bg = pygame.image.load("assets/hudTile.png")
        
        self.crate_ammo_title = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosive_crate_ammo_title = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)
        self.balloon_ammo_title = AmmoTile(self.screen, self.normal_shot_icon, self.hud_font)
    def update(self):
        if self.state == "ingame":
            x, y = toolbox.centeringCoords(self.bg, self.screen)
            xa = x - 72
            xb = x + 72
            self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (255, 255, 255))
            self.screen.blit(self.score_text, (1, 1))
            self.crate_ammo_title.update(xa, self.screen.get_height(), self.player.crate_ammo)
            self.explosive_crate_ammo_title.update(x, self.screen.get_height(), self.player.exp_crate_ammo)
            if self.player.shot_type == "normal":
                self.balloon_ammo_title.icon = self.normal_shot_icon
                self.balloon_ammo_title.update(xb, self.screen.get_height(), self.player.specail_ammo)
            elif self.player.shot_type == "burst" or self.player.exp_balloon:
                self.balloon_ammo_title.icon = self.burst_shot_icon
                self.balloon_ammo_title.update(xb, self.screen.get_height(), self.player.specail_ammo)
            elif self.player.shot_type == "stream":
                self.balloon_ammo_title.icon = self.stream_shot_icon
                self.balloon_ammo_title.update(xb, self.screen.get_height(), self.player.specail_ammo)
            elif self.player.shot_type == "split":
                self.balloon_ammo_title.icon = self.split_shot_icon
                self.balloon_ammo_title.update(xb, self.screen.get_height(), self.player.specail_ammo)
        elif self.state == "mainmenu":
            x, y = toolbox.centeringCoords(self.title_image, self.screen)
            self.screen.blit(self.title_image, (x, y))
            x, y = toolbox.centeringCoords(self.start_text, self.screen)
            
        elif self.state == "gameover":
            t_x, t_y = toolbox.centeringCoords(self.gameover_text, self.screen)
            self.screen.blit(self.gameover_text, (t_x, t_y - 80))
            self.score_text = self.r_font.render("Final score: " + str(self.player.score), True, (255,0,0))
            t_x, t_y = toolbox.centeringCoords(self.score_text, self.screen)
            self.screen.blit(self.score_text, (t_x, t_y))
            bx, by = toolbox.centeringCoords(self.reset_button, self.screen)
            by += 100
            
            btn_rect = self.screen.blit(self.reset_button, (bx, by))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()
                    if btn_rect.collidepoint(mpos):
                        self.state = "mainmenu"
                    
class AmmoTile():
    def __init__(self, screen, icon, font):
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bg_image = pygame.image.load("assets/hudTile.png")
    def update(self, x, y, ammo):
        tile_rect = self.bg_image.get_rect()
        tile_rect.bottomleft = (x, y)
        self.screen.blit(self.bg_image, tile_rect)
        icon_rect = self.icon.get_rect()
        icon_rect.center = tile_rect.center
        self.screen.blit(self.icon, icon_rect)
        ammo_text = self.font.render(str(ammo), True, (255, 255, 255))
        self.screen.blit(ammo_text, tile_rect.topleft)
    
