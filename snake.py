#  Forbid 180 degree turns; Scoreboard: Menu line, Score, Super food;.

import pygame
import random


class Cell:
    def __init__(self, coordinates, dimensions, direction):
        self.rect = pygame.Rect(coordinates, dimensions)
        self.direction = direction


class Snake:
    def __init__(self, offsetXY):
        self.size = 20
        self.cells = [
            Cell(
                (offsetXY[0] + i * self.size + i * 3, offsetXY[1]),
                (self.size, self.size),
                "RIGHT",
            )
            for i in range(4, -1, -1)
        ]
        self.head = self.cells[0]

    def increase(self):
        lastCell = self.cells[len(self.cells) - 1]
        if lastCell.direction == "UP":
            XY = (lastCell.rect.left, lastCell.rect.top + self.size + 3)
        elif lastCell.direction == "DOWN":
            XY = (lastCell.rect.left, lastCell.rect.top - self.size - 3)
        elif lastCell.direction == "RIGHT":
            XY = (lastCell.rect.left - self.size - 3, lastCell.rect.top)
        else:
            XY = (lastCell.rect.left + self.size + 3, lastCell.rect.top)
        self.cells.append(Cell(XY, (self.size, self.size), lastCell.direction))

    def move(self):
        speed = 1
        for cell in self.cells:
            if cell.direction == "RIGHT":
                cell.rect.move_ip(speed, 0)
            elif cell.direction == "LEFT":
                cell.rect.move_ip(-speed, 0)
            elif cell.direction == "UP":
                cell.rect.move_ip(0, -speed)
            else:
                cell.rect.move_ip(0, speed)

    def update(self):
        self.move()
        cellAhead = self.cells[0]
        for cell in self.cells[1:]:
            if cellAhead.direction != cell.direction:
                if cellAhead.rect.left <= cell.rect.left and cell.direction == "RIGHT":
                    cell.direction = cellAhead.direction
                elif cellAhead.rect.left >= cell.rect.left and cell.direction == "LEFT":
                    cell.direction = cellAhead.direction
                elif cellAhead.rect.top >= cell.rect.top and cell.direction == "UP":
                    cell.direction = cellAhead.direction
                elif cellAhead.rect.top <= cell.rect.top and cell.direction == "DOWN":
                    cell.direction = cellAhead.direction
            cellAhead = cell

    def render(self, screen):
        for i, cell in reversed(list(enumerate(self.cells))):
            if i == 0:
                pygame.draw.rect(screen, (246, 82, 16), cell)
                pygame.draw.rect(screen, (13, 27, 30), cell, 1)
            elif i % 2 == 0:
                pygame.draw.rect(screen, (71, 168, 189), cell)
                pygame.draw.rect(screen, (13, 27, 30), cell, 1)
            else:
                pygame.draw.rect(screen, (139, 38, 53), cell)
                pygame.draw.rect(screen, (13, 27, 30), cell, 1)


class HUD:
    def __init__(self):
        self.score = 0
        self.foodEaten = True
        self.supperFoodEaten = True
        self.food = (0, 0)
        self.supperFood = (0, 0)

    def update(self):
        if self.foodEaten and self.supperFoodEaten:
            if random.random() < 0.85:
                self.foodEaten = False
                self.food = (random.randint(50, 1150), random.randint(150, 600))
            else:
                self.supperFoodEaten = False
                self.supperFood = (random.randint(50, 1150), random.randint(150, 600))

    def render(self, screen):
        if not self.foodEaten:
            pygame.draw.circle(screen, (204, 13, 74), self.food, 7)
        if not self.supperFoodEaten:
            pygame.draw.circle(screen, (5, 0, 113), self.supperFood, 8)
        # scoreboard
        myFont = pygame.font.SysFont("Segoe UI", 35)
        scoreTxt = myFont.render("Score: ", True, (11, 60, 73))
        score = myFont.render(str(self.score), True, (11, 60, 73))
        screen.blit(scoreTxt, (30, 14))
        screen.blit(score, (121, 16))
        # border
        pygame.draw.rect(screen, (13, 27, 30), pygame.Rect(0, 70, 1200, 630), 20)


class App:
    def __init__(self):
        pygame.init()
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = None
        self.HUD = None
        self.travelled = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.travelled = 25
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Sneaky")
        self.snake = Snake((500, 400))
        self.HUD = HUD()
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        head = self.snake.cells[0].rect
        food = self.HUD.food
        sFood = self.HUD.supperFood
        if any(
            map(
                lambda point: head.collidepoint(point),
                [
                    (food[0] + 7, food[1]),
                    (food[0] - 7, food[1]),
                    (food[0], food[1] + 7),
                    (food[0], food[1] - 7),
                ],
            )
        ):
            self.HUD.food = (0, 0)
            self.HUD.score += 10
            self.HUD.foodEaten = True
            self.snake.increase()
        elif any(
            map(
                lambda point: head.collidepoint(point),
                [
                    (sFood[0] + 7, sFood[1]),
                    (sFood[0] - 7, sFood[1]),
                    (sFood[0], sFood[1] + 7),
                    (sFood[0], sFood[1] - 7),
                ],
            )
        ):
            self.HUD.supperFood = (0, 0)
            self.HUD.score += 50
            self.HUD.supperFoodEaten = True
        if (
            head.collidelist(self.snake.cells[2:]) != -1
            or head.left < 20
            or head.left > 1165
            or head.top < 85
            or head.top > 665
        ):
            self.running = False
        self.events()
        self.travelled += 1
        self.snake.update()
        self.HUD.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if (
            (keys[pygame.K_w] or keys[pygame.K_UP])
            and self.snake.cells[0].direction != "DOWN"
            and self.travelled >= 24
        ):
            self.travelled = 0
            self.snake.cells[0].direction = "UP"
        elif (
            (keys[pygame.K_a] or keys[pygame.K_LEFT])
            and self.snake.cells[0].direction != "RIGHT"
            and self.travelled >= 24
        ):
            self.travelled = 0
            self.snake.cells[0].direction = "LEFT"
        elif (
            (keys[pygame.K_s] or keys[pygame.K_DOWN])
            and self.snake.cells[0].direction != "UP"
            and self.travelled >= 24
        ):
            self.travelled = 0
            self.snake.cells[0].direction = "DOWN"
        elif (
            (keys[pygame.K_d] or keys[pygame.K_RIGHT])
            and self.snake.cells[0].direction != "LEFT"
            and self.travelled >= 24
        ):
            self.travelled = 0
            self.snake.cells[0].direction = "RIGHT"

    def render(self):
        self.screen.fill((255, 250, 255))
        pygame.draw.rect(self.screen, (247, 244, 243), pygame.Rect(0, 0, 1200, 70))
        self.snake.render(self.screen)
        self.HUD.render(self.screen)
        pygame.display.flip()

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
