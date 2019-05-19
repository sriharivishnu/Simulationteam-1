import pygame, pygame.gfxdraw, random, math
# Player class to define players
class Player(pygame.sprite.Sprite):
    FRICTION = 0.75
    MAX_VELOCITY = 10
    ACCELERATION = 1
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
        #pygame.draw.rect(self.image, (200, 200, 69), [0, 0, 100, 100])
        pygame.draw.circle(self.image, (200,200,69), [25,25],25)
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
        self.xvel = self.xvel + self.ACCELERATION * math.cos(math.radians(self.angle))
        # Calculate the vertical component of velocity
        self.yvel = self.yvel + self.ACCELERATION * math.sin(math.radians(self.angle))

        # Make sure the velocity doesn't go above the max velocity
        if self.xvel > self.MAX_VELOCITY:
            self.xvel = self.MAX_VELOCITY
        if self.yvel > self.MAX_VELOCITY:
            self.yvel = self.MAX_VELOCITY

    def bouncex(self):
        self.xvel = -self.xvel/2

    def bouncey(self):
        self.yvel = -self.yvel/2

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

        # Decrease velocity every frame by the friction of the surface as long as its
        # greater than 0
        if -1<self.xvel<1:
            self.xvel = 0
        elif self.xvel >= 1:
            self.xvel -= self.FRICTION
        else:
            self.xvel += self.FRICTION

        if -1<self.yvel < 1:
            self.yvel = 0
        elif self.yvel >= 1:
            self.yvel -= self.FRICTION
        else:
            self.yvel += self.FRICTION

WIDTH = 800
HEIGHT = 800
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
center = [400, 400]
sprites = pygame.sprite.Group()
player = Player([400,400])
sprites.add(player)
targetdist = 100
targetangle = 260
hit=False
bruh=True
forward = False
left = False
right = False
down = False
clock = pygame.time.Clock()
while bruh==True:
    #print (targetangle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bruh = False
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0]-center[0] != 0:
                x = event.pos[1]-center[1]
                y = event.pos[0]-center[0]
                targetangle = math.degrees(math.atan(x/y))
                if x > 0 and y < 0 or x < 0 and y < 0:
                    targetangle += 180
            print (targetangle)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                forward = True
            if event.key == pygame.K_s:
                down = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                forward = False
            if event.key == pygame.K_s:
                down = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    wall = pygame.draw.rect(screen, (0, 0, 0), [400 - 100, 50, 100, 100])
    wall1 = pygame.draw.rect(screen, (0, 0, 0), [300, 200, 50, 50])
    position = player.get_position()
    if player.rect.colliderect(wall) or player.rect.colliderect(wall1):
        player.bouncex()
        player.bouncey()
    if 50 <= position[0] + player.xvel <= WIDTH:
        if left:
            player.move_left()
        if right:
            player.move_right()
    else:
        player.bouncex()

    if 50 <= position[1] + player.yvel <= HEIGHT - 50:
        if forward:
            player.move_up()

        if down:
            player.move_down()
    else:
        player.bouncey()



    position[0] = min(max(position[0], 50), WIDTH)
    position[1] = min(max(position[1], 50), HEIGHT - 50)
    player.set_position(position[0], position[1])
    center = position
    screen.fill((0, 0, 0))
    pointlist = [center]
    for x in range(-30, 31):
        y=targetangle+x
        hit=False
        currenttargetangle = targetangle+x
        targetposy = center[1]+(2 * math.sin(math.radians(y)) * targetdist)
        targetposx = center[0]+(2 * math.cos(math.radians(y)) * targetdist)

        xdisp=(targetposx-center[0])/targetdist
        ydisp = (targetposy - center[1]) / targetdist
        for y in range(targetdist):
            if wall.collidepoint((center[0]+xdisp*y),(center[1]+ydisp*y)) or wall1.collidepoint((center[0]+xdisp*y),(center[1]+ydisp*y)):
                pointlist.append(((center[0]+xdisp*y), (center[1]+ydisp*y)))
                hit=True
                break
        if hit!=True:
            pointlist.append((targetposx, targetposy))
    pygame.gfxdraw.filled_polygon(screen,pointlist,(255,255,0))
    sprites.update()
    sprites.draw(screen)
    pygame.display.flip()
    clock.tick(30)
