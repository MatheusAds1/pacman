import pygame

MAGENTA = (255, 0, 255)
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)

pygame.init()

tam_x = 640
tam_y = 480
width = 5

tela = pygame.display.set_mode((tam_x, tam_y), 0)

while True:
    # Calcula as regras


    # Pinta
    tela.fill(PRETO)
    pygame.draw.line(tela, AMARELO, (40, 200), (300, 100), width)
    pygame.draw.line(tela, AMARELO, (600, 200), (300, 100), width)
    pygame.draw.rect(tela, AMARELO, ((40, 200), (560, 200)), 5)
    pygame.display.update()

    # Eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
