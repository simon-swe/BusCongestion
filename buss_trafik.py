import pygame
import math
import random

# Konstanter
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 300
NUM_BUSSES = 10
BUS_RADIUS = 5
MAX_SPEED = 0.0005
STOP_INTERVALL = [3*math.pi/4, 5*math.pi/4, 7*math.pi/4]
LAMBDA_POSSION = 7  
BUS_INTERVALL = 5
BUS_STARTSPEED = math.pi/3600
NUM_BUSSTOPS = 10
boardingPerTime = 5

# Initiera pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trafik Simulering")
clock = pygame.time.Clock()

# Buss klass
class Bus:
    def __init__(self, angle, speed):
        self.angle = angle
        self.speed = speed
        self.stop_time = 0

    def move(self): #Lägg till så att den kollar för först bussar framför och sen hållplatser
        
        self.angle += min(self.speed, distanceInFront())
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def draw(self, surface):
        x = CENTER[0] + RADIUS * math.cos(self.angle)
        y = CENTER[1] + RADIUS * math.sin(self.angle)
        pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), BUS_RADIUS)
    
    def start(self):
        self.speed=BUS_STARTSPEED

# Buss klass
class BusStop:
    def _init_(self, angle, people):
        self.angle = angle
        self.people = 0
    
    def addPeople(self):
        amount = random.poission(lam=LAMBDA_POSSION)
        self.people+=amount

    def removePeople(self):
        self.people -= min(self.people, boardingPerTime)
        if self.people<boardingPerTime:
            return boardingPerTime - self.people
        else:
            return 0

def distanceInFront(busStops,bus):
    distanceInFront = float('inf')
    for i in busStops:
        if bus.angle>i.angle:
            if math.abs(i.angle-bus.angle)<distanceInFront:
                distanceInFront = i.angle-bus.angle

        if math.abs(i.angle-bus.angle)<distanceInFront:
            distanceInFront = i.angle-bus.angle

def onBusStop(busStops, bus):
    for busStop in busStops:
        if busStop.angle == bus.angle:
            return (True, busStops.index(busStop))
    return False    
    

# Skapa bussar
buses = [Bus(2 * math.pi * i / NUM_BUSSES, BUS_STARTSPEED) for i in range(NUM_BUSSES)]
busStops = [BusStop(2*math.pi * i / NUM_BUSSTOPS, 0) for i in range(NUM_BUSSTOPS)]
# Main loop
running = True
runTime = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ++runTime

    # Öka hållplatsens människor
    for BusStop in busStops:
        BusStop.addPeople()

    # Updatera buss positioner
    for bus in buses:
        status = onBusStop(bus,busStops)
        if (status[0]):
            bus.move(busStops(status[1]))fdv gh
        bus.move()

    # Rita bussarna
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (128, 128, 128), CENTER, RADIUS + BUS_RADIUS)
    pygame.draw.circle(screen, (0, 0, 0), CENTER, RADIUS - BUS_RADIUS)
    for bus in buses:
        bus.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()