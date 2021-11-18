import pygame as pg
from pygame.locals import *


# t1 - claro - pretas - 1(peca) - 11(cap)
# t2 - escuro - brancas - 2(peca) - 22(cap)
#cores
clara = [(114, 199, 225),'#72c7e1']
escura = [(0, 155, 160),'#009BA0']
class Bizingo:
    def __init__(self):
        pg.init()
        self._tela = pg.display.set_mode((1000,650))
        pg.display.set_caption("Bizingo")
        self._t1 = pg.image.load('imgs/t1.png')
        self._t2 = pg.image.load('imgs/t2.png')

        self.area_t2 = pg.image.load('imgs/area_selecionada 50x44.png')
        self.area_t1 = pg.image.load('imgs/area_selecionada(1) 50x44.png')

        self.peca_t1 = pg.image.load('imgs/peca_preta 50x44.png')
        self.cap_t1 = pg.image.load('imgs/cap_preta 50x44.png')
        self.peca_t2 = pg.image.load('imgs/peca_branca 50x44.png')
        self.cap_t2 = pg.image.load('imgs/cap_branca 50x44.png')

        self._area_selecionada = False
        self._tabuleiro = []
        self._pecas = []

 
    def point_collide(self, point):
        for linha in range(len(self._tabuleiro)):
            if linha <= 8:
                peca = self.area_t2
                triangulo = self._t2
            else:
                peca = self.area_t1
                triangulo = self._t1
            for i in self._tabuleiro[linha]:
                rect = i["pos"]
                color = None
                
                if triangulo == self._t2:
                    color = (0, 155, 160)
                else:
                    color = (114, 199, 225)

                x, y = point
                x -= rect.x
                y -= rect.y

                #detects if click hits the image
                if 0 <= x < 50:
                    if 0 <= y < 44:
                        #detects if color at clicking position != colorkey-color(transparent)
                        if triangulo.get_at((x,y))[0:3] == color:
                            if self._area_selecionada == False:
                                self._tela.blit(peca, (rect.x,rect.y))
                                self._area_selecionada = True
                            else:
                                self.clear()
                                self._area_selecionada = False
                            return rect
                
                if triangulo == self._t2:
                    triangulo = self._t1
                    peca = self.area_t1
                else:
                    triangulo = self._t2
                    peca = self.area_t2
            
    def clear(self):
        self._tela.fill((255, 255, 255))
        self.construirTabuleiro()
        self.posPecas()
        self.textos()

    def textos(self):            
        font_1 = pg.font.SysFont('Comic Sans MS', 50)
        font_2 = pg.font.SysFont('Comic Sans MS', 40)
        font_3 = pg.font.SysFont('Comic Sans MS', 20)

        title = font_1.render('Bizingo', False, (0, 0, 0))
        vez = font_2.render('Vez de:', False, (0, 0, 0))
        jogador = font_2.render("Jogador 1", False, (0, 0, 0))

        status = font_3.render("Staus:", False, (255, 0, 0))
        status_j = font_3.render("jogando...", False, (255, 0, 0))

        pecas_restantes = font_3.render("Peças restantes:", False, (0, 0, 0))
        pecas_j1 = font_3.render("Jogador 1 : 7", False, (0, 0, 0))
        pecas_j2 = font_3.render("Jogador 2 : 10", False, (0, 0, 0))

        self._tela.blit(title,(250,0))

        self._tela.blit(vez,(730,150))
        self._tela.blit(jogador,(700,200))

        self._tela.blit(status,(770,300))
        self._tela.blit(status_j,(750,330))

        self._tela.blit(pecas_restantes,(720,400))
        self._tela.blit(pecas_j1,(700,430))
        self._tela.blit(pecas_j2,(700,460))

        pg.draw.line(self._tela,(0,0,0),(650,50),(650,600),5)
        pg.draw.line(self._tela,(0,0,0),(950,50),(950,600),5)

        pg.draw.line(self._tela,(0,0,0),(650,50),(950,50),5)
        pg.draw.line(self._tela,(0,0,0),(650,600),(950,600),5)

    def construirTabuleiro(self):
        for l in range(11):
            tr = self._t2
            if l >= 9:
                tr = self._t1
            for c in self._tabuleiro[l]:
                self._tela.blit(tr, (c["pos"].x,c["pos"].y))
                if tr == self._t2:
                    tr = self._t1
                else:
                    tr = self._t2

    def matrizTabuleiro(self):
    
        t_altura = 44
        t_largura = 50
        #meio ponto 325 , x_meio 325 - 25 (metade da largura do triangulo)
        meio = 325 -25
        
        triangulos = 5
        for l in range(11):
            self._tabuleiro.append([])
            tr = self._t2
            if l >= 9:
                tr = self._t1
            x = triangulos//2 
            for t in range(triangulos):
                 
                #negativo
                if t+1< triangulos//2+1:
                    self._tabuleiro[l].append({"pos":Rect((meio -25*x+25*t, t_altura*l + 100),(50,44)),"peca":None}) 
                #neutro
                elif t+1== triangulos//2+1:
                    self._tabuleiro[l].append({"pos":Rect((meio, t_altura*l + 100),(50,44)),"peca":None})
                    x = 1
                #positivo
                else:
                    self._tabuleiro[l].append({"pos":Rect((meio + 25*x, t_altura*l + 100),(50,44)),"peca":None})
                    x += 1

                if tr == self._t2:
                    tr = self._t1
                else:
                    tr = self._t2
                
            if l == 8:
                pass
            elif l == 9 :
                triangulos -= 2
            else:
                triangulos += 2

    def iniciarJogo(self):
        self._tela.fill((255, 255, 255))
        
        self.matrizTabuleiro()
        self.construirTabuleiro()
        self.pecas_iniciais()
        self.textos()
        while True:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.point_collide(mouse_pos)

            pg.display.flip()

    def pecas_iniciais(self):
        for p in range(2):
            if p == 0:
                #brancas
                peca= self.peca_t2
                cap = self.cap_t2
                x_i = 2
                x_f = 6
                for i in range(2,6):
                    for c in range(len(self._tabuleiro[i])):
                        if x_i<=c<=x_f and c%2 == 0:
                            rect = self._tabuleiro[i][c]["pos"]
                            if (i == 5) and (c == 4 or c == 10):
                                self._tabuleiro[i][c]["peca"] = 22
                                self._tela.blit(cap, (rect.x,rect.y))
                            else:  
                                self._tabuleiro[i][c]["peca"] = 2
                                self._tela.blit(peca, (rect.x,rect.y ))
                    x_f += 2
            else:
                #pretas
                peca= self.peca_t1
                cap = self.cap_t1
                x_i = 1
                x_f = 15
                for i in range(7,10):
                    if i < 9:
                        x_i += 2
                        for c in range(len(self._tabuleiro[i])):
                            if x_i<=c<=x_f and c%2 != 0:
                                rect = self._tabuleiro[i][c]["pos"]
                                if (i == 7) and (c == 5 or c == 13):
                                    self._tabuleiro[i][c]["peca"] = 11
                                    self._tela.blit(cap, (rect.x,rect.y- 10))
                                else:
                                    self._tabuleiro[i][c]["peca"] = 1    
                                    self._tela.blit(peca, (rect.x,rect.y- 10))       
                    else:
                        x_i += 1
                        x_f -= 1
                        for c in range(len(self._tabuleiro[i])):
                            if x_i<=c<=x_f and c%2 == 0:
                                rect = self._tabuleiro[i][c]["pos"]
                                self._tabuleiro[i][c]["peca"] = 1
                                self._tela.blit(peca, (rect.x,rect.y- 10))

    def posPecas(self):
        for l in range(11):
            linha = self._tabuleiro[l]
            for c in range(len(linha)):
                coluna = linha[c]
                if coluna["peca"] == None:
                    pass
                elif coluna["peca"] == 1 or coluna["peca"] == 11 :
                    if coluna["peca"] == 1:
                        peca = self.peca_t1
                        self._tela.blit(peca, (coluna["pos"].x,coluna["pos"].y-10))
                    else:
                        cap = self.cap_t1
                        self._tela.blit(cap, (coluna["pos"].x,coluna["pos"].y-10))
                else:
                    if coluna["peca"] == 2:
                        peca = self.peca_t2
                        self._tela.blit(peca, (coluna["pos"].x,coluna["pos"].y))
                    else:
                        cap = self.cap_t2
                        self._tela.blit(cap, (coluna["pos"].x,coluna["pos"].y))
               


Bizingo().iniciarJogo()