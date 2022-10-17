import pygame
import colors

pygame.init()


class Board:
    def __init__(self, size=300, n=3, line=25):
        self.size = size
        self.n = n
        self.side = 0
        self.cells = [[0]*n for _ in range(n)]
        self.line_width = line
        self.player = 0
        self.moves = 0
        self.screen = None

    def get_cell(self, pos):
        # last line
        if pos[0] >= self.size - self.line_width or pos[1] >= self.size - self.line_width:
            return None
        i = int(pos[0] // (self.side + self.line_width))
        j = int(pos[1] // (self.side + self.line_width))
        # if cell already filled
        if self.cells[i][j] != 0:
            return None
        # mouse clicked in grid, not particular cell
        cell = self.get_corner(i, j)
        if pos[0] < cell[0] or pos[1] < cell[1]:
            return None
        return i, j

    def get_corner(self, i, j):
        # get corner of cell without grid
        left = self.line_width + i * (self.side + self.line_width)
        top = self.line_width + j * (self.side + self.line_width)
        return left, top

    def mark(self, i, j):
        if self.player == 0:
            self.cells[i][j] = 1
            self.print_x(i, j, colors.red)
            return
        if self.player == 1:
            self.cells[i][j] = -1
            self.print_o(i, j, colors.blue)
            return

    def print_o(self, i, j, color):
        left, top = self.get_corner(i, j)
        center = (left + self.side//2, top + self.side//2)
        radius = self.side // 3
        width = self.side // 10
        pygame.draw.circle(self.screen, color, center, radius, width)

    def print_x(self, i, j, color):
        left, top = self.get_corner(i, j)
        skip = self.side//6
        width = self.side//8
        pygame.draw.line(self.screen, color, (left+skip, top+skip), (left+self.side-skip, top+self.side-skip), width)
        pygame.draw.line(self.screen, color, (left+self.side-skip, top+skip), (left+skip, top+self.side-skip), width)

    def check_winner(self):
        diag_1, diag_2 = 0, 0
        for j in range(self.n):
            row, col = 0, 0
            diag_1 += self.cells[j][j]
            diag_2 += self.cells[j][self.n - 1 - j]
            for i in range(self.n):
                row += self.cells[j][i]
                col += self.cells[i][j]
            if abs(row) == self.n or abs(col) == self.n:
                return True
        if abs(diag_1) == self.n or abs(diag_2) == self.n:
            return True
        return False

    def print_finish(self, sign):
        myfont = pygame.font.SysFont("microsoftttaile", self.size//12, bold=True)
        label = myfont.render(sign, True, colors.green)
        self.screen.blit(label, (self.size//3.5, self.size//4))
        label_2 = myfont.render("Press mouse button to close", True, colors.green)
        self.screen.blit(label_2, (self.size//20, self.size//3))

    def draw(self):
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Tic-tac-toe")
        self.screen.fill(colors.black)
        self.side = (self.size - ((self.n + 1) * self.line_width)) // self.n
        winner = tied_game = False

        for i in range(self.n):
            for j in range(self.n):
                left, top = self.get_corner(i, j)
                r = pygame.Rect(left, top, self.side, self.side)
                pygame.draw.rect(self.screen, colors.white, r)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if winner or tied_game:
                        return
                    pos = pygame.mouse.get_pos()
                    cell = self.get_cell(pos)
                    if cell is None:
                        break
                    self.mark(*cell)
                    self.moves += 1
                    winner = self.check_winner()
                    if winner:
                        self.print_finish(f"Player {self.player + 1} won!")
                        break
                    tied_game = self.moves >= self.n*self.n
                    if tied_game:
                        self.print_finish("Tied game!")
                        break
                    self.player = (self.player + 1) % 2
                    break
            pygame.display.update()
