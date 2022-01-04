import pygame
import random

from pygame.locals import *
pygame.font.init()
pygame.mixer.init()
pygame.display.init()

pygame.mixer.music.load("gametheme1.wav")
crash = pygame.mixer.Sound("Crash.wav")
clear = pygame.mixer.Sound("TING SOUND EFFECT.wav")
End = pygame.mixer.Sound("End.wav")
endpic = pygame.image.load("GameOver.jpg")
winpic = pygame.image.load("win.jpg")
back = pygame.image.load("background2.jpg")
Win = pygame.mixer.Sound("PARTY POPPER with SOUND Green Screen HD.wav")

ScreenWidth = 800
ScreenHeight = 700
PlayWidth = 300
PlayHeight = 600
Cube = 30


x_corner = (ScreenWidth - PlayWidth) // 2
y_corner = ScreenHeight - PlayHeight

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

Q = [['.....',
      '.000.',
      '.000.',
      '.000.',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

X = [['.....',
      '.0.0.',
      '..0..',
      '.0.0.',
      '.....'],
     ['.....',
      '..0..',
      '.000.',
      '..0..',
      '.....']]

H = [['.....',
      '.0.0.',
      '.000.',
      '.0.0.',
      '.....'],
     ['.....',
      '.000.',
      '..0..',
      '.000.',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, X, J, H, L, T, Q]
shape_colors = [(51, 255, 153), (153, 0, 0), (102, 0, 204), (51, 255, 255),(31, 78, 47) ,(255, 153, 51),
                (90, 89, 88),(102, 102, 255), (222, 49, 99),(175, 57, 73)]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def GameLayout(locked_pos={}):
    grid = [[(0,0,0) for n in range(10)] for n in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid

def GridLine(surface, grid):
    sx = x_corner
    sy = y_corner

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i * Cube), (sx + PlayWidth, sy + i * Cube))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * Cube, sy), (sx + j * Cube, sy + PlayHeight))

def ShapeLocation(shape):
    location = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                location.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(location):
        location[i] = (pos[0] - 2, pos[1] - 4)

    return location

