import pygame
import os
import random
import math
import pathlib
import cv2

pygame.font.init() # carga los fondos de escritura

WIDTH, HEIGHT = 500,700 # dimensiones de la ventana del juego
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT)) # Objeto de la ventana

FPS = 60 # fps del juego

# WHITE = (255,255,255) # definicion del color blanco

CAR_WIDTH, CAR_HEIGHT = 50,100 # dimensiones de los carros
# TRUCK_WIDTH, TRUCK_HEIGHT = 50,200 # dimensiones de los camiones

VEL = 8 # velocidad del carro
VEL_VEHICLES = 3 # velocidad de los vehiculos (obstaculos)
VEL_BACKGROUND = VEL_VEHICLES*7 # velocidad del fondo
VEL_VEHICLE_GENERATION = 80 # entre menor sea mas rapido es la generacion
score = 0 #Variable que lleva el puntaje.
font = pygame.font.Font('freesansbold.ttf',20) #Definimos el tipo de letra y tamaño

# IS_CAR = True # verifica que el objeto sea un carro

YOU_LOSE = pygame.image.load(os.path.join('assets','YOU_LOSE.jpg')) # carga la imagen que se mostrara cuando el jugador pierde
YOU_LOSE = pygame.transform.scale(YOU_LOSE,(WIDTH,HEIGHT)) # escala la imagen al tamaño de la ventana

WHITE_CAR = pygame.image.load(os.path.join('assets','white_car.png')) # carga la imagen del carro blaco
WHITE_CAR = pygame.transform.scale(WHITE_CAR,(CAR_WIDTH,CAR_HEIGHT)) # escala el tañano de la imagen

BACKGROUND = pygame.image.load(os.path.join('assets','road.jpg')) # carga la imagen del fondo, es una carretera
BACKGROUND_HEIGHT = BACKGROUND.get_height() # obtiene la altura del fondo
BACKGROUND = pygame.transform.scale(BACKGROUND,(WIDTH,BACKGROUND_HEIGHT)) # escala la imagen para que el ancho sea del tamaño de la ventana

# WHITE_TRUCK = pygame.image.load(os.path.join('assets','white_truck.png')) # carla la imagen de un camion blanco
# WHITE_TRUCK = pygame.transform.scale(WHITE_TRUCK,(TRUCK_WIDTH,TRUCK_HEIGHT)) # escala la imagen de un camion blanco

CAR = pygame.image.load(os.path.join('assets','car.png')) # carga la imagen del carro
CAR = pygame.transform.scale(CAR,(CAR_WIDTH,CAR_HEIGHT)) # escala la imagen del carro

HIT = pygame.USEREVENT + 1 # crea el evento que sera generado cuando haya una colision
TILES = math.ceil(HEIGHT / BACKGROUND.get_height()) # calcula cuantas imagenes del fondo se deben usar para llenar la ventana

vehicles = [] # guarda los objetos de los vehiculos

pygame.display.set_caption("JIMMED EXPRESSWAY") # pone el nombre de la ventana creada (esta se muestra en la esquina superior izquierda)

cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml" #Selecciona el archivo xml que reconoce caras.
clf = cv2.CascadeClassifier(str(cascade_path)) #Se define el clasificador
video_cap = cv2.VideoCapture(0) #La camara a utilizar es la camara por defecto. Atributo 0.


def draw_window(car, vehicles, lose, displacement):

    """
    funcion que dibuja los objetos que se mostraran en la ventana
    parametros:
    * car: carro del juegador
    * vehicles: lista de vehiculos presentes en el juego
    * lose: bandera que verifica si el jugador no ha perdido
    * displacement: es el desplazamiento que lleva el fondo para generar la sensacion de movimiento de la carretera
    retorno:
    * retorna el desplazamiento actual del fondo
    """
    # verifica si el jugador perdio o no
    if not lose:
        # WINDOW.fill(WHITE)
        # dibuja el fondo las veces necesarias para llenar la ventana
        for i in range(0,TILES+1):
            WINDOW.blit(BACKGROUND, (0,-i*BACKGROUND_HEIGHT+displacement)) 

        displacement += VEL_BACKGROUND # genera el desplazamiento del fondo
        #si el desplazamiento es mas grande el tamaño de cada imagen de la carretera entonces se estan dibujando carreteras fuera 
        # de la ventana, entonces debe reiniciarse para no dibujar imagenes de carretera fuera de la ventana
        if displacement >= BACKGROUND_HEIGHT:
            displacement = 0 
        # dibuja los vehiculos
        for vehicle, type in vehicles:
            WINDOW.blit(type, (vehicle.x,vehicle.y)) 

        WINDOW.blit(CAR,(car.x,car.y)) # dibuja el carro del jugador
        text = font.render("Score: "+str(score),True,(255,255,255))
        WINDOW.blit(text,(50,20))
    else:
        # WINDOW.fill(WHITE)
        WINDOW.blit(YOU_LOSE,(0,0)) # dibuja la imagen que se muestra cuando el jugador pierde

    pygame.display.update() # actualiza los dibujos

    return displacement

    
