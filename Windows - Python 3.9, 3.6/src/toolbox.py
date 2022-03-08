import pygame
import math

def getRotatedImage(image, rect, angle):
    newImage = pygame.transform.rotate(image, angle)
    newRect = newImage.get_rect(center=rect.center)
    return newImage, newRect
def angleBetweenPoints(x1, y1, x2, y2):
    x_d = x2 - x1
    y_d = y2 - y1
    angle = math.degrees(math.atan2(-y_d, x_d))
    return angle
def centeringCoords(image, screen):
    new_x = screen.get_width()/2 - image.get_width()/2
    new_y = screen.get_height()/2 - image.get_height()/2
    return new_x, new_y
