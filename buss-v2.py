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
LAMBDA_POSSION = 2  
modeFrontDist = False
NUM_BUSSTOPS = 10
boardingPerTime = 20

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

    def move(self):
        if not self.stopped:
            self.angle += self.speed
            if self.angle > 2 * math.pi:
                self.angle -= 2 * math.pi
        return self.angle
    
    def check_for_stop(self):
            for stop in busStops:
                if abs(self.angle - stop.angle) < self.speed:
                    self.angle = stop.angle
                    self.stop_time += stop.people/boardingPerTime
                    stop.removePeople()
                    self.stopped = True

    def update_stop_time(self):
        if self.stopped:
            self.stop_time -= 1
            if modeFrontDist: # Här ska mode för nära 
                return 0 
            else:
                if self.stop_time <= 0:
                    self.stopped = False
                    self.stop_time = 0

    def draw(self, surface):
        x = CENTER[0] + RADIUS * math.cos(self.angle)
        y = CENTER[1] + RADIUS * math.sin(self.angle)
        pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), BUS_RADIUS)

class BusStop:
    def __init__(self, angle):
        self.angle = angle
        self.people = 0
    
    def addPeople(self):
        amount = random.expovariate(LAMBDA_POSSION)
        self.people+=amount

    def removePeople(self):
        self.people -= min(self.people, boardingPerTime)

# Skapa bussar
buses = [Bus(2 * math.pi * i / NUM_BUSSES) for i in range(NUM_BUSSES)]
# Skapar hållplatser
busStops = [BusStop(2*math.pi * i / NUM_BUSSTOPS) for i in range(NUM_BUSSTOPS)]
# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Öka traffikanter på busshållsplatsen
    for BusStop in busStops:
        BusStop.addPeople()

    # Updatera buss positioner
    for i, bus in enumerate(buses):
        bus.speed = random.uniform(MAX_SPEED/10, MAX_SPEED)
        bus.check_for_stop()
        bus.update_stop_time()
        bus.move()
        

    # Rita grafik 
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (128, 128, 128), CENTER, RADIUS + BUS_RADIUS)
    pygame.draw.circle(screen, (0, 0, 0), CENTER, RADIUS - BUS_RADIUS)
    for stop in busStops:
        stop_angle = stop.angle
        stop_x = CENTER[0] + RADIUS * math.cos(stop_angle)
        stop_y = CENTER[1] + RADIUS * math.sin(stop_angle)
        pygame.draw.line(screen, (255, 0, 0), (stop_x-10, stop_y), (stop_x+10, stop_y), 2)
        pygame.draw.line(screen, (255, 0, 0), (stop_x, stop_y-10), (stop_x, stop_y+10), 2)
    for bus in buses:
        bus.draw(screen)
    pygame.display.flip()

    clock.tick(500)

pygame.quit()