import random
import pygame
from abc import ABCMeta, abstractmethod

pygame.init()

Y = 600
X = 800
VELOCIDADE = 1
size = 600 // 30

# Cores
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)
CIANO = (0, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Direções
ACIMA = 1
ABAIXO = 2
DIREITA = 3
ESQUERDA = 4

screen = pygame.display.set_mode((X, Y), 0)
fonte = pygame.font.SysFont("arial", 30, True, False)


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def processar_eventos(self, evs):
        pass


class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_intencao(self):
        pass

    @abstractmethod
    def recusar_intencao(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.tamanho = tamanho
        self.estado = "jogando"  # 0-Jogando 1-Pausado 2-GameOver 3-Vitória
        self.pontos = 0
        self.pacman = pac
        self.moviveis = []
        # 28 colunas por 29 linhas
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_score(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render(f"Score: {self.pontos}", True, AMARELO)
        img_vidas = fonte.render(f"Lifes: {self.pacman.vidas}", True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 20))
        tela.blit(img_vidas, (pontos_x, 60))

    def pintar(self, tela):
        if self.estado == "jogando":
            self.pintar_jogando(tela)
        elif self.estado == "pausado":
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == "gameover":
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == "vitoria":
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_texto_centro(self, tela, texto):
        texto_img = fonte.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "V I T Ó R I A")

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S A D O")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)

    def pintar_linha(self, tela, numero_linha, linha):
        cor = PRETO
        for numero_coluna, espaco in enumerate(linha):
            if espaco == 0:
                cor = PRETO
            if espaco == 1:
                cor = PRETO
            if espaco == 2:
                cor = AZUL

            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho

            # Desenha os retângulos de tamanho = 20px
            pygame.draw.rect(tela, cor, ((x, y), (self.tamanho, self.tamanho)), 0)
            # pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)

            # Desenha os pontos brancos
            if espaco == 1:
                pygame.draw.circle(tela, AMARELO, (x + self.tamanho // 2, y + self.tamanho // 2), 2, 0)

    def calcular_regras(self):
        if self.estado == "jogando":
            self.calcular_regras_jogando()
        elif self.estado == "pausado":
            self.calcular_regras_pausado()
        elif self.estado == "gameover":
            self.calcular_regras_gameover()
        elif self.estado == "vitoria":
            self.calcular_regras_vitoria()

    def calcular_regras_vitoria(self):
        pass

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            linha_intencao = int(movivel.linha_intencao)
            coluna_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)

            if len(direcoes) >= 3:
                movivel.esquina(direcoes)

            # Colisão com o fantasma
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and \
                    movivel.coluna == self.pacman.coluna:
                self.pacman.vidas -= 1
                print(self.pacman.vidas)
                if self.pacman.vidas <= 0:
                    self.estado = "gameover"
                else:
                    self.pacman.linha = 1
                    self.pacman.coluna = 1
            else:
                if 0 <= coluna_intencao < 28 and 0 <= linha_intencao < 29 and \
                        self.matriz[linha_intencao][coluna_intencao] != 2:
                    movivel.aceitar_intencao()
                    if isinstance(movivel, Pacman):
                        self.calcular_pontos()
                else:
                    movivel.recusar_intencao(direcoes)

    def get_direcoes(self, linha: int, coluna: int) -> list:
        linha = int(linha)
        coluna = int(coluna)
        direcoes = []
        if self.matriz[linha - 1][coluna] != 2:
            direcoes.append(ACIMA)
        if self.matriz[linha + 1][coluna] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[linha][coluna - 1] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[linha][coluna + 1] != 2:
            direcoes.append(DIREITA)

        return direcoes

    def calcular_pontos(self):
        if self.matriz[self.pacman.linha][self.pacman.coluna] == 1:
            self.pontos += 1
            self.matriz[self.pacman.linha][self.pacman.coluna] = 0
            if self.pontos == 306:
                self.estado = "vitoria"

    def processar_eventos(self, evs):
        for e in evs:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == "jogando":
                        self.estado = "pausado"
                    else:
                        self.estado = "jogando"


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura = 0
        self.abertura_velocidade = 1
        self.vidas = 5

    def recusar_intencao(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

    def aceitar_intencao(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela):
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        self.abertura += self.abertura_velocidade
        if self.abertura <= 0:
            self.abertura_velocidade = 1
        elif self.abertura >= self.raio:
            self.abertura_velocidade = -1

        # Desenha a boca
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos)

        # Desenha o olho
        olho_x = int(self.centro_x + self.raio / 9)
        olho_y = int(self.centro_y - self.raio / 1.5)
        olho_raio = int(self.raio / 4)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, evs):
        for e in evs:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = VELOCIDADE
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -VELOCIDADE
                elif e.key == pygame.K_UP:
                    self.vel_y = -VELOCIDADE
                elif e.key == pygame.K_DOWN:
                    self.vel_y = +VELOCIDADE

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0

    def processar_eventos_mouse(self, evs):
        delay = 30
        for e in evs:
            if e.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) / delay


class Fantasma(ElementoJogo, Movivel):
    def __init__(self, cor, tamanho):
        self.velocidade = 1
        self.direcao = ACIMA
        self.coluna = 13.0
        self.linha = 15.0
        self.cor = cor
        self.tamanho = tamanho
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 2, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)
                    ]
        pygame.draw.polygon(tela, self.cor, contorno)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_e_x = int(px + fatia * 2.5)
        olho_e_y = int(py + fatia * 2.5)

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext)  # Olho esquerdo externo
        pygame.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_int)  # Olho esquerdo interno
        pygame.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext)  # Olho direito externo
        pygame.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_int)  # Olho direito interno

    def processar_eventos(self, evs):
        pass

    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade

    def aceitar_intencao(self):
        self.coluna = self.coluna_intencao
        self.linha = self.linha_intencao

    def recusar_intencao(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes: list) -> None:
        self.mudar_direcao(direcoes)


if __name__ == "__main__":
    # Criação dos objetos
    pacman = Pacman(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pacman)
    clk = pygame.time.Clock()

    # Passagem dos objetos para cenário
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    while True:
        # Calcular as regras
        pacman.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()

        # Pintar a tela
        screen.fill(PRETO)
        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        clk.tick(10)
        # pygame.time.delay(100)

        # Eventos
        eventos = pygame.event.get()

        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)
