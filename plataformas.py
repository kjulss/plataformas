import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)

# Tamaño de la ventana
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Plataformas Subiendo")

# Configuración del jugador
jugador_width = 50
jugador_height = 60
jugador_x = ANCHO // 2 - jugador_width // 2
jugador_y = ALTO - jugador_height - 100
jugador_vel = 5
gravedad = 0.8  # Gravedad ajustada
velocidad_y = 0
en_suelo = False

# Plataforma
plataformas = []
plataforma_width = 100
plataforma_height = 20
plataforma_vel_inicial = 3  # Velocidad inicial de las plataformas (más rápida)
plataforma_vel = plataforma_vel_inicial  # Se actualiza con el tiempo

# Fuente de texto
fuente = pygame.font.SysFont(None, 36)

def dibujar_jugador(x, y):
    pygame.draw.rect(pantalla, AZUL, (x, y, jugador_width, jugador_height))

def dibujar_plataformas():
    for plataforma in plataformas:
        pygame.draw.rect(pantalla, VERDE, plataforma)

def crear_plataforma():
    x = random.randint(0, ANCHO - plataforma_width)
    y = ALTO  # Comienza desde el suelo
    return pygame.Rect(x, y, plataforma_width, plataforma_height)

def reiniciar_juego():
    global jugador_x, jugador_y, velocidad_y, plataformas, plataforma_vel
    jugador_x = ANCHO // 2 - jugador_width // 2
    jugador_y = ALTO - jugador_height - 100
    velocidad_y = 0
    plataformas = [crear_plataforma() for _ in range(5)]
    plataforma_vel = plataforma_vel_inicial  # Reiniciar la velocidad de las plataformas

# Bucle principal del juego
reiniciar_juego()

# Contador para aumentar la velocidad de las plataformas gradualmente
tiempo = 0

while True:
    pantalla.fill(BLANCO)
    
    # Detectar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtener teclas presionadas
    teclas = pygame.key.get_pressed()
    
    # Movimiento del jugador
    if teclas[pygame.K_LEFT]:
        jugador_x -= jugador_vel
    if teclas[pygame.K_RIGHT]:
        jugador_x += jugador_vel

    # Salto
    if teclas[pygame.K_SPACE] and en_suelo:
        velocidad_y = -12  # Ajuste de altura de salto
        en_suelo = False
    
    # Aplicar gravedad solo si el jugador no está en el suelo
    if not en_suelo:
        velocidad_y += gravedad
    jugador_y += velocidad_y
    
    # Colisión con las plataformas
    en_suelo = False
    for plataforma in plataformas:
        if plataforma.colliderect(pygame.Rect(jugador_x, jugador_y, jugador_width, jugador_height)) and velocidad_y > 0:
            velocidad_y = 0
            jugador_y = plataforma.top - jugador_height
            en_suelo = True
            break

    # Mover plataformas hacia arriba
    for i in range(len(plataformas)):
        plataformas[i].y -= plataforma_vel
        # Si la plataforma se ha salido de la pantalla, la regeneramos
        if plataformas[i].y + plataforma_height < 0:
            plataformas[i] = crear_plataforma()

    # Si el jugador cae al suelo, reiniciar juego
    if jugador_y >= ALTO - jugador_height:
        reiniciar_juego()

    # Evitar que el jugador se salga de la pantalla
    if jugador_x < 0:
        jugador_x = 0
    if jugador_x > ANCHO - jugador_width:
        jugador_x = ANCHO - jugador_width

    # Dibujar la plataforma y el jugador
    dibujar_plataformas()
    dibujar_jugador(jugador_x, jugador_y)
    
    # Aumentar gradualmente la velocidad de las plataformas con el tiempo
    tiempo += 1
    if tiempo % 400 == 0:  # Cada 400 ciclos de juego, aumentamos la velocidad
        plataforma_vel += 0.3  # Aumento más rápido

    # Actualizar la pantalla
    pygame.display.update()

    # Limitar la tasa de cuadros por segundo
    pygame.time.Clock().tick(60)