def ValidSpace(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = ShapeLocation(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def Lose(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

def RandShape():
    return Piece(5, 1, random.choice(shapes))

def DrawText(surface, text, size, color, y):
    font = pygame.font.SysFont("comicsans", size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label, (x_corner + PlayWidth / 2 - (label.get_width() / 2), y_corner + PlayHeight / 3 + y))

def Clear(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            pygame.mixer.Sound.play(clear)
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def nextshape(shape, surface):
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Next Shape', 1, (0,255,255))

    sx = x_corner + PlayWidth + 50
    sy = y_corner + PlayHeight / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * Cube, sy + i * Cube, Cube, Cube), 0)

    surface.blit(label, (sx + 10, sy - 50))

def updatescore(nscore):
    score = maxscore()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def maxscore():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score

def window(surface, grid, score=0, scorelast = 0):
    surface.fill((0, 0, 0))
    surface.blit(pygame.transform.scale(back, (ScreenWidth, ScreenHeight)), (0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 80)
    label = font.render('Reverse Tetris ', 1, (143, 0, 255))

    surface.blit(label, (x_corner + PlayWidth / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('comicsans', 42)
    label = font.render('Score: ' + str(score), 1, (212,175,55))

    sx = x_corner + PlayWidth + 50
    sy = y_corner + PlayHeight / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    label = font.render('High Score: ' + scorelast, 1, (212,175,55))

    sx = x_corner - 200
    sy = y_corner + 200

    surface.blit(label, (sx - 40, sy + 100))

    label = font.render('Press P to Pause', 1, (204,204,255))

    sx = x_corner - 200
    sy = y_corner + 200

    surface.blit(label, (sx - 40, sy - 100))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (x_corner + j * Cube, y_corner + i * Cube, Cube, Cube), 0)

    pygame.draw.rect(surface, (255, 0, 0), (x_corner, y_corner, PlayWidth, PlayHeight), 5)

    GridLine(surface, grid)

def main(win):
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

    scorelast = maxscore()
    locked_positions = {}
    grid = GameLayout(locked_positions)
    ThisPiece = RandShape()
    NextPiece = RandShape()
    clock = pygame.time.Clock()

    change_piece = False
    Round_1 = True
    Round_2 = True
    Round_3 = True
    run = True

    fall_time = 0
    fall_speed = 0.4
    level_time = 0
    score = 0
    RUN = 1
    PAUSE = 0
    state = RUN

    while run:
        grid = GameLayout(locked_positions)
        clock.tick(60)
        presskey = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            elif presskey[pygame.K_p]:
                state = PAUSE

        if state == PAUSE:
            pygame.mixer.music.pause()
            win.fill((0, 0, 0))
            DrawText(win, "PAUSED", 120, (255, 255, 255),-50)
            DrawText(win, "Press q to quit, c to continue", 60, (255, 255, 255),30)
            if presskey[pygame.K_q]:
                run = False
                pygame.display.quit()
            elif presskey[pygame.K_c]:
                pygame.mixer.music.unpause()
                state = RUN

        if state == RUN:

            fall_time += clock.get_time()
            level_time += clock.get_time()

            if level_time / 1000 > 5:
                level_time = 0
                if level_time > 0.12:
                    level_time -= 0.005

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                ThisPiece.y += 1
                if not (ValidSpace(ThisPiece, grid)) and ThisPiece.y > 0:
                    pygame.mixer.Sound.play(crash)
                    ThisPiece.y -= 1
                    change_piece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

            press = pygame.key.get_pressed()
            if press[pygame.K_LEFT]:
                ThisPiece.x -= press[pygame.K_LEFT]
                pygame.time.delay(90)
                if not (ValidSpace(ThisPiece, grid)):
                    ThisPiece.x += 1
            if press[pygame.K_RIGHT]:
                ThisPiece.x += press[pygame.K_RIGHT]
                pygame.time.delay(90)
                if not (ValidSpace(ThisPiece, grid)):
                    ThisPiece.x -= 1
            if press[pygame.K_DOWN]:
                ThisPiece.y += press[pygame.K_DOWN]
                pygame.time.delay(90)
                if not (ValidSpace(ThisPiece, grid)):
                    ThisPiece.y -= 1
            if press[pygame.K_UP]:
                ThisPiece.rotation += press[pygame.K_UP]
                pygame.time.delay(140)
                if not (ValidSpace(ThisPiece, grid)):
                    ThisPiece.rotation -= 1

            if score < 50:
                if Round_1:
                    win.fill((0, 0, 0))
                    DrawText(win, "ROUND 1", 120, (255, 255, 255),0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    Round_1 = False
                fall_speed = 0.4

            elif score >= 50 and score < 100:
                if Round_2:
                    win.fill((0, 0, 0))
                    DrawText(win, "ROUND 2", 120, (255, 255, 255),-50)
                    DrawText(win, "x2 speed", 80, (255, 255, 255), 30)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    Round_2 = False
                fall_speed = 0.2

            elif score >= 100 and score < 200:
                if Round_3:
                    win.fill((0, 0, 0))
                    DrawText(win, "ROUND 3", 120, (255, 255, 255),-50)
                    DrawText(win, "reverse controls", 80, (255, 255, 255), 30)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    Round_3 = False
                fall_speed = 0.2
                if press[pygame.K_LEFT]:
                    ThisPiece.x += press[pygame.K_LEFT] * 2
                    pygame.time.delay(75)
                    if not (ValidSpace(ThisPiece, grid)):
                        ThisPiece.x -= 1
                if press[pygame.K_RIGHT]:
                    ThisPiece.x -= press[pygame.K_RIGHT] * 2
                    pygame.time.delay(75)
                    if not (ValidSpace(ThisPiece, grid)):
                        ThisPiece.x += 1
                if press[pygame.K_DOWN]:
                    ThisPiece.y -= press[pygame.K_DOWN]
                    if not (ValidSpace(ThisPiece, grid)):
                        ThisPiece.y += 1
                    ThisPiece.rotation += press[pygame.K_DOWN]
                    pygame.time.delay(75)
                    if not (ValidSpace(ThisPiece, grid)):
                        ThisPiece.rotation -= 1
                if press[pygame.K_UP]:
                    ThisPiece.rotation -= press[pygame.K_UP]
                    if not (ValidSpace(ThisPiece, grid)):
                        ThisPiece.rotation += 1
                    ThisPiece.y += press[pygame.K_UP]
                    pygame.time.delay(125)
                    if not (ValidSpace(ThisPiece, grid)):
                        ThisPiece.y -= 1
            else:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(Win)
                win.fill((0, 0, 0))
                win.blit(pygame.transform.scale(winpic, (ScreenWidth, ScreenHeight)), (0, 0))
                pygame.display.update()
                pygame.time.delay(5000)
                run = False
                updatescore(score)

            shape_pos = ShapeLocation(ThisPiece)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = ThisPiece.color

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = ThisPiece.color
                ThisPiece = NextPiece
                NextPiece = RandShape()
                change_piece = False
                score += Clear(grid, locked_positions) * 10

            window(win, grid, score, scorelast)
            nextshape(NextPiece, win)
            pygame.display.update()

            if Lose(locked_positions):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(End)
                win.fill((0, 0, 0))
                win.blit(pygame.transform.scale(endpic, (ScreenWidth, ScreenHeight)), (0, 0))
                DrawText(win, "YOU LOST", 120, (205, 0, 0),200)
                pygame.display.update()
                pygame.time.delay(5000)
                run = False
                updatescore(score)

        pygame.display.update()

def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        DrawText(win, 'Press Any Key To Play', 80, (255,255,255),0)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

win = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption('Reverse Tetris')
main_menu(win)