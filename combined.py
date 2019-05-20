import pygame, pygame.gfxdraw, random, math


# Spaceship class to define players
class Player(pygame.sprite.Sprite):
    FRICTION = 0.75
    MAX_VELOCITY = 10
    ACCELERATION = 1

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, 50], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 10, 69), [25, 25], 25)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.xvel = 0
        self.yvel = 0
        self.position = position
        self.angle = 0
        self.deceleration = True

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
        self.xvel = -self.xvel / 2

    def bouncey(self):
        self.yvel = -self.yvel / 2

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

def calculate_angle(x1,y1,x2,y2):
    if x1 - x2 != 0:
        y = y1 - y2
        x = x1 - x2
        angle = math.degrees(math.atan(y / x))
        if x < 0 and y > 0 or x < 0 and y < 0:
            angle += 180
        return angle
    return None

def get_light(center, angle, walls):
    pointlist = [center]
    hit = False
    for x in range(-30, 31):
        current = angle + x
        hit = False
        targetposy = center[1] + (2 * math.sin(math.radians(current)) * targetdist)
        targetposx = center[0] + (2 * math.cos(math.radians(current)) * targetdist)
        xdisp = (targetposx - center[0]) / targetdist
        ydisp = (targetposy - center[1]) / targetdist
        for y in range(targetdist):
            for wall in walls:
                if wall.collidepoint((center[0] + xdisp * y), (center[1] + ydisp * y)):
                    pointlist.append(((center[0] + xdisp * y), (center[1] + ydisp * y)))
                    hit = True
                    break
            if hit:
                break

        if not hit:
            pointlist.append((targetposx, targetposy))
    return pointlist
WIDTH = 800
HEIGHT = 500
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
center = [WIDTH/2, HEIGHT/2]
mouse_position = center
sprites = pygame.sprite.Group()
player = Player([400, 400])
sprites.add(player)
targetdist = 100
targetangle = 260
crashed = False
forward = False
left = False
right = False
down = False
brightness = 180
clock = pygame.time.Clock()
walls = [pygame.Rect(300, 50, 100, 100), pygame.Rect(300, 200, 50, 50)]
while not crashed:
    # print (targetangle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bruh = True
        if event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                forward = True
            if event.key == pygame.K_s:
                down = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_UP:
                brightness += 10
            if event.key == pygame.K_DOWN:
                brightness -= 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                forward = False
            if event.key == pygame.K_s:
                down = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False


    position = player.get_position()
    for wall in walls:
        if player.rect.colliderect(wall):
            player.bouncex()
            player.bouncey()
    if player.rect[2] / 2 <= position[0] + player.xvel <= WIDTH - player.rect[2] / 2:
        if left:
            player.move_left()
        if right:
            player.move_right()
    else:
        player.bouncex()

    if player.rect[3] / 2 <= position[1] + player.yvel <= HEIGHT - player.rect[3] / 2:
        if forward:
            player.move_up()

        if down:
            player.move_down()
    else:
        player.bouncey()
    position[0] = min(max(position[0], player.rect[2] / 2), WIDTH - player.rect[2] / 2)
    position[1] = min(max(position[1], player.rect[3] / 2), HEIGHT - player.rect[3] / 2)
    player.set_position(position[0], position[1])
    new_angle = calculate_angle(mouse_position[0], mouse_position[1], position[0], position[1])
    if new_angle:
        targetangle = new_angle
    screen.fill((0, 0, 0))
    box_surface_fill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pointlist = get_light(position, targetangle, walls)
    pygame.draw.polygon(box_surface_fill, (255, 255, 100, min(brightness,255)), pointlist)
    screen.blit(box_surface_fill, (0,0))
    sprites.update()
    sprites.draw(screen)
    pygame.display.flip()
    clock.tick(30)
