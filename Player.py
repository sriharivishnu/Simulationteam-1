# Player class to define players
import pygame
import math
class Player(pygame.sprite.Sprite):
    FRICTION = 0.75
    MAX_VELOCITY = 5
    ACCELERATION = 1.5

    def __init__(self, position, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, width], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 10, 69), [width//2, width//2], width//2)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.width = width
        self.rect.center = position
        self.xvel = 0
        self.yvel = 0
        self.position = position
        self.angle = 0
        self.deceleration = True

    # Accelerate forward in the direction the player is facing
    def thrust(self):
        # Calculate the horizontal component of velocity
        self.xvel = self.xvel + self.ACCELERATION * math.cos(math.radians(self.angle))
        # Calculate the vertical component of velocity
        self.yvel = self.yvel + self.ACCELERATION * math.sin(math.radians(self.angle))

        # Make sure the velocity doesn't go above the max velocity
        if self.xvel > self.MAX_VELOCITY:
            self.xvel = self.MAX_VELOCITY
        if self.xvel < -self.MAX_VELOCITY:
            self.xvel = -self.MAX_VELOCITY
        if self.yvel > self.MAX_VELOCITY:
            self.yvel = self.MAX_VELOCITY
        if self.yvel < -self.MAX_VELOCITY:
            self.yvel = -self.MAX_VELOCITY

    def bouncex(self):
        self.xvel = -self.xvel / 2

    def bouncey(self):
        self.yvel = -self.yvel / 2

    def move_right(self):
        self.angle = 0
        self.thrust()

    def move_up(self):
        self.angle = 270
        self.thrust()

    def move_left(self):
        self.angle = 180
        self.thrust()

    def move_down(self):
        self.angle = 90
        self.thrust()

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position = [x, y]

    # Called every frame
    def update(self, *args):

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Get new rect object
        self.rect = self.image.get_rect()
        # Set the rect center to the new position
        self.rect.center = self.position

        # Decrease velocity every frame by the friction of the surface as long as its
        # greater than 0
        if self.deceleration:
            if -1 < self.xvel < 1:
                self.xvel = 0
            elif self.xvel >= 1:
                self.xvel -= self.FRICTION
            else:
                self.xvel += self.FRICTION

            if -1 < self.yvel < 1:
                self.yvel = 0
            elif self.yvel >= 1:
                self.yvel -= self.FRICTION
            else:
                self.yvel += self.FRICTION
