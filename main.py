import pygame, pygame.gfxdraw, random, math
from Player import *
WIDTH_LIGHT=30
MAX_DISTANCE = 100

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
    for x in range(-1*WIDTH_LIGHT, WIDTH_LIGHT+1):
        current = angle + x
        hit = False
        targetposy = center[1] + (2 * math.sin(math.radians(current)) * MAX_DISTANCE)
        targetposx = center[0] + (2 * math.cos(math.radians(current)) * MAX_DISTANCE)
        xdisp = (targetposx - center[0]) / MAX_DISTANCE
        ydisp = (targetposy - center[1]) / MAX_DISTANCE
        for y in range(MAX_DISTANCE):
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

def check_collisions():
    collides = False
    new_rect = pygame.Rect(position[0] + player.xvel - player.rect[2] / 2,
                           position[1] + player.yvel - player.rect[3] / 2, player.rect[2], player.rect[3])
    for wall in walls:
        if new_rect.colliderect(wall):
            collides = True
    if player.rect[2] / 2 <= position[0] + player.xvel <= WIDTH - player.rect[2] / 2:
        if not collides:
            player.position[0] += player.xvel
        else:
            player.bouncex()
    else:
        player.bouncex()

    if player.rect[3] / 2 <= position[1] + player.yvel <= HEIGHT - player.rect[3] / 2:
        if not collides:
            player.position[1] += player.yvel
        else:
            player.bouncey()
    else:
        player.bouncey()

def draw_screen():
    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.rect(screen, (0,0,0), wall)
    box_surface_fill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pointlist = get_light(position, targetangle, walls)
    pygame.draw.polygon(box_surface_fill, (255, 255, 100, max(0, min(brightness, 255))), pointlist)
    screen.blit(box_surface_fill, (0, 0))
    sprites.update()
    sprites.draw(screen)
    pygame.display.flip()

# WIDTH = 1250
# HEIGHT = 950
WIDTH = 500
HEIGHT = 500
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
center = [WIDTH/2, HEIGHT/2]
mouse_position = center
sprites = pygame.sprite.Group()
player = Player([400, 400], 20)
sprites.add(player)

targetangle = 260
crashed = False
forward = False
left = False
right = False
down = False
brightness = 180
clock = pygame.time.Clock()
walls = []
for x in range(3):
    walls.append(pygame.Rect(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 50, 50))
while not crashed:
    # print (targetangle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
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

    if left:
        player.move_left()
    if right:
        player.move_right()
    if forward:
        player.move_up()
    if down:
        player.move_down()

    position = player.get_position()
    check_collisions()
    position[0] = min(max(position[0], player.rect[2] / 2), WIDTH - player.rect[2] / 2)
    position[1] = min(max(position[1], player.rect[3] / 2), HEIGHT - player.rect[3] / 2)
    player.set_position(position[0], position[1])

    new_angle = calculate_angle(mouse_position[0], mouse_position[1], position[0], position[1])
    if new_angle:
        targetangle = new_angle

    draw_screen()
    clock.tick(60)
