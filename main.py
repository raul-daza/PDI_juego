import pygame
import os
import random
import math

pygame.font.init()

WIDTH, HEIGHT = 500,700
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

FPS = 60

WHITE = (255,255,255)

CAR_WIDTH, CAR_HEIGHT = 50,100
TRUCK_WIDTH, TRUCK_HEIGHT = 50,200

VEL = 8
VEL_VEHICLES = 3
VEL_BACKGROUND = VEL_VEHICLES*7
VEL_VEHICLE_GENERATION = 80 # less is faster

IS_CAR = True

YOU_LOSE = pygame.image.load(os.path.join('assets','YOU_LOSE.jpg'))
YOU_LOSE = pygame.transform.scale(YOU_LOSE,(WIDTH,HEIGHT))

WHITE_CAR = pygame.image.load(os.path.join('assets','white_car.png'))
WHITE_CAR = pygame.transform.scale(WHITE_CAR,(CAR_WIDTH,CAR_HEIGHT))

BACKGROUND = pygame.image.load(os.path.join('assets','road.jpg'))
BACKGROUND_HEIGHT = BACKGROUND.get_height()
BACKGROUND = pygame.transform.scale(BACKGROUND,(WIDTH,BACKGROUND_HEIGHT))

# WHITE_TRUCK = pygame.image.load(os.path.join('assets','white_truck.png'))
# WHITE_TRUCK = pygame.transform.scale(WHITE_TRUCK,(TRUCK_WIDTH,TRUCK_HEIGHT))

CAR = pygame.image.load(os.path.join('assets','car.png'))
CAR = pygame.transform.scale(CAR,(CAR_WIDTH,CAR_HEIGHT))

HIT = pygame.USEREVENT + 1
TILES = math.ceil(HEIGHT / BACKGROUND.get_height())

vehicles = []

pygame.display.set_caption("RUN RUN")


def draw_window(car, vehicles, lose, displacement):

    if not lose:
        # WINDOW.fill(WHITE)
        for i in range(0,TILES+1):
            WINDOW.blit(BACKGROUND, (0,-i*BACKGROUND_HEIGHT+displacement))

        displacement += VEL_BACKGROUND
        if displacement >= BACKGROUND_HEIGHT:
            displacement = 0

        for vehicle, type in vehicles:
            WINDOW.blit(type, (vehicle.x,vehicle.y))

        WINDOW.blit(CAR,(car.x,car.y))
    else:
        WINDOW.fill(WHITE)
        WINDOW.blit(YOU_LOSE,(0,0))

    pygame.display.update()

    return displacement

    
def handle_vehicles(car, vehicles):
    for vehicle, type in vehicles:
        if car.colliderect(vehicle):
            pygame.event.post(pygame.event.Event(HIT))
            # vehicles.remove((vehicle,type))
            return True
        elif vehicle.y > HEIGHT:
            vehicles.remove((vehicle,type))
        vehicle.y += VEL_VEHICLES
    return False

def random_car_generator(count):
    count += 1
    global VEL_VEHICLE_GENERATION
    if count%VEL_VEHICLE_GENERATION == 0:
        vehicles.append((pygame.Rect(random.randint(0,WIDTH-CAR_WIDTH),-CAR_HEIGHT,CAR_WIDTH,CAR_HEIGHT), WHITE_CAR))
        return 0
    return count

def main():
    lose = False
    run = True
    displacement = 0
    clock = pygame.time.Clock()

    white_car = pygame.Rect(0,-CAR_HEIGHT,CAR_WIDTH,CAR_HEIGHT), WHITE_CAR
    # white_truck = pygame.Rect(WIDTH//2,0,TRUCK_WIDTH,TRUCK_HEIGHT)

    vehicles.append(white_car)
    # vehicles.append(white_truck)

    car = pygame.Rect(WIDTH//2+WIDTH//4,HEIGHT//2,CAR_WIDTH,CAR_HEIGHT)

    count = 0

    while run:
        clock.tick(FPS)

        count = random_car_generator(count)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not lose:
            lose = handle_vehicles(car, vehicles)
            displacement = draw_window(car, vehicles, lose, displacement)
            

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a] and car.x > 0:
                car.x -= VEL
            if keys_pressed[pygame.K_d] and car.x+CAR_WIDTH < WIDTH:
                car.x += VEL
        # print(len(vehicles))

    pygame.quit()

            
if __name__ == "__main__":
    main()