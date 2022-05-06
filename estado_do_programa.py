class Estado_do_Programa:
	# ESTADOS DO PROGRAMA #
	MENU_PRINCIPAL = 1
	MENU_DE_DIFICULDADE = 2
	JOGO = 3
	INSERIR_NOVO_SCORE = 4
	
	def __init__(self):
		self.MENU_PRINCIPAL = 1
		self.MENU_DE_DIFICULDADE = 2
		self.JOGO = 3
		self.INSERIR_NOVO_SCORE = 4
		self.RANKING = 5
		
		self.estado = self.MENU_PRINCIPAL
		self.dimensões = 3 # 3x3
		self.rodando = True
		self.ultimo_score = None
