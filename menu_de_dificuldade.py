import pygame
import os
from menu_principal import Botão
from cores import *

pygame.freetype.init()
fonte_gigante: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 175)
fonte_grande: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 100)
fonte_menor: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 70)

pygame.mixer.init()
som_click = pygame.mixer.Sound(os.path.join('som', 'click.wav'))

class Menu_de_Dificuldade:
	def __init__(self, estado_do_programa, jogo):
		self.estado_do_programa = estado_do_programa
		self.tela = pygame.display.get_surface()
		self.tela_rect = self.tela.get_rect()
		self.dimensões = estado_do_programa.dimensões
		self.jogo = jogo
		
		# 'SELECIONE A DIFICULDADE' #
		self.texto, self.texto_rect = fonte_menor.render('Selecione a dificuldade: ', COR_DO_TEXTO)
		self.texto_rect.center = self.tela.get_rect().center
		self.texto_rect.y -= 150

		# DIMENSÕES DA MATRIZ #
		dimensões_repr = f'{self.dimensões}x{self.dimensões}'
		self.dimensões_surface, self.dimensões_rect = fonte_gigante.render(dimensões_repr, COR_DO_TEXTO)
		self.dimensões_rect.center = self.tela_rect.center

		# SETAS #
		self.seta1_surface, self.seta1_rect = fonte_gigante.render('<', COR_DO_TEXTO)
		self.seta1_rect.midright = self.dimensões_rect.midleft
		self.seta1_rect.x -= 75
		self.seta2_surface, self.seta2_rect = fonte_gigante.render('>', COR_DO_TEXTO)
		self.seta2_rect.midleft = self.dimensões_rect.midright
		self.seta2_rect.x += 75

		# JOGAR #
		self.jogar = Botão((0, 0, 475, 125), 'INICIAR')
		self.jogar.rect.midtop = self.dimensões_rect.midbottom
		self.jogar.rect.y += 75

		# VOLTAR #
		self.voltar_surface = pygame.image.load('left_arrow.png').convert_alpha()
		self.voltar_surface = pygame.transform.rotozoom(self.voltar_surface, 0, 0.085)
		self.voltar_rect = self.voltar_surface.get_bounding_rect()
		self.voltar_rect.x = -6
		self.voltar_rect.y = -6

	def draw(self):
		self.tela.blits([
			(self.texto, self.texto_rect),
			(self.dimensões_surface, self.dimensões_rect),
			(self.seta1_surface, self.seta1_rect),
			(self.seta2_surface, self.seta2_rect),
			(self.jogar.surface, self.jogar.rect),
			(self.voltar_surface, self.voltar_rect)
			])

	def rodar(self, eventos):
		for event in eventos:
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if self.dimensões > 2 and self.seta1_rect.collidepoint(pos):
					self.dimensões -= 1
					self.atualizar_surfaces()
					som_click.play()
				elif self.dimensões < 18 and self.seta2_rect.collidepoint(pos):
					self.dimensões += 1
					self.atualizar_surfaces()
					som_click.play()
				elif self.jogar.rect.collidepoint(pos):
					self.estado_do_programa.estado = self.estado_do_programa.JOGO
					self.estado_do_programa.dimensões = self.dimensões
					self.jogo.dimensões = self.dimensões
					self.jogo.resetar()
					som_click.play()
				elif self.voltar_rect.collidepoint(pos):
					self.estado_do_programa.estado = self.estado_do_programa.MENU_PRINCIPAL
					self.estado_do_programa.dimensões = self.dimensões
					self.jogo.dimensões = self.dimensões
					som_click.play()


		self.draw()

	def atualizar_surfaces(self):
		dimensões_repr = f'{self.dimensões}x{self.dimensões}'
		self.dimensões_surface, self.dimensões_rect = fonte_gigante.render(dimensões_repr, COR_DO_TEXTO)
		self.dimensões_rect.center = self.tela_rect.center
