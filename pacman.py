import pygame

MAGENTA = (255, 0, 255)
PRETO = (0, 0, 0)
VELOCIDADE = 0.1

pygame.init()

tam_x = 640
tam_y = 480

tela = pygame.display.set_mode((tam_x, tam_y), 0)

x = 21
y = 21
width = 20

vel_x = VELOCIDADE
vel_y = VELOCIDADE

while True:
    # Calcula as regras
    x += vel_x
    y += vel_y

    if x >= tam_x - width:
        vel_x = - VELOCIDADE
    if x <= 0 + width:
        vel_x = VELOCIDADE

    if y >= tam_y - width:
        vel_y = - VELOCIDADE
    if y <= 0 + width:
        vel_y = VELOCIDADE

    # Pinta
    tela.fill(PRETO)
    pygame.draw.circle(tela, MAGENTA, (int(x), int(y)), width, 0)
    pygame.display.update()

    # Eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
