import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100,100], pygame.SRCALPHA)
        pygame.draw.rect(self.image, (200,200,69), [0,0,100,100])
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.x_change = 0
        self.y_change = 0
        self.x = x
        self.y = y

    def right(self):
        self.x_change = 5
    def up(self):
        self.y_change = -5
    def left(self):
        self.x_change = -5
    def down(self):
        self.y_change = 5


    def update(self, *args):
        self.x += self.x_change
        self.y += self.y_change
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

pygame.init()
display_size_x = 1000
display_size_y = 700
gameDisplay = pygame.display.set_mode((display_size_x, display_size_y))
pygame.display.set_caption("SRIHARI VISHNU")

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
crashed = False

x = display_size_x/2-75
y = display_size_y/2-65
player = Player(x,y)
sprites.add(player)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left()
            if event.key == pygame.K_RIGHT:
                player.right()
            if event.key == pygame.K_UP:
                player.up()
            if event.key == pygame.K_DOWN:
                player.down()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                player.y_change = 0

    
    gameDisplay.fill((255, 255, 255))
    sprites.update()
    sprites.draw(gameDisplay)
    clock.tick(60)
    pygame.display.update()

pygame.quit()
quit()
