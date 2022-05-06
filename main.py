import pygame
from menu_principal import Menu_Principal
from menu_de_dificuldade import Menu_de_Dificuldade
from jogo import Jogo
from cores import *
from estado_do_programa import Estado_do_Programa
from ranking import Ranking
from tela_novo_score import Tela_Novo_Score

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
FPS = 30

LARGURA = 800
ALTURA = 840
tela = pygame.display.set_mode((LARGURA, ALTURA))

estado_do_programa = Estado_do_Programa()
menu_de_ranking = Ranking(estado_do_programa)
menu_pricipal = Menu_Principal(menu_de_ranking, estado_do_programa)
jogo = Jogo(estado_do_programa)
menu_de_dificuldade = Menu_de_Dificuldade(estado_do_programa, jogo)
tela_novo_score = Tela_Novo_Score(estado_do_programa, menu_de_ranking)

while estado_do_programa.rodando:
	eventos = pygame.event.get()
	for event in eventos:
		if event.type == pygame.QUIT:
			estado_do_programa.rodando = False

	tela.fill(COR_DE_FUNDO)

	if estado_do_programa.estado == estado_do_programa.MENU_PRINCIPAL:
		menu_pricipal.rodar(eventos)
	elif estado_do_programa.estado == estado_do_programa.MENU_DE_DIFICULDADE:
		menu_de_dificuldade.rodar(eventos)
	elif estado_do_programa.estado == estado_do_programa.JOGO:
		jogo.rodar(eventos)
	elif estado_do_programa.estado == estado_do_programa.INSERIR_NOVO_SCORE:
		tela_novo_score.rodar(eventos)
	elif estado_do_programa.estado == estado_do_programa.RANKING:
		menu_de_ranking.rodar(eventos)

	# TERMINAR FRAME
	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()