import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as plt
# Konstanter
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 300
NUM_BUSSES = 8
BUS_RADIUS = 5
MAX_SPEED = 0.005
LAMBDA_POSSION = 0.5
NUM_BUSSTOPS = 8
boardingPerTime = 20
timeBetweenStop = 2*math.pi / NUM_BUSSTOPS / (MAX_SPEED+MAX_SPEED/10)/2
timeOnStop = timeBetweenStop/LAMBDA_POSSION/boardingPerTime
waitTime = 3
busAdded = False

#Olika lösningar, inte helt implementerat
modeWait = False #Fungerar: Väntar lite på varje hållplats
modeWaitSched = False #Fungerar: Väntar in sin beräknade avgång
modeExtraBus = False #Fungerar: Lägger till en till buss
# Initiera pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trafik Simulering")
clock = pygame.time.Clock()

# Buss klass
class Bus:
    def __init__(self, angle): #Klassattribute r
        self.angle = angle
        self.speed = 0
        self.stop_time = 0.0
        self.stopped = False
        self.stopPassed = 0
        self.disTraveled = 0

    def move(self): #Rör på buss 
        if not self.stopped:
            self.angle += self.speed
            self.disTraveled += self.speed
            if self.angle > 2 * math.pi:
                self.angle -= 2 * math.pi
            self.stop_time = 0

    def check_for_stop(self): #Kollar om och hur länge bussen ska stanna
            for stop in busStops:
                con = stop.angle - self.angle
                if ((con >= 0) and (con <= self.speed)) or ((con + 2 * math.pi >= 0) and
                                                             (con + 2 * math.pi <= self.speed)):
                    self.angle = stop.angle
                    if self.stopped == False:
                        self.stop_time += abs(waitTime - stop.people/boardingPerTime)
                    else:
                        self.stop_time += stop.people/boardingPerTime
                    stop.people = 0
                    print("\n",stop.people)
                    self.stopped = True
                    

    def update_stop_time(self, time): #Updaterar stoptiden
        if self.stopped:
            self.stop_time -= 1
            if modeWaitSched:
                if self.disTraveled < (MAX_SPEED+MAX_SPEED/10)/2*time*timeBetweenStop/(timeBetweenStop+timeOnStop+waitTime):
                    if self.stop_time <= 0:
                        self.stopped = False
                        self.stop_time = 0
                        self.stopPassed += 1
                else:
                    print("Waited")
            else:
                if self.stop_time <= 0:
                    self.stopped = False
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

    def removePeople(self):
        self.people -= min(self.people, boardingPerTime)
        

def bunchingScore(buses): #Betygsätter lösningen
    distances = 0
    for bus1 in buses:
        closest = 2 * math.pi
        for bus2 in buses:
            if bus1==bus2:
                continue
            if abs(bus1.angle-bus2.angle)<closest:
                closest=abs(bus1.angle-bus2.angle)
        distances += abs(closest-2*math.pi/NUM_BUSSES)
    score = abs(distances) #Kan behöva förklaras. Mindre är bättre
    return score

# Skapa bussar
if modeExtraBus:
    ++NUM_BUSSES
    buses = [Bus(2 * math.pi * i / NUM_BUSSES + 0.01) for i in range(NUM_BUSSES)]
else:
    buses = [Bus(2 * math.pi * i / NUM_BUSSES + 0.01) for i in range(NUM_BUSSES)]
# Skapar hållplatser
busStops = [BusStop(2*math.pi * i / NUM_BUSSTOPS) for i in range(NUM_BUSSTOPS)]

bunchingScores = []

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

    if time==15000: #Bestämmer hur länge programmet kör (iterationer)
        print(busAdded) #Om man har lagt till 
        break
    
    if time%100==0:
        bunchingScores.append((bunchingScore(buses), time))
    clock.tick(200)

for i in bunchingScores:
    print("Score: ", i[0], " Vid tid: ", i[1])
print("Tillagd buss: ", busAdded)
pygame.quit()

# Dela i två listor
deviation = [x[0] for x in bunchingScores]
time = [x[1] for x in bunchingScores]

# Omvandla till np array
deviation_np = np.array(deviation)
time_np = np.array(time)

# Plotta värdet
plt.plot(time_np, deviation_np, label="bunchingScores")
plt.xlabel("tid")
plt.ylabel("bunchingScores")
plt.legend()
plt.title("modeWait") 
plt.grid()
plt.show()