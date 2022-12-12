import pygame as pg

WIDTH, HEIGHT = 800, 600
FPS = 60


window = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
img_bg = pg.image.load('image/bg/c.jpg')
img_crow = pg.image.load('image/crow/crowanim.png')
img_toprock = pg.image.load('image/rock/1.png')
img_botrock = pg.image.load('image/rock/2.png')

# player pos y, sy-speed, ay-jump
py, sy, ay = HEIGHT // 2, 0, 0
player = pg.Rect(WIDTH // 3, py, 40, 42)
state = 'start'
frame = 0
timer = 10
rocks = []
bgs = []
bgs.append(pg.Rect(0, 0, 288, 600))


play = True
while play:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            play = False

    # controls
    press = pg.mouse.get_pressed()
    keys = pg.key.get_pressed()
    click = press[0] or keys[pg.K_SPACE]

    # timer если значение > 0 то должен стремиться к 0
    if timer > 0:
        timer -= 1
    # смена кадров
    frame = (frame + 0.1) % 4

    for i in range(len(bgs)-1, -1, -1):
        bg = bgs[i]
        bg.x -= 1
        # drop rocks if off window
        if bg.right < 0:
            bgs.remove(bg)

        # склеивание картинок для фона
        if bgs[len(bgs)-1].right <= WIDTH:
            bgs.append(pg.Rect(bgs[len(bgs)-1].right, 0, 288, 600))

    # obstacles
    for i in range(len(rocks)-1, -1, -1):
        rock = rocks[i]
        rock.x -= 4
        # drop rocks if off window
        if rock.right < 0:
            rocks.remove(rock)

    # state parameters
    if state == 'start':
        if click and timer == 0 and len(rocks) == 0:
            state = 'play'
        # возвращется на место
        py += (HEIGHT // 2 - py) * 0.1
        player.y = py
    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0
        # gravitation player
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        # rocks если труба перешла границу экрана
        if len(rocks) == 0 or rocks[len(rocks)-1].x < WIDTH - 200:
            rocks.append(pg.Rect(WIDTH, 0, 62, 190))
            rocks.append(pg.Rect(WIDTH, 420, 50, 190))

        # столкновение
        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fail'

        for rock in rocks:
            if player.colliderect(rock):
                state = 'fail'

    elif state == 'fail':
        # сброс на начало
        sy, ay = 0, 0
        state = 'start'
        timer = 60
    else:
        pass

    # draw
    window.fill(pg.Color('black'))
    #
    for bg in bgs:
        window.blit(img_bg, bg)
    #

    for rock in rocks:
        if rock.y == 0:
            rect = img_botrock.get_rect(bottomleft=rock.bottomleft)
            window.blit(img_botrock, rect)
        else:
            rect = img_botrock.get_rect(topleft=rock.topleft)
            window.blit(img_toprock, rect)

    image = img_crow.subsurface(60 * int(frame), 0, 37, 40)
    # задирать нос
    image = pg.transform.rotate(image, -sy * 2)
    window.blit(image, player)
    pg.display.update()
    clock.tick(FPS)

pg.quit()