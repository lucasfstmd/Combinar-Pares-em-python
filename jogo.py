import pygame
import os
import random
from cores import *

fonte: pygame.freetype.Font = pygame.freetype.SysFont('bahnschrift', 35)

pygame.mixer.init()
som_click = pygame.mixer.Sound(os.path.join('som', 'click.wav'))

som_incorrect = pygame.mixer.Sound(os.path.join('som', 'incorrect.wav'))
som_incorrect.set_volume(0.25)

som_correct = pygame.mixer.Sound(os.path.join('som', 'correct.wav'))
som_correct.set_volume(0.1)

som_success = pygame.mixer.Sound(os.path.join('som', 'success.mp3'))

# ESTADOS DO JOGO #
NENHUM_QUADRADO_CLICADO = 0
UM_QUADRADO_CLICADO = 1
DOIS_QUADRADOS_CLICLADOS = 2
JOGO_TERMINADO = 3

class Jogo:
	def __init__(self, estado_do_programa):
		self.estado_do_programa = estado_do_programa
		self.dimensões = estado_do_programa.dimensões
		self.tela = pygame.display.get_surface()
		self.tela_rect = self.tela.get_rect()

		self.barrinha_rect = pygame.Rect(0, 0, self.tela_rect.width, 40)
		self.barrinha_rect.bottom = self.tela_rect.bottom

		self.quadrados = self.gerar_quadrados()

		self.tempo_inicial = pygame.time.get_ticks()
		self.tempo = 0
		self.erros = 0

		self.estado_do_jogo = NENHUM_QUADRADO_CLICADO
		self.par_atual = []
		self.tempo_do_segundo_quadrado_clicado = 0

	def draw(self):
		for quadrado in self.quadrados:
			quadrado.draw()

		self.draw_barrinha()

	def update(self, eventos):
		if self.estado_do_jogo != JOGO_TERMINADO:
			self.tempo += pygame.time.get_ticks() - self.tempo_inicial - self.tempo
		
		for evento in eventos:
			if evento.type == pygame.MOUSEMOTION:
				pos = evento.pos
				for quadrado in self.quadrados:
					if quadrado.rect.collidepoint(pos):
						quadrado.destacado = True
					else:
						quadrado.destacado = False
			
			if evento.type == pygame.MOUSEBUTTONDOWN:
				pos = evento.pos
				for quadrado in self.quadrados:
					if quadrado.rect.collidepoint(pos):
						if quadrado.virado == False and quadrado.vazio == False:
							if self.estado_do_jogo == NENHUM_QUADRADO_CLICADO:
								quadrado.virado = True
								self.par_atual.append(quadrado)
								som_click.play()
								self.estado_do_jogo = UM_QUADRADO_CLICADO
							elif self.estado_do_jogo == UM_QUADRADO_CLICADO:
								quadrado.virado = True
								self.par_atual.append(quadrado)
								self.estado_do_jogo = DOIS_QUADRADOS_CLICLADOS
								
								if self.par_atual[0].id == self.par_atual[1].id:
									
									self.par_atual[0].terminado = True
									self.par_atual[1].terminado = True
									self.par_atual = []
									self.estado_do_jogo = NENHUM_QUADRADO_CLICADO

									if self.jogo_terminado():
										self.tempo_do_segundo_quadrado_clicado = pygame.time.get_ticks()
										self.estado_do_jogo = JOGO_TERMINADO
										som_success.play()
									else:
										som_correct.play()
								else:
									self.tempo_do_segundo_quadrado_clicado = pygame.time.get_ticks()
									self.erros += 1
									som_incorrect.play()


		if self.estado_do_jogo == DOIS_QUADRADOS_CLICLADOS:
			if (pygame.time.get_ticks() - self.tempo_do_segundo_quadrado_clicado) > 300:
				self.estado_do_jogo = NENHUM_QUADRADO_CLICADO
				self.par_atual[0].virado = False
				self.par_atual[1].virado = False
				self.par_atual = []
		elif self.estado_do_jogo == JOGO_TERMINADO:
			if (pygame.time.get_ticks() - self.tempo_do_segundo_quadrado_clicado) > 300:
				self.estado_do_programa.estado = self.estado_do_programa.INSERIR_NOVO_SCORE
				self.estado_do_programa.ultimo_score = [self.erros, self.tempo/1000]
	
	def rodar(self, eventos):
		self.update(eventos)
		self.draw()

	def resetar(self):
		self.quadrados = self.gerar_quadrados()
		self.tempo_inicial = pygame.time.get_ticks()
		self.estado_do_jogo = NENHUM_QUADRADO_CLICADO
		self.erros = 0
		self.tempo = 0

	def draw_barrinha(self):
		pygame.draw.rect(self.tela, COR_DA_BARRINHA, self.barrinha_rect)
		
		tempo, tempo_rect = fonte.render(f"Tempo: {int(self.tempo/1000)}s", COR_DO_TEXTO)
		tempo_rect.bottomleft = self.barrinha_rect.bottomleft
		tempo_rect.x += 2

		erros, erros_rect = fonte.render(f"Erros: {self.erros}", COR_DO_TEXTO)
		erros_rect.center = self.barrinha_rect.center

		dimensões, dimensões_rect = fonte.render(f"{self.dimensões}x{self.dimensões}", COR_DO_TEXTO)
		dimensões_rect.midright = self.barrinha_rect.midright
		dimensões_rect.x -= 2

		self.tela.blit(tempo, tempo_rect)
		self.tela.blit(erros, erros_rect)
		self.tela.blit(dimensões, dimensões_rect)

	def gerar_quadrados(self):
		imagens = self.carregar_imagens()
		quadrados = []
		unidade = self.tela_rect.width // self.dimensões
		lado = unidade * 0.9

		for i in range(self.dimensões):
			for j in range(self.dimensões):
				rect_maior = pygame.Rect(unidade*i, unidade*j, unidade, unidade)
				rect_menor = pygame.Rect(0, 0, lado, lado)
				rect_menor.center = rect_maior.center

				if self.dimensões % 2 != 0 and i == (self.dimensões//2) and j == (self.dimensões//2):
					surface_vazia = pygame.Surface((0, 0))
					quadrado = Quadrado(surface_vazia, rect_menor)
					quadrado.vazio = True
					quadrado.terminado = True
					
				else:
					quadrado = Quadrado(imagens.pop(), rect_menor)
				
				quadrados.append(quadrado)
		
		return quadrados

	def carregar_imagens(self):
		imagens = os.listdir('imagens')
		
		imagens_paths = random.sample(imagens, (self.dimensões * self.dimensões) // 2)
		
		imagens_carregadas = []
		for imagem in imagens_paths:
			path = os.path.join('imagens', imagem)
			surface = pygame.image.load(path).convert_alpha()
			surface = pygame.transform.rotozoom(surface, 0, 1.5/self.dimensões)
			imagens_carregadas.append(surface)

		imagens_carregadas += imagens_carregadas
		random.shuffle(imagens_carregadas)
		return imagens_carregadas

	def jogo_terminado(self):
		for quadrado in self.quadrados:
			if quadrado.terminado == False:
				return False
		return True

class Quadrado:
	def __init__(self, imagem, rect):
		self.id = id(imagem)
		self.tela = pygame.display.get_surface()
		self.imagem = imagem
		self.imagem_rect = imagem.get_rect()
		self.imagem_rect.center = rect.center
		self.rect = rect
		
		self.vazio = False
		self.virado = False
		self.destacado = False
		self.terminado = False

	def draw(self):
		if self.vazio:
			pygame.draw.rect(self.tela, COR_DO_QUADRADO_VAZIO, self.rect)
		elif self.virado:
			if self.terminado:
				pygame.draw.rect(self.tela, COR_DO_QUADRADO_TERMINADO, self.rect)
			else:
				pygame.draw.rect(self.tela, COR_DO_QUADRADO, self.rect)
			self.tela.blit(self.imagem, self.imagem_rect)
		else:
			if self.destacado:
				pygame.draw.rect(self.tela, COR_DO_QUADRADO_DESTACADO, self.rect)
			else:
				pygame.draw.rect(self.tela, COR_DO_QUADRADO, self.rect)

