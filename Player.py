import pygame
import math


# Spaceship class to define players
class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 100], pygame.SRCALPHA)
        pygame.draw.rect(self.image, (200, 200, 69), [0, 0, 100, 100])
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.xvel = 0
        self.yvel = 0
        self.position = position
        self.angle = 0

    # Accelerate forward in the direction the ship is facing
    def thrust(self):
        # Calculate the horizontal component of velocity
        self.xvel = self.xvel + ACCELERATION * math.cos(math.radians(self.angle))
        # Calculate the vertical component of velocity
        self.yvel = self.yvel + ACCELERATION * math.sin(math.radians(self.angle))

        # Make sure the velocity doesn't go above the max velocity
        if self.xvel > MAX_VELOCITY:
            self.xvel = MAX_VELOCITY
        if self.yvel > MAX_VELOCITY:
            self.yvel = MAX_VELOCITY

    def move_right(self):
        self.angle = 0
        self.thrust()

    def move_up(self):
        self.angle = 90
        self.thrust()

    def move_left(self):
        self.angle = 180
        self.thrust()

    def move_down(self):
        self.angle = 270
        self.thrust()

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position = [x, y]

    # Called every frame
    def update(self, *args):
        addx = self.xvel
        addy = -self.yvel

        self.position[0] += addx
        self.position[1] += addy

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Get new rect object
        self.rect = self.image.get_rect()
        # Set the rect center to the new position
        self.rect.center = self.position

        # Decrease velocity every frame by the deceleration of the surface as long as its
        # greater than 0
        if -1<self.xvel<1:
            self.xvel = 0
        elif self.xvel >= 1:
            self.xvel -= FRICTION
        else:
            self.xvel += FRICTION

        if -1<self.yvel < 1:
            self.yvel = 0
        elif self.yvel >= 1:
            self.yvel -= FRICTION
        else:
            self.yvel += FRICTION

WIDTH = 500
HEIGHT = 500
MAX_VELOCITY = 10
ACCELERATION = 1
ANGLE_ACCELERATION = 1
MAX_ANGLE_VELOCITY = 5
FRICTION = 0.75
white = (255, 255, 255)

pygame.init()
display_size_x = 550
display_size_y = 500
gameDisplay = pygame.display.set_mode((display_size_x, display_size_y))
pygame.display.set_caption("SRIHARI VISHNU")

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
crashed = False

x = display_size_x / 2 - 75
y = display_size_y / 2 - 65
player1 = Player([x, y])
sprites.add(player1)

forward = False
left = False
right = False
down = False

while not crashed:
    for event in pygame.event.get():
        # Listen for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                forward = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                forward = False
            if event.key == pygame.K_DOWN:
                down = False
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False

    # Apply the thrust, or rotation according to which key was pressed
    position = player1.get_position()
    if 50 <= position[0] + player1.xvel <= WIDTH:
        if left:
            player1.move_left()
        if right:
            player1.move_right()
    else:
        player1.xvel = 0

    if 50 <= position[1] + player1.yvel <= HEIGHT-50:
        if forward:
            player1.move_up()

        if down:
            player1.move_down()
    else:
        player1.yvel = 0

    position[0] = min(max(position[0], 50), WIDTH)
    position[1] = min(max(position[1],50), HEIGHT-50)
    player1.set_position(position[0],position[1])
    gameDisplay.fill((255, 255, 255))
    sprites.update()
    sprites.draw(gameDisplay)
    clock.tick(60)
    pygame.display.update()

pygame.quit()
quit()
