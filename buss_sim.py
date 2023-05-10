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
NUM_BUSSTOPS = 10
boardingPerTime = 30
timeBetweenStop = 2*math.pi / NUM_BUSSTOPS / (MAX_SPEED+MAX_SPEED/10)/2
timeOnStop = timeBetweenStop/LAMBDA_POSSION/boardingPerTime
waitTime = 30

#Olika lösningar, inte helt implementerat
modeWait = False
modeWaitSched = False
modeSpeed = False
modeDriveOver = False
modeExtraBus = False
# Initiera pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trafik Simulering")
clock = pygame.time.Clock()

# Buss klass
class Bus:
    def __init__(self, angle): #Klassattributer
        self.angle = angle
        self.speed = 0
        self.stop_time = 0
        self.stopped = False
        self.stopPassed = 0
        self.disTraveled = 0

    def move(self): #Rör på buss 
        if not self.stopped:
            self.angle += self.speed
            self.disTraveled += self.speed
            if self.angle > 2 * math.pi:
                self.angle -= 2 * math.pi

    def check_for_stop(self): #Kollar om man är på ett busstop, och lägger till hur länge bussen ska stanna
            for stop in busStops:
                con = stop.angle - self.angle
                if ((con >= 0) and (con <= self.speed)) or ((con + 2 * math.pi >= 0) and (con + 2 * math.pi <= self.speed)):
                    self.angle = stop.angle
                    self.stop_time += stop.people/boardingPerTime #Lägger till hur läänge bussen ska stanna
                    stop.removePeople(1) #Tar bort folk från busshållsplatsen
                    if modeWait and self.stopped == False:
                        self.stop_time += waitTime
                    self.stopped = True

    def update_stop_time(self, time): #Updaterar stoptiden, samt lite krimskrams
        if self.stopped:
            self.stop_time -= 1
            print("Time: ",time)
            print("Expected time: ",(timeBetweenStop + timeOnStop + waitTime)*(self.stopPassed+1), "\n") #Dumt att använda tid, använd distansen under om något
            print("Distance tracaled: ",self.disTraveled)
            print("Expected dist: ", (MAX_SPEED+MAX_SPEED/10)/2*time*0.97)
            if modeWaitSched:
                if time >= (timeBetweenStop + timeOnStop + waitTime)*(self.stopPassed+1):
                    if self.stop_time <= 0:
                        self.stopped = False
                        self.stop_time = 0
                        self.stopPassed += 1
                else:
                    print("Waited")
            else:
                if self.stop_time <= 0:
                    self.stopped = False
                    self.stop_time = 0
                    self.stopPassed += 1

    def draw(self, surface):
        x = CENTER[0] + RADIUS * math.cos(self.angle)
        y = CENTER[1] + RADIUS * math.sin(self.angle)
        pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), BUS_RADIUS)

class BusStop: #Hållplats klass
    def __init__(self, angle):
        self.angle = angle
        self.people = 0
    
    def addPeople(self): 
        amount = random.expovariate(LAMBDA_POSSION)
        self.people+=amount

    def removePeople(self,time):
        self.people -= min(self.people*time, boardingPerTime*time)

def bunchingScore(buses): #Metod för att betygsätta lösningen för att motverka bunching. Kanske borde lägga till metod för att mäta flöde av människor
    distances = 0
    for bus1 in buses:
        closest = 2 * math.pi
        for bus2 in buses:
            if bus1==bus2:
                continue
        if abs(bus1.angle-bus2.angle)<closest:
            closest=bus1.angle-bus2.angle
        distances += closest
    score = abs(distances - 2*math.pi) #Kan behöva förklaras. Mindre är bättre
    return score

# Skapa bussar
buses = [Bus(2 * math.pi * i / NUM_BUSSES + 0.01) for i in range(NUM_BUSSES)]
# Skapar hållplatser
busStops = [BusStop(2*math.pi * i / NUM_BUSSTOPS) for i in range(NUM_BUSSTOPS)]
# Main loop
running = True
time = 0
if modeWait != True:
    waitTime=0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    time += 1
    # Öka traffikanter på busshållsplatsen
    for BusStop in busStops:
        BusStop.addPeople()

    # Updatera buss positioner
    for i, bus in enumerate(buses):
        bus.speed = random.uniform(MAX_SPEED/10, MAX_SPEED)
        bus.check_for_stop()
        bus.update_stop_time(time)
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

    clock.tick(300)
    if time==5000:
        print(bunchingScore(buses))
        break

pygame.quit()