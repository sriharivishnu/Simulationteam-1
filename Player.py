import pygame
#Constructing player class and driver code. Will delete driver code once done
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface
        self.rect = [x,y,100,100]
        self.x_change = 0
        self.y_change = 0
        self.x = x
        self.y = y

    def update(self, *args):
        self.x += self.x_change
        self.y += self.y_change
        pygame.draw.rect()
pygame.init()
display_size_x = 1000
display_size_y = 700
gameDisplay = pygame.display.set_mode((display_size_x, display_size_y))
pygame.display.set_caption("SRIHARI VISHNU")

clock = pygame.time.Clock()
crashed = False
def display_person(x,y,width,height):
    pygame.draw.rect(gameDisplay, (200,200,69), [x,y,x+width, y+height])
def check(x,y):
    if x > 0 and y > 0 and x < display_size_x-150 and y < display_size_y-130:
        return True
    return False
x = display_size_x/2-75
y = display_size_y/2-65
right = False
left = False
x_change = 0
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            if event.key == pygame.K_RIGHT:
                x_change = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = 0


    gameDisplay.fill((255, 255, 255))
    if check(x+x_change,y):
        x += x_change
    display_person(x,y,100,100)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
