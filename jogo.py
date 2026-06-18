import pygame
import random
import time

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 600, 600
TILE = 30
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Simplificado")

clock = pygame.time.Clock()

# ---------------- MAPA ----------------
# # = parede | . = pílula | o = super pílula | ' ' = caminho
maze = [
    "####################",
    "#........#.........#",
    "#.####...#...####..#",
    "#o#  #...#...#  #o.#",
    "#.####...#...####..#",
    "#..................#",
    "#######.####.#######",
    "#........#.........#",
    "#.####...#...####..#",
    "#o.................o#",
    "####################"
]

ROWS = len(maze)
COLS = len(maze[0])

# ---------------- CORES ----------------
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# ---------------- JOGADOR ----------------
player = [1, 1]
score = 0
lives = 3

# ---------------- FANTASMAS ----------------
ghosts = [
    {"pos": [10, 5], "color": RED, "home": [10, 5], "vulnerable": False},
    {"pos": [11, 5], "color": PINK, "home": [11, 5], "vulnerable": False},
    {"pos": [10, 6], "color": CYAN, "home": [10, 6], "vulnerable": False},
    {"pos": [11, 6], "color": ORANGE, "home": [11, 6], "vulnerable": False},
]

vulnerable_end = 0

# ---------------- FUNÇÕES ----------------
def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)

            if cell == "#":
                pygame.draw.rect(screen, BLUE, rect)
            elif cell == ".":
                pygame.draw.circle(screen, WHITE, rect.center, 4)
            elif cell == "o":
                pygame.draw.circle(screen, WHITE, rect.center, 8)

def is_wall(x, y):
    if x < 0 or y < 0 or x >= COLS or y >= ROWS:
        return True
    return maze[y][x] == "#"

def move_player(dx, dy):
    nx, ny = player[0] + dx, player[1] + dy

    # túnel horizontal
    if nx < 0:
        nx = COLS - 1
    elif nx >= COLS:
        nx = 0

    if not is_wall(nx, ny):
        player[0], player[1] = nx, ny

def update_pellets():
    global score
    x, y = player

    row = list(maze[y])

    if row[x] == ".":
        row[x] = " "
        score += 10
        maze[y] = "".join(row)

    elif row[x] == "o":
        row[x] = " "
        score += 50
        maze[y] = "".join(row)
        activate_power()

def activate_power():
    global vulnerable_end
    vulnerable_end = time.time() + 7

    for g in ghosts:
        g["vulnerable"] = True

def move_ghosts():
    for g in ghosts:
        x, y = g["pos"]

        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # túnel
            if nx < 0:
                nx = COLS - 1
            elif nx >= COLS:
                nx = 0

            if not is_wall(nx, ny):
                g["pos"] = [nx, ny]
                break

def check_collisions():
    global lives, score

    for g in ghosts:
        if g["pos"] == player:
            if g["vulnerable"]:
                g["pos"] = g["home"]
                score += 200
            else:
                lives -= 1
                player[0], player[1] = 1, 1
                time.sleep(1)

def update_vulnerability():
    global vulnerable_end

    if time.time() > vulnerable_end:
        for g in ghosts:
            g["vulnerable"] = False

def check_win():
    for row in maze:
        if "." in row or "o" in row:
            return False
    return True

# ---------------- LOOP PRINCIPAL ----------------
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_player(-1, 0)
    if keys[pygame.K_RIGHT]:
        move_player(1, 0)
    if keys[pygame.K_UP]:
        move_player(0, -1)
    if keys[pygame.K_DOWN]:
        move_player(0, 1)

    update_pellets()
    move_ghosts()
    update_vulnerability()
    check_collisions()

    draw_maze()

    # desenha jogador
    pygame.draw.circle(screen, YELLOW,
                       (player[0]*TILE + TILE//2, player[1]*TILE + TILE//2), 10)

    # desenha fantasmas
    for g in ghosts:
        color = BLUE if g["vulnerable"] else g["color"]
        x, y = g["pos"]
        pygame.draw.rect(screen, color,
                         (x*TILE, y*TILE, TILE, TILE))

    # HUD
    font = pygame.font.SysFont(None, 24)
    hud = font.render(f"Score: {score}  Lives: {lives}", True, WHITE)
    screen.blit(hud, (10, HEIGHT - 25))

    if check_win():
        win = font.render("YOU WIN!", True, WHITE)
        screen.blit(win, (WIDTH//2 - 40, HEIGHT//2))

    if lives <= 0:
        over = font.render("GAME OVER", True, RED)
        screen.blit(over, (WIDTH//2 - 50, HEIGHT//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()