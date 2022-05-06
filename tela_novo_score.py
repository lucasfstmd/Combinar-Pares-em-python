import pygame
import pickle
from cores import *

fonte: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 150)
fonte_menor: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 100)

def adcionar_score(dimensões, score):
	with open('ranking', 'rb') as f:
		ranking = pickle.load(f)
	
	ranking[dimensões].append(score)
	ranking[dimensões] = sorted(ranking[dimensões], key=lambda x: (x[1], x[2]))
	
	with open('ranking', 'wb') as f:
		pickle.dump(ranking, f)

class Tela_Novo_Score:
	def __init__(self, estado_do_programa, menu_de_ranking):
		self.menu_de_ranking = menu_de_ranking
		self.input = ''
		self.estado_do_programa = estado_do_programa
		self.tela = pygame.display.get_surface()
		self.tela_rect = self.tela.get_rect()

		# "INSIRA SEU NOME" #
		self.anunciado_surface, self.anunciado_rect = fonte_menor.render('Insira seu nome:', COR_DO_TEXTO)
		self.anunciado_rect.center = self.tela_rect.center
		self.anunciado_rect.y -= 150

		# BOTÃO "CONTINUAR" #
		continuar_texto, self.continuar_rect = fonte_menor.render('CONTINUAR', COR_DO_TEXTO)
		self.continuar_rect.width += 20
		self.continuar_rect.height += 20
		
		self.continuar_surface = pygame.Surface(self.continuar_rect.size)
		self.continuar_surface.fill(COR_DA_BARRINHA)
		self.continuar_surface.blit(continuar_texto, (20/2,  20/2))

		self.continuar_rect.center = self.tela_rect.center
		self.continuar_rect.y += 150
		
	def rodar(self, eventos):
		for evento in eventos:
			if evento.type == pygame.MOUSEBUTTONDOWN:
				pos = evento.pos
				if self.continuar_rect.collidepoint(pos):
					self.finalizar()
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_BACKSPACE:
					self.input = self.input[0:-1]
				elif evento.key == pygame.K_RETURN:
					self.finalizar()
				elif evento.unicode == '~':
					pass
				else:
					if len(self.input) <= 8:
						self.input += evento.unicode
						self.input = self.input.upper()
		self.draw()

	def draw(self):
		input_surface, input_rect = fonte.render(self.input, COR_DO_TEXTO)
		input_rect.center = self.tela.get_rect().center
		
		self.tela.blit(input_surface, input_rect)
		self.tela.blit(self.anunciado_surface, self.anunciado_rect)
		self.tela.blit(self.continuar_surface, self.continuar_rect)

	def finalizar(self):
		if len(self.input) > 0:
			self.estado_do_programa.estado = self.estado_do_programa.RANKING
			score = [self.input] + self.estado_do_programa.ultimo_score
			score = tuple(score)
			adcionar_score(self.estado_do_programa.dimensões, score)
			self.menu_de_ranking.atualizar_ranking()


