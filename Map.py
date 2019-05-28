import pygame
class Wall(pygame.sprite.Sprite):
    def __init__(self, pcx, pcy, width, height, group):
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width,height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.pcx = pcx
        self.pcy = pcy
        self.rect.x = pcx*width
        self.rect.y = pcy*height

class Map:
    def __init__(self):
        self.map_data = []
        with open("maps.txt", "r") as file:
            for line in file:
                self.map_data.append(line)

        self.mapwidth = len(self.map_data[0])
        self.mapheight = len(self.map_data)

        self.width = self.mapwidth * 32
        self.height = self.mapheight * 32

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0, width, height)
        self.width = width
        self.height = height

    def apply(self, sprite):
        return sprite.rect.move(self.camera.topleft)

    def update(self, target, screenw, screenh):
        x = -target.rect.x + screenw //2
        y = -target.rect.y + screenh // 2
        self.camera = pygame.Rect(x,y, self.width, self.height)
