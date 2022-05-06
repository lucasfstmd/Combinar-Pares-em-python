import pygame
import pickle
import os
from cores import *

pygame.freetype.init()
fonte_grande: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 65)
fonte: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 50)
fonte_menor: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 40)

pygame.mixer.init()
som_click = pygame.mixer.Sound(os.path.join('som', 'click.wav'))

def carregar_ranking():
	with open('ranking', 'rb') as f:
		ranking = pickle.load(f)
	return ranking

class Ranking:
	def __init__(self, estado_do_programa):
		self.estado_do_programa = estado_do_programa
		self.tela = pygame.display.get_surface()
		self.tela_rect = self.tela.get_rect()
		self.ranking = carregar_ranking()
		self.dimensões = estado_do_programa.dimensões
		self.linhas = self.gerar_linhas()

		# DIMENSÕES DA MATRIZ #
		dimensões_repr = f'{self.dimensões}x{self.dimensões}'
		self.dimensões_surface, self.dimensões_rect = fonte_grande.render(dimensões_repr, COR_DO_TEXTO)
		self.dimensões_rect.midtop = self.tela_rect.midtop
		self.dimensões_rect.y += 10

		# SETAS #
		self.seta1_surface, self.seta1_rect = fonte_grande.render('<', COR_DO_TEXTO)
		self.seta1_rect.midright = self.dimensões_rect.midleft
		self.seta1_rect.x -= 30
		self.seta2_surface, self.seta2_rect = fonte_grande.render('>', COR_DO_TEXTO)
		self.seta2_rect.midleft = self.dimensões_rect.midright
		self.seta2_rect.x += 30

		# COLUNAS #
		self.rank_surface, self.rank_rect = fonte.render('RANK', COR_DO_TEXTO)
		self.rank_rect.center = self.linhas[1][0].center	
		
		self.nome_surface, self.nome_rect = fonte.render('NOME', COR_DO_TEXTO)
		self.nome_rect.center = self.linhas[1][1].center	
		
		self.erros_surface, self.erros_rect = fonte.render('ERROS', COR_DO_TEXTO)
		self.erros_rect.center = self.linhas[1][2].center
		
		self.tempo_surface, self.tempo_rect = fonte.render('TEMPO', COR_DO_TEXTO)
		self.tempo_rect.center = self.linhas[1][3].center

		# VOLTAR #
		self.voltar_surface = pygame.image.load('left_arrow.png').convert_alpha()
		self.voltar_surface = pygame.transform.rotozoom(self.voltar_surface, 0, 0.085)
		self.voltar_rect = self.voltar_surface.get_bounding_rect()
		self.voltar_rect.x = -6
		self.voltar_rect.y = -6
	
	def draw(self):
		self.draw_colunas()
		self.draw_interface()
		self.draw_ranking()
	
	def draw_ranking(self):
		ranking = self.ranking[self.dimensões]
		for i in range(2, 12):
			rank = str(i-1)
			rank_surface, rank_rect = fonte_menor.render(rank, COR_DO_TEXTO)
			rank_rect.center = self.linhas[i][0].center
			self.tela.blit(rank_surface, rank_rect)

			try:
				nome = ranking[i-2][0]
				erros = ranking[i-2][1]
				tempo = ranking[i-2][2]
			except IndexError:
				nome, erros, tempo = '-', '-', '-'

			nome_surface, nome_rect = fonte_menor.render(nome, COR_DO_TEXTO)
			nome_rect.center = self.linhas[i][1].center
			self.tela.blit(nome_surface, nome_rect)

			erros_surface, erros_rect = fonte_menor.render(str(erros), COR_DO_TEXTO)
			erros_rect.center = self.linhas[i][2].center
			self.tela.blit(erros_surface, erros_rect)

			tempo_surface, tempo_rect = fonte_menor.render(str(tempo), COR_DO_TEXTO)
			tempo_rect.center = self.linhas[i][3].center
			self.tela.blit(tempo_surface, tempo_rect)
	
	def rodar(self, eventos):
		for event in eventos:
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				if self.dimensões > 2 and self.seta1_rect.collidepoint(pos):
					self.dimensões -= 1
					self.atualizar_dimensões_surface()
					som_click.play()
				elif self.dimensões < 18 and self.seta2_rect.collidepoint(pos):
					self.dimensões += 1
					self.atualizar_dimensões_surface()
					som_click.play()
				elif self.voltar_rect.collidepoint(pos):
					self.estado_do_programa.estado = self.estado_do_programa.MENU_PRINCIPAL
					som_click.play()
		
		self.draw()

	def gerar_linhas(self):
		largura = self.tela_rect.width / 4
		linhas = []
		for i in range(12):
			altura = self.tela_rect.height / 12
			coluna = []
			for j in range(4):
				retangulo = pygame.Rect(largura * j, altura * i, largura, altura)
				coluna.append(retangulo)
			linhas.append(coluna)
		return linhas
	
	def draw_colunas(self):
		cor = (COR_DE_FUNDO[0], COR_DE_FUNDO[1], COR_DE_FUNDO[2])
		for retangulo in self.linhas:
			for linha in retangulo:
				pygame.draw.rect(self.tela, cor, linha)
			
			if cor == COR_DE_FUNDO:
				cor = (COR_DE_FUNDO[0]-15, COR_DE_FUNDO[1]-9, COR_DE_FUNDO[2]-15)
			else:
				cor = COR_DE_FUNDO

	def draw_interface(self):
		self.tela.blit(self.dimensões_surface, self.dimensões_rect)
		self.tela.blit(self.seta1_surface, self.seta1_rect)
		self.tela.blit(self.seta2_surface, self.seta2_rect)
		self.tela.blit(self.nome_surface, self.nome_rect)
		self.tela.blit(self.erros_surface, self.erros_rect)
		self.tela.blit(self.tempo_surface, self.tempo_rect)
		self.tela.blit(self.rank_surface, self.rank_rect)
		self.tela.blit(self.voltar_surface, self.voltar_rect)
	
	def atualizar_dimensões_surface(self):
		dimensões_repr = f'{self.dimensões}x{self.dimensões}'
		self.dimensões_surface, self.dimensões_rect = fonte_grande.render(dimensões_repr, COR_DO_TEXTO)
		self.dimensões_rect.midtop = self.tela_rect.midtop
		self.dimensões_rect.y += 6

	def atualizar_ranking(self):
		self.ranking = carregar_ranking()
		self.dimensões = self.estado_do_programa.dimensões
		self.atualizar_dimensões_surface()
