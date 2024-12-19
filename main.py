import pygame
import numpy as np
import time

# Константы
WIDTH, HEIGHT = 800, 600
POINT_RADIUS = 5
EPSILON = 30  # Радиус поиска
MIN_SAMPLES = 3  # Минимальное количество соседей для образования кластера

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)    # Ядро кластера
YELLOW = (255, 255, 0) # Граница кластера
RED = (255, 0, 0)      # Шум
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255),
          (255, 165, 0), (128, 0, 128), (255, 20, 147)]  # Цвета кластеров

# Класс точки
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flag_color = WHITE  # Цвет "флажка"
        self.cluster_id = -1  # -1 для нерассмотренных точек

# Функции
def draw_points(screen, points):
    for point in points:
        pygame.draw.circle(screen, point.flag_color, (point.x, point.y), POINT_RADIUS)

def distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def region_query(points, point):
    return [p for p in points if distance(p, point) <= EPSILON]

def expand_cluster(points, point, neighbors, cluster_id):
    point.cluster_id = cluster_id
    point.flag_color = GREEN  # Ядро кластера

    i = 0
    while i < len(neighbors):
        neighbor = neighbors[i]
        if neighbor.cluster_id == -1:  # Если точка раньше не рассматривалась
            neighbor.cluster_id = cluster_id
            neighbor.flag_color = YELLOW  # Граничная точка

            neighbor_neighbors = region_query(points, neighbor)
            if len(neighbor_neighbors) >= MIN_SAMPLES:
                neighbors += neighbor_neighbors
        i += 1

def dbscan(points):
    cluster_id = 0
    for point in points:
        if point.cluster_id != -1:  # Если точка уже присоединена к кластеру
            continue

        neighbors = region_query(points, point)
        if len(neighbors) < MIN_SAMPLES:
            point.flag_color = RED  # Шумовая точка
        else:
            expand_cluster(points, point, neighbors, cluster_id)
            screen.fill(BLACK)
            assign_cluster_colors(points)
            draw_points(screen, points)

            pygame.display.flip()
            time.sleep(0.5)
            cluster_id += 1

def assign_cluster_colors(points):
    num_clusters = max(p.cluster_id for p in points if p.cluster_id != -1)
    for point in points:
        if point.cluster_id != -1:
            color_index = point.cluster_id % len(COLORS)
            point.flag_color = COLORS[color_index]

# Основной код
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DBSCAN Clustering Visualization")
points = []
running = True

while running:
    screen.fill(BLACK)
    draw_points(screen, points)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            points.append(Point(x, y))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:

                dbscan(points)  # Помечаем точки "флажками" (ядро, граница, шум)

pygame.quit()