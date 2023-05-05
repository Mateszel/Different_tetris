import numpy as np
import pygame


BLOCKS = [[[10, 11, 12, 13], [7, 12, 17, 22]],
          [[7, 12, 13, 17], [11, 12, 13, 17], [7, 11, 12, 13], [7, 11, 12, 17]],
          [[10, 11, 12, 13, 14, 15, 17, 19], [1, 2, 7, 11, 12, 17, 21, 22],
          [5, 7, 9, 10, 11, 12, 13, 14], [2, 3, 7, 12, 13, 17, 22, 23]]]


class Shape:

    def __init__(self, x, y):
        self.type = np.random.randint(0, len(BLOCKS))
        self.color = tuple(np.random.randint(100, 255, 3))
        self.rotation = np.random.randint(0, len(BLOCKS[self.type]))
        self.x = x
        self.y = y

    def rotate(self, right=1):
        self.rotation = (self.rotation + right) % len(BLOCKS[self.type])

    def image(self):
        return BLOCKS[self.type][self.rotation]


class Game:
    scale = 30
    x = 40
    y = 40

    def __init__(self, height=15, width=25, n_blocks=15):
        self.map = [[0 for y in range(width)] for z in range(height)]
        self.figures = []
        self.current_figure = 0
        self.n_blocks = n_blocks
        self.height = height
        self.width = width
        self.create_figures()

    def create_figures(self):
        for z in range(self.n_blocks):
            collides = True
            while collides:
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)
                block = Shape(x, y)
                collides = self.collides(block)
            self.figures.append(block)
            self.refresh_map(block)

    def collides(self, block):
        collision = False
        for i in range(5):
            for j in range(5):
                if i * 5 + j in block.image():
                    if i + block.y > self.height - 1 or \
                            i + block.y < 0 or \
                            j + block.x > self.width - 1 or \
                            j + block.x < 0 or \
                            self.map[i + block.y][j + block.x] != 0:
                        collision = True
        return collision

    def refresh_map(self, block, add=True):
        for y in range(5):
            for z in range(5):
                if y * 5 + z in block.image():
                    if add == True:
                        self.map[y + block.y][z + block.x] = 1
                    else:
                        self.map[y + block.y][z + block.x] = 0

    def select_previous(self):
        self.current_figure = (self.current_figure - 1) % self.n_blocks

    def select_next(self):
        self.current_figure = (self.current_figure + 1) % self.n_blocks

    def rotate(self, right=1):
        current_fig = self.figures[self.current_figure]
        self.refresh_map(current_fig, add=False)
        old_rotation = current_fig.rotation
        current_fig.rotate(right)
        if self.collides(current_fig):
            current_fig.rotation = old_rotation
        self.refresh_map(current_fig)

    def go_side(self, dx):
        current_fig = self.figures[self.current_figure]
        self.refresh_map(current_fig, add=False)
        old_x = current_fig.x
        current_fig.x += dx
        if self.collides(current_fig):
            current_fig.x = old_x
        self.refresh_map(current_fig)

    def go_vertical(self, dy):
        current_fig = self.figures[self.current_figure]
        self.refresh_map(current_fig, add=False)
        old_y = current_fig.y
        current_fig.y += dy
        if self.collides(current_fig):
            current_fig.y = old_y
        self.refresh_map(current_fig)


pygame.init()
NET = (255, 255, 255)
BACKGROUND = (0, 0, 0)
window_size = (820, 600)
window_screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tetris but different")
clock = pygame.time.Clock()
fps = 30
counter = 0
is_finished = False
game = Game()

while not is_finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                game.rotate(right=1)
            if event.key == pygame.K_z:
                game.rotate(right=-1)
            if event.key == pygame.K_a:
                game.select_previous()
            if event.key == pygame.K_d:
                game.select_next()
            if event.key == pygame.K_UP:
                game.go_vertical(-1)
            if event.key == pygame.K_DOWN:
                game.go_vertical(1)
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
    window_screen.fill(BACKGROUND)
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(window_screen, NET, [game.x + game.scale * j, game.y + game.scale * i, game.scale, game.scale], 1)
    for idx, figure in enumerate(game.figures):
        for i in range(5):
            for j in range(5):
                z = i * 5 + j
                if z in figure.image():
                    if idx != game.current_figure:
                        pygame.draw.rect(window_screen, figure.color,
                                         [game.x + game.scale * (j + figure.x) + 1,
                                          game.y + game.scale * (i + figure.y) + 1,
                                          game.scale - 2, game.scale - 2])
                    else:
                        pygame.draw.rect(window_screen, figure.color,
                                         [game.x + game.scale * (j + figure.x) + 1,
                                          game.y + game.scale * (i + figure.y) + 1,
                                          game.scale - 2, game.scale - 2], width=5)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
