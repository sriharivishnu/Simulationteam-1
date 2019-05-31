import pygame
class Wall(pygame.sprite.Sprite):
    def __init__(self, x,y, width, height, group):
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width,height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Map:
    def __init__(self):
        self.map_data = []
        with open("maps.txt", "r") as file:
            for line in file:
                self.map_data.append(line)

        self.width = len(self.map_data[0]) * 32
        self.height = len(self.map_data) * 32

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0, width*32, height*32)
        self.width = width
        self.height = height

    def apply(self, sprite):
        new_rect = pygame.Rect(sprite.rect.x + self.camera.x, sprite.rect.y + self.camera.y, sprite.rect.width, sprite.rect.height)
        return new_rect

    def update(self, target, screenw, screenh):
        x = -target.rect.x + screenw //2
        y = -target.rect.y + screenh // 2

        x = max(min(0,x), - (self.width + 32))
        y = max(min(0,y), -(self.height + 32))
        self.camera = pygame.Rect(x,y, self.width, self.height)
