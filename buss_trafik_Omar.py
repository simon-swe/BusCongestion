import pygame
import math
import random

# Konstanter
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 300
NUM_BUSSES = 10
BUS_RADIUS = 5
MAX_SPEED = 0.005
STOP_INTERVALL = [3*math.pi/4, 5*math.pi/4, 7*math.pi/4]
LAMBDA_POSSION = 2  

# Initiera pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trafik Simulering")
clock = pygame.time.Clock()

# Buss klass
class Bus:
    def __init__(self, angle):
        self.angle = angle
        self.speed = 0
        self.stop_time = 0
        self.stopped = False

    def move(self, speed):
        self.speed = speed
        if not self.stopped:
            self.angle += speed
            if self.angle > 2 * math.pi:
                self.angle -= 2 * math.pi
        return self.angle
    
    def check_for_stop(self):
        if not self.stopped:
            for stop in STOP_INTERVALL:
                if abs(self.angle - stop) < self.speed * 9/10:
                    self.angle = stop
                    self.stop_time = random.expovariate(LAMBDA_POSSION)*60
                    self.stopped = True

    def update_stop_time(self, next_bus):
        if self.stopped:
            self.stop_time -= 1
            distance = abs(self.angle - next_bus.angle)
            if self.stop_time <= 0 and distance >= 2 * math.pi / NUM_BUSSES:
                self.stopped = False

    def draw(self, surface):
        x = CENTER[0] + RADIUS * math.cos(self.angle)
        y = CENTER[1] + RADIUS * math.sin(self.angle)
        pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), BUS_RADIUS)

# Skapa bussar
buses = [Bus(2 * math.pi * i / NUM_BUSSES) for i in range(NUM_BUSSES)]

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Updatera buss positioner
    for i, bus in enumerate(buses):
        next_bus = buses[(i + 1) % NUM_BUSSES] 
        bus.move(random.uniform(MAX_SPEED/10, MAX_SPEED))
        bus.check_for_stop()
        bus.update_stop_time(next_bus)

    # Rita grafik
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (128, 128, 128), CENTER, RADIUS + BUS_RADIUS)
    pygame.draw.circle(screen, (0, 0, 0), CENTER, RADIUS - BUS_RADIUS)
    for stop in STOP_INTERVALL:
        stop_angle = stop
        stop_x = CENTER[0] + RADIUS * math.cos(stop_angle)
        stop_y = CENTER[1] + RADIUS * math.sin(stop_angle)
        pygame.draw.line(screen, (255, 0, 0), (stop_x-10, stop_y), (stop_x+10, stop_y), 2)
        pygame.draw.line(screen, (255, 0, 0), (stop_x, stop_y-10), (stop_x, stop_y+10), 2)
    for bus in buses:
        bus.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()