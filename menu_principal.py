import pygame
import pygame.freetype
import os
from cores import *

pygame.freetype.init()
pygame.mixer.init()
fonte_gigante: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 175)
fonte_grande: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 100)
fonte_menor: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 70)

som_click = pygame.mixer.Sound(os.path.join('som', 'click.wav'))

class Botão:
	def __init__(self, rect, texto):
		self.tela = pygame.display.get_surface()

		self.rect = pygame.rect.Rect(rect)
		self.surface = pygame.surface.Surface(self.rect.size)
		self.surface.fill(COR_DA_BARRINHA)

		self.texto = texto
		texto_surface, texto_rect = fonte_grande.render(texto, COR_DO_TEXTO)
		texto_rect.center = self.rect.center
		self.surface.blit(texto_surface, texto_rect)

	def draw(self):
		self.tela.blit(self.surface, self.rect)

class Menu_Principal:
	def __init__(self, menu_de_ranking, estado_do_programa):
		self.estado_do_programa = estado_do_programa
		self.menu_de_ranking = menu_de_ranking
		tela = pygame.display.get_surface()
		tela_rect = tela.get_rect()
		self.estado = 1

		largura, altura = 550, 150
		offset = 250

		# JOGAR #
		jogar = Botão((0, 0, largura, altura), 'JOGAR')
		jogar.rect.center = tela_rect.center
		jogar.rect.y -= offset

		# RANKING #
		ranking = Botão((0, 0, largura, altura), 'RANKING')
		ranking.rect.center = tela_rect.center

		# SAIR #
		sair = Botão((0, 0, largura, altura), 'SAIR')
		sair.rect.center = tela_rect.center
		sair.rect.y += offset

		self.botões = [jogar, ranking, sair]


	def draw(self):
		for botão in self.botões:
			botão.draw()

	def rodar(self, eventos):
		for event in eventos:
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				for botão in self.botões:
					if botão.rect.collidepoint(pos):
						som_click.play()
						if botão.texto == "JOGAR":
							self.estado_do_programa.estado = self.estado_do_programa.MENU_DE_DIFICULDADE
						if botão.texto == "RANKING":
							self.estado_do_programa.estado = self.estado_do_programa.RANKING
							self.menu_de_ranking.atualizar_ranking()
						if botão.texto == "SAIR":
							self.estado_do_programa.rodando = False
		self.draw()


