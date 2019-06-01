import pygame, pygame.gfxdraw, random, math
from Player import *
from Map import *
WIDTH_LIGHT = 30
MAX_DISTANCE = 100
FPS = 60

def calculate_angle(x1,y1,x2,y2):
    if x1 - x2 != 0:
        y = y1 - y2
        x = x1 - x2
        angle = math.degrees(math.atan(y / x))
        if x < 0 and y > 0 or x < 0 and y < 0:
            angle += 180
        return angle
    return None

def get_light(center, angle):
    pointlist = [center]
    for x in range(-1*WIDTH_LIGHT, WIDTH_LIGHT+1):
        current = angle + x
        hit = False
        targetposy = center[1] + (2 * math.sin(math.radians(current)) * MAX_DISTANCE)
        targetposx = center[0] + (2 * math.cos(math.radians(current)) * MAX_DISTANCE)
        xdisp = (targetposx - center[0]) / MAX_DISTANCE
        ydisp = (targetposy - center[1]) / MAX_DISTANCE
        for y in range(0, MAX_DISTANCE, 2):
            for wall in renderlist:
                if camera.apply(wall).collidepoint((center[0] + xdisp * y), (center[1] + ydisp * y)):
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
    new_rect = pygame.Rect(position[0] + player.xvel - player.rect.width / 2, position[1] + player.yvel - player.rect.height / 2, player.rect.width, player.rect.height)
    for wall in renderlist:
        if new_rect.colliderect(wall):
            collides = True

    if not collides:
        player.position[0] += player.xvel
    else:
        player.bouncex()

    if not collides:
        player.position[1] += player.yvel
    else:
        player.bouncey()


def draw_screen():
    screen.fill((255,255,255))
    box_surface_fill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    player1surface.fill((255, 255, 255))
    pygame.draw.polygon(box_surface_fill, (255, 255, 100, max(0, min(brightness, 255))), pointlist)
    player1surface.blit(box_surface_fill, (0, 0))
    sprites.update()
    walls_sprites.update()
    camera.update(player, WIDTH, HEIGHT)
    for sprite in sprites:
        player1surface.blit(sprite.image, camera.apply(sprite))

    for wall in walls_sprites:
        player1surface.blit(wall.image, camera.apply(wall))
    screen.blit(player1surface,(0,0))
    pygame.draw.rect(screen, (125, 124, 200), render, 1)
    pygame.display.flip()


# WIDTH = 1250
# HEIGHT = 950
WIDTH = 1000
HEIGHT = 500
player1surface=pygame.Surface([WIDTH/2,HEIGHT])
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

walls = []
map = Map()

center = [WIDTH/2, HEIGHT/2]
mouse_position = center
sprites = pygame.sprite.Group()
renderlist = pygame.sprite.Group()
walls_sprites = pygame.sprite.Group()

for y, tiles in enumerate(map.map_data):
    for x, tile in enumerate(tiles):
        if tile == "#":
            Wall(x*32, y*32, 32, 32, walls_sprites)

Wall(0, 0, 32*32,32, walls_sprites)
Wall(0,0, 32, 32*32, walls_sprites)
Wall(32*31, 0, 32, 32*32, walls_sprites)
Wall(0, 32*31, 32*32, 32, walls_sprites)

player = Player([WIDTH/2, HEIGHT/2], 20)
sprites.add(player)
render = pygame.Rect(WIDTH/2 - MAX_DISTANCE * 2, HEIGHT/2 - MAX_DISTANCE * 2, MAX_DISTANCE * 4,MAX_DISTANCE * 4)
camera = Camera(WIDTH, HEIGHT)
targetangle = 260
crashed = False
forward = False
left = False
right = False
down = False
brightness = 180
clock = pygame.time.Clock()

while not crashed:

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


    player.move(left, right, forward, down)

    position = player.get_position()
    actual = camera.apply(player)
    pointlist = get_light([actual.x + player.width//2, actual.y + player.width//2], targetangle)
    check_collisions()
    render.center = actual.center

    for sprite in walls_sprites:
        if render.colliderect(camera.apply(sprite)):
            renderlist.add(sprite)
        else:
            renderlist.remove(sprite)
    new_angle = calculate_angle(mouse_position[0], mouse_position[1], actual.x + player.width, actual.y + player.width)
    if new_angle:
        targetangle = new_angle

    draw_screen()
    clock.tick(FPS)
    print(clock.get_fps())
