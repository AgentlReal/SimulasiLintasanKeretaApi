import pygame
from pygame.locals import *
import math
import time
import pygame.locals
from shapely.geometry import LineString

# Inisialisasi pygame
pygame.init()

# Dimensi layar
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aljabar Boolean Pada Gerbang Kereta Api")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
DARK_GREY = (125, 125, 125)

# Class untuk kereta


class Train:
    def __init__(self, track_points, speed):
        # List of (x, y) tuples untuk lintasan
        self.track_points = track_points
        self.current_index = 0  # Indeks titik lintasan saat ini
        self.speed = speed
        self.x, self.y = track_points[0]  # Posisi awal
        self.angle = 0  # Sudut orientasi kereta
        self.train_sprite_left = pygame.image.load('images/train.png')
        self.train_sprite_left_rect = self.train_sprite_left.get_rect()

        self.train_sprite_rotated = pygame.transform.rotate(
            self.train_sprite_left, self.angle)
        self.train_sprite_rotated_rect = self.train_sprite_rotated.get_rect()

    def draw(self):
        screen.blit(self.train_sprite_rotated, self.train_sprite_rotated_rect)

    def update(self):
        # Update Posisi Kereta
        self.train_sprite_rotated = pygame.transform.rotate(
            self.train_sprite_left, self.angle)
        self.train_sprite_rotated_rect = self.train_sprite_rotated.get_rect()
        self.train_sprite_rotated_rect.center = (self.x, self.y)

        # Ambil titik tujuan berikutnya
        if self.current_index < len(self.track_points) - 1:
            next_point = self.track_points[self.current_index + 1]
        else:
            # Reset ke titik awal (looping)
            self.x, self.y = self.track_points[0]
            self.current_index = 0
            next_point = self.track_points[self.current_index + 1]

        # Hitung vektor ke titik berikutnya
        dx = next_point[0] - self.x
        dy = next_point[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Perbarui posisi jika belum mencapai titik berikutnya
        if distance > self.speed:
            # Normalisasi vektor dan gerakkan kereta
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            # Hitung sudut orientasi
            if int(dy) == 0 or int(dy) == 1:
                if next_point[0] > self.x:
                    self.angle = 0
                else:
                    self.angle = 180
            elif int(dx) == 0 or int(dx) == 1:
                if next_point[1] > self.y:
                    self.angle = 270
                else:
                    self.angle = 90
            else:
                self.angle = ((math.atan2(dy, dx) * 10) // 1) * -6
        else:
            # Pindah ke titik berikutnya
            self.current_index += 1


class Car:
    def __init__(self, track_points, speed, gerbangs, reverse=False):
        # List of (x, y) tuples untuk lintasan
        self.gerbangs = gerbangs
        self.track_points = track_points
        self.current_index = 0  # Indeks titik lintasan saat ini
        self.default_speed = speed
        self.speed = self.default_speed
        if reverse:
            self.track_points.reverse()
        self.x, self.y = self.track_points[0]  # Posisi awal
        self.angle = 0  # Sudut orientasi kereta
        self.car_sprite = pygame.image.load('images/sedan.png')
        self.car_sprite_right = pygame.transform.scale(
            self.car_sprite, (self.car_sprite.get_width() * 0.1, self.car_sprite.get_height() * 0.1))
        self.car_sprite_right_rect = self.car_sprite_right.get_rect()

        self.car_sprite_rotated = pygame.transform.rotate(
            self.car_sprite_right, self.angle)
        self.car_sprite_rotated_rect = self.car_sprite_rotated.get_rect()

    def draw(self):
        screen.blit(self.car_sprite_rotated, self.car_sprite_rotated_rect)

    def update(self):
        # Update Posisi Kereta
        self.car_sprite_rotated = pygame.transform.rotate(
            self.car_sprite_right, self.angle)
        self.car_sprite_rotated_rect = self.car_sprite_rotated.get_rect()
        self.car_sprite_rotated_rect.center = (self.x, self.y)

        # Ambil titik tujuan berikutnya
        if self.current_index < len(self.track_points) - 1:
            next_point = self.track_points[self.current_index + 1]
        else:
            # Reset ke titik awal (looping)
            self.x, self.y = self.track_points[0]
            self.current_index = 0
            next_point = self.track_points[self.current_index + 1]

        # Berhenti jika ada gerbang di depan
        for gerbang in self.gerbangs:
            if gerbang.x > self.x - 80 and gerbang.x < self.x + 80 and gerbang.y > self.y - 80 and gerbang.y < self.y + 80:
                if gerbang.state in ["closed", "opening", "closing"]:
                    self.speed = 0
                else:
                    self.speed = self.default_speed

        # Hitung vektor ke titik berikutnya
        dx = next_point[0] - self.x
        dy = next_point[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Perbarui posisi jika belum mencapai titik berikutnya
        if distance > self.speed:
            # Normalisasi vektor dan gerakkan kereta
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            # Hitung sudut orientasi
            if int(dy) == 0 or int(dy) == 1:
                if next_point[0] > self.x:
                    self.angle = 0
                else:
                    self.angle = 180
            elif int(dx) == 0 or int(dx) == 1:
                if next_point[1] > self.y:
                    self.angle = 270
                else:
                    self.angle = 90
            else:
                self.angle = ((math.atan2(dy, dx) * 10) // 1) * -6
        else:
            # Pindah ke titik berikutnya
            self.current_index += 1


class Gate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "open"  # Pilihan: open, closing, closed, opening
        self.timer_active = False
        self.timer_start = 0

    def draw(self):
        if self.state == "open":
            pygame.draw.rect(screen, GREEN, (self.x - 10, self.y - 20, 40, 10))
            pygame.draw.rect(screen, GREEN, (self.x - 10, self.y + 20, 40, 10))
        elif self.state == "closed":
            pygame.draw.rect(screen, RED, (self.x - 10, self.y - 20, 40, 10))
            pygame.draw.rect(screen, RED, (self.x - 10, self.y + 20, 40, 10))
        elif self.state in ["closing", "opening"]:
            pygame.draw.rect(screen, GRAY, (self.x - 10, self.y - 20, 40, 10))
            pygame.draw.rect(screen, GRAY, (self.x - 10, self.y + 20, 40, 10))

    def update(self, trains, current_time):
        # Jika kereta mendekati gerbang dan melewati gerbang
        # if train.x + 100 > self.x - 60 and train.x < self.x + 100 and train.y > self.y - 60 and train.y < self.y + 60:
        if trains:
            for train in trains:
                if train.x > self.x - 160 and train.x < self.x + 160 and train.y > self.y - 160 and train.y < self.y + 160:
                    if self.state == "open":
                        self.state = "closing"
                        self.timer_active = True
                        self.timer_start = current_time
                else:
                    if self.state == "closed":
                        self.state = "opening"
                        self.timer_active = True
                        self.timer_start = current_time
        elif self.state in ["closed", "closing"]:
            self.state = "opening"
            self.timer_active = True
            self.timer_start = current_time

        # Timer logika
        if self.timer_active:
            if self.state == "closing" and current_time - self.timer_start > 0.5:
                self.state = "closed"
                self.timer_active = False
            elif self.state == "opening" and current_time - self.timer_start > 0.5:
                self.state = "open"
                self.timer_active = False


# Fungsi menggambar lintasan rel dan jalan raya
def draw_track(track_points):
    for i in range(len(track_points) - 1):
        pygame.draw.line(
            screen, DARK_GREY, track_points[i], track_points[i + 1], 20)
        pygame.draw.line(
            screen, ORANGE, track_points[i], track_points[i + 1], 2)


def draw_roads(road_points):
    for i in range(len(road_points)):
        for j in range(len(road_points[i]) - 1):
            pygame.draw.line(
                screen, BLACK, road_points[i][j], road_points[i][j + 1], 20)
            pygame.draw.line(
                screen, WHITE, road_points[i][j], road_points[i][j + 1], 2)


# Inisialisasi
bg = pygame.transform.scale(pygame.image.load("images/bg.jpg"), (pygame.image.load(
    "images/bg.jpg").get_width() * 1.4, pygame.image.load("images/bg.jpg").get_height() * 1.4))
track = [
    (1200, 150),
    (0, 575)
]

roads = [
    [(750, 1100),
     (1125, -100)], [(50, 1100),
                     (350, -100)]
]

gates = []

trains = []
cars = [Car(roads[0], speed=8, gerbangs=gates), Car(
    roads[1], speed=8, gerbangs=gates, reverse=True)]


# Menambahkan Gerbang jika terjadi persimpangan
for i in range(len(roads)):
    for j in range(len(roads[i]) - 1):
        for k in range(len(track) - 1):
            garis1 = LineString([roads[i][j], roads[i][j+1]])
            garis2 = LineString([track[k], track[k+1]])
            if garis1.intersects(garis2):
                persimpangan = garis1.intersection(garis2)
                gates.append(Gate(persimpangan.x, persimpangan.y))


# Main loop
running = True
while running:
    screen.fill(WHITE)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not trains:
                    trains.append(Train(track, speed=2.5))
            if event.key == K_r:
                if trains:
                    del trains[0]

    current_time = time.time()

    # Gambar elemen
    draw_roads(roads)
    draw_track(track)  # Gambar lintasan
    if gates:
        for gate in gates:
            gate.update(trains, current_time)
            gate.draw()
    if trains:
        for train in trains:
            train.update()
            train.draw()  # Gambar kereta
    if cars:
        for car in cars:
            car.update()
            car.draw()

    # Update layar
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