def handle_vehicles(car, vehicles):
    """
    Funcion que se encarga de manejar las acciones de los vehiculos y como interactuan estos con el carro del jugador y la ventana
    parametros:
    * car: carro del jugador
    * vehicles: vehiculos
    retorno:
    * retorna si hay colision o no
    """

    global score

    # itera por la lista de los vehiculos, extrayendo su objeto y tipo
    for vehicle, type in vehicles:
        # verifica si existe una colision del carro del jugador con un vehiculo
        if car.colliderect(vehicle):
            pygame.event.post(pygame.event.Event(HIT)) # genera el evento HIT cuando hay una colision
            return True
        elif vehicle.y > HEIGHT:
            vehicles.remove((vehicle,type))
            score+=1
        vehicle.y += VEL_VEHICLES
    return False

def random_car_generator(frame_count,x):
    """
    Funcion que se encarga de generar los vehiculos en posiciones aleatorias
    parametros:
    * frame_count: lleva las cuentas de los frames desde que se creo el ultimo vehiculo
    retorno:
    * retorna la actualizacion de la variable frame_count
    """
    frame_count += 1 # actualiza la cantidad de frames que han pasado desde la ultima generacion
    global VEL_VEHICLE_GENERATION # variavle global que maneja la velocidad con la que se generan los vehiculos
    # si se alcanza la cantidad de frames definida en VEL_VEHICLE_GENERATION se genera un nuevo vehiculo
    if frame_count == VEL_VEHICLE_GENERATION:
        up_limit = x+x*0.3
        down_limit = x-x*0.3
        if down_limit > 0 and up_limit < WIDTH - CAR_WIDTH:
            car_x_position = random.randint(int(down_limit),int(up_limit))
        else:
            car_x_position = random.randint(0, WIDTH - CAR_WIDTH)
        vehicles.append((pygame.Rect(car_x_position,-CAR_HEIGHT,CAR_WIDTH,CAR_HEIGHT), WHITE_CAR)) # genera un vehiculo aleatorio 
        return 0 # reinicia la cuenta de los frames
    return frame_count # devuelve la cuenta de los frames

def Is_window_close():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  False
    return True

def key_event(car):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a] and car.x > 0:
        car.x -= VEL
    if keys_pressed[pygame.K_d] and car.x+CAR_WIDTH < WIDTH:
        car.x += VEL

def car_movement(car,x):
     if car.x + CAR_WIDTH < WIDTH and car.x > 0:
        car.x = x
    


def main():
    """
    Funcion principal del juego
    """
    lose = False # bandera que guarda el jugador ha perdido
    run = True # bandera que define si el juego debe seguir corriendo
    displacement = 0 # desplazamiento del fondo para generar sensacion de movimiento de la carretera
    clock = pygame.time.Clock() # creacion de objeto que maneja el tiempo

    white_car = pygame.Rect(0,-CAR_HEIGHT,CAR_WIDTH,CAR_HEIGHT), WHITE_CAR # creacion de un carro blanco al inicio del juego
    # white_truck = pygame.Rect(WIDTH//2,0,TRUCK_WIDTH,TRUCK_HEIGHT) # creacion de un camion blanco

    vehicles.append(white_car) # se agrega el carro a la lista de vehiculos
    # vehicles.append(white_truck) # agrega el camion a la lista de vehiculos

    car = pygame.Rect(3*WIDTH//4,HEIGHT//2,CAR_WIDTH,CAR_HEIGHT) # crea el rectangulo del carro del jugador

    frame_count = 0 # cuenta la cantidad de frames que han pasado desde el ultimo vehiculo creado
    face = (None,None,None,None)
    # bucle principal de juego
    while run:

        clock.tick(FPS)# define los fps del juego

        # se generan obstaculos
        frame_count = random_car_generator(frame_count,car.x)

        # verifica si la ventana no se ha cerrado
        run = Is_window_close()
        
        # si no ha perdido, el juego contiuna
        if not lose:

            ret, video_data = video_cap.read() #Leo de la camara.

            # Flip the video horizontally
            video_data = cv2.flip(video_data, 1)

            gray = cv2.cvtColor(video_data,cv2.COLOR_BGR2GRAY) #Convierto la imagen a escala de grises
            faces = clf.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(30,30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )   # Se detectan las caras

            # manejo de los obstaculos, si hay una colision el jugador pierde
            lose = handle_vehicles(car, vehicles)
            # dibuja todos los objetos en la ventana, de vuelve el desplazamiento actual de las imagenes de la carretera 
            displacement = draw_window(car, vehicles, lose, displacement)
            # verifica las entradas por teclado y define las acciones que se hacen con estas
            #key_event(car)

            maxi = 0
            
            for(x,y,width,height) in faces:
                if  maxi < width*height:
                    maxi = width*height
                    face = (x,y,width,height)

            cv2.rectangle(video_data,(face[0],face[1]),(face[0]+face[2],face[1]+face[3]),(255,0,0),2)
            car_movement(car,face[0])
                #print(x,y,width,height)
            
            cv2.imshow("video_live face detection",video_data)

            # if cv2.waitKey(10) == ord("a"):
            #     break
    video_cap.release()
    cv2.destroyAllWindows()
    pygame.quit() # cierra el juego

            
if __name__ == "__main__":
    main()