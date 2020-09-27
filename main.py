import pygame
from random import  random
from math import sqrt


SCREEN_SIZE = (1280, 720)

class Vector:
    """"""

    def __init__(self, x, y = None):
        """"""
        if y is not None:
            self.x = x
            self.y = y
        else:
            self.x = x[0]
            self.y = x[1]

    def __sub__(self, other):
        """"""
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """"""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        """"""
        return Vector(self.x * other.x, self.y * other.y)

    def int_pair(self):
        """"""
        return (int(self.x), int(self.y))

    def multiply(self, k):
        """"""
        return Vector(self.x * k, self.y * k)

    def __len__(self, other):
        """"""
        return int(sqrt(self.x ** 2 + self.y ** 2))


class Line:
    """"""
    def __init__(self):
        """"""
        self.points = []
        self.speed = []

    def add_point(self, new_point, new_speed):
        """"""
        self.points.append(new_point)
        self.speed.append(new_speed)

    def set_points(self):
        """"""
        for i in range(len(self.points)):
            self.points[i] += self.speed[i]
            if self.points[i].x > SCREEN_SIZE[0] or self.points[i].x < 0:
                self.speed[i] = Vector(- self.speed[i].x, self.speed[i].y)
            if self.points[i].y > SCREEN_SIZE[0] or self.points[i].y < 0:
                self.speed[i] = Vector(self.speed[i].x, self.speed[i].y)


    def draw_points(self, style="points", width=4, color=(255, 255, 255)):
        """"""
        if style == "line":
            for point_number in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, (int(self.points[point_number].x), int(self.points[point_number].y)),
                                 (int(self.points[point_number + 1].x), int(self.points[point_number + 1].y)), width)
        elif style == "points":
            for point in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(point[0]), int(point[1])), width)


class Joint(Line):
    """"""

    def __init__(self, quanity):
        """"""
        super().__init__()
        self.count = quanity

    def get_point(self, points, alpha, deg=None):
        """"""
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        """"""
        alpha = 1 / self.count
        result = []
        for i in range(self.count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_joint(self):
        """"""
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append(((self.points[i] + self.points[i + 1])) * 0.5)
            pnt.append(self.points[i + 1])
            pnt.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            result.extend(self.get_points(pnt))
        return result

def display_help():
    """"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))



if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    all_points = Line()
    speeds = Joint(steps)
    show_help = False
    pause = False
    color_param = 0
    color = pygame.Color(0)


    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    all_points = Line()
                    speeds = Joint(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                all_points.add_point(Vector(event.pos[0], event.pos[1]), Vector(random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)

        all_points.draw_points(all_points.points)
        if not pause:
            all_points.set_points()
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)