import pyxel
import random
import os

class RPG:
    def __init__(self):
        #inicio da renderizacao e variavel global
        pyxel.init(200, 150, title="Average RPG Pyxel")
        pyxel.mouse(True)
        
        #carrega a arte de forma segura
        pasta_do_jogo = os.path.dirname(os.path.abspath(__file__))
        caminho_da_arte = os.path.join(pasta_do_jogo, "rpg.pyxres")
        
        try:
            pyxel.load(caminho_da_arte) 
        except:
            pass
            
        #estado inicial da tela
        self.tela = "menu"
        self.turno = "jogador"
        
        #atributos principais
        self.hp_jogador = 100
        self.hp_max = 100
        self.nivel = 1
        self.xp = 0
        self.xp_proximo = 50
        self.dano_base = 15
        self.esquiva_chance = 0
        
        #sistema de rcurso
        self.classe_escolhida = ""
        self.nome_recurso = "Stamina"
        self.recurso = 100
        self.max_recurso = 100
        self.custo_ataque = 35
        
        #controle fase
        self.estagio = 0 
        self.max_estagios = 8
        
        #atributo inimigo
        self.nome_inimigo = ""
        self.hp_inimigo = 0
        self.hp_max_inimigo = 0
        
        #combate e inventario
        self.pocoes = 3
        self.defendendo = False
        self.timer_inimigo = 0
        self.dano_pendente = 0
        self.msg_inimigo = ""
        self.msg_aviso = ""
        
        #caminho e recompensa pool
        self.opcoes_caminho_atual = []
        self.opcoes_recompensa_atual = []
        
        pyxel.run(self.update, self.draw)

    def update(self):

        #logica atualiza e estados
        
        #esc
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit() 
            
        #tela menu princial
        if self.tela == "menu":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if 50 <= pyxel.mouse_x <= 150 and 75 <= pyxel.mouse_y <= 95:
                    self.tela = "selecionar_classe"
                    
        #tela classes 
        elif self.tela == "selecionar_classe":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if 10 <= pyxel.mouse_x <= 190:
                    if 45 <= pyxel.mouse_y <= 65: # Guerreiro
                        self.configurar_classe("Guerreiro", hp=120, dano=18, pocoes=2, esquiva=0, tipo_rec="Stamina", max_rec=100, custo=35)
                    elif 75 <= pyxel.mouse_y <= 95: # Assassino
                        self.configurar_classe("Assassino", hp=95, dano=22, pocoes=3, esquiva=10, tipo_rec="Stamina", max_rec=140, custo=30)
                    elif 105 <= pyxel.mouse_y <= 125: # Mago
                        self.configurar_classe("Mago", hp=80, dano=26, pocoes=5, esquiva=20, tipo_rec="Mana", max_rec=130, custo=45)
                    
        #tela escolha de caminhos
        elif self.tela == "caminhos":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                escolhido = None
                if 10 <= pyxel.mouse_x <= 190:
                    if 45 <= pyxel.mouse_y <= 65 and len(self.opcoes_caminho_atual) > 0:
                        escolhido = self.opcoes_caminho_atual[0]
                    elif 75 <= pyxel.mouse_y <= 95 and len(self.opcoes_caminho_atual) > 1:
                        escolhido = self.opcoes_caminho_atual[1]
                    elif 105 <= pyxel.mouse_y <= 125 and len(self.opcoes_caminho_atual) > 2:
                        escolhido = self.opcoes_caminho_atual[2]
                        
                if escolhido:
                    self.aplicar_efeito_caminho(escolhido)
                    if self.hp_jogador <= 0:
                        self.tela = "derrota"
                    else:
                        self.turno = "jogador"
                        self.tela = "batalha"
                        
        #tela recompensa 
        elif self.tela == "recompensa":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                escolhido = None
                if 10 <= pyxel.mouse_x <= 190:
                    if 55 <= pyxel.mouse_y <= 77 and len(self.opcoes_recompensa_atual) > 0:
                        escolhido = self.opcoes_recompensa_atual[0]
                    elif 85 <= pyxel.mouse_y <= 107 and len(self.opcoes_recompensa_atual) > 1:
                        escolhido = self.opcoes_recompensa_atual[1]
                        
                if escolhido:
                    self.aplicar_efeito_recompensa(escolhido)
                    self.avancar_proxima_fase()
                    
        #tela de batalha e turno
        elif self.tela == "batalha":
            #verifica condição de vitoiria ou derrota
            if self.hp_inimigo <= 0:
                xp_ganho = 40 * self.estagio
                self.ganhar_xp(xp_ganho)
                
                if self.estagio >= self.max_estagios:
                    self.tela = "vitoria" 
                else:
                    self.gerar_novas_recompensas()
                    self.tela = "recompensa" 
                    
            elif self.hp_jogador <= 0:
                self.tela = "derrota"
            
            #turno jogador
            elif self.turno == "jogador":
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    #botao atacar (gasta recurso)
                    if 15 <= pyxel.mouse_x <= 65 and 115 <= pyxel.mouse_y <= 135: 
                        if self.recurso >= self.custo_ataque:
                            self.recurso -= self.custo_ataque
                            self.hp_inimigo -= self.dano_base 
                            self.defendendo = False
                            self.msg_aviso = ""
                            self.turno = "inimigo_decide"
                        else:
                            self.msg_aviso = f"Sem {self.nome_recurso}! Defenda-se!"
                        
                    #defender (gasta nada ereduz dano inimigo)
                    elif 70 <= pyxel.mouse_x <= 130 and 115 <= pyxel.mouse_y <= 135: 
                        self.defendendo = True 
                        self.recurso = min(self.max_recurso, self.recurso + 55) 
                        self.msg_aviso = ""
                        self.turno = "inimigo_decide"
                        
                    #botao curar (gasta poção)
                    elif 135 <= pyxel.mouse_x <= 185 and 115 <= pyxel.mouse_y <= 135: 
                        if self.pocoes > 0: 
                            self.hp_jogador += 40
                            if self.hp_jogador > self.hp_max:
                                self.hp_jogador = self.hp_max
                            self.pocoes -= 1
                            self.defendendo = False
                            self.msg_aviso = ""
                            self.turno = "inimigo_decide"
                        
            #ia do inimigo
            elif self.turno == "inimigo_decide":
                chance = random.randint(1, 100) 
                if chance <= 25: 
                    self.dano_pendente = (10 * self.estagio) if self.estagio < 8 else 95 
                    self.msg_inimigo = "CRITICO!"
                else: 
                    self.dano_pendente = random.randint(4 * self.estagio, 7 * self.estagio) if self.estagio < 8 else 70 
                    self.msg_inimigo = f"{self.nome_inimigo} ataca!"
                
                if self.defendendo:
                    self.dano_pendente = max(2, self.dano_pendente // 2)
                    
                self.timer_inimigo = 45 
                self.turno = "inimigo_espera"
                    
            #pausa pro ataque inimigo
            elif self.turno == "inimigo_espera":
                self.timer_inimigo -= 1
                if self.timer_inimigo <= 0:
                    if random.randint(1, 100) <= self.esquiva_chance:
                        self.msg_inimigo = "ESQUIVOU!"
                        self.dano_pendente = 0
                    else:
                        self.hp_jogador -= self.dano_pendente
                    self.turno = "jogador"

    # 3.progressao e regras
    def configurar_classe(self, nome, hp, dano, pocoes, esquiva, tipo_rec, max_rec, custo):
        self.classe_escolhida = nome
        self.hp_max = hp
        self.hp_jogador = hp
        self.dano_base = dano
        self.pocoes = pocoes
        self.esquiva_chance = esquiva
        self.nome_recurso = tipo_rec
        self.max_recurso = max_rec
        self.recurso = max_rec
        self.custo_ataque = custo
        self.estagio = 1
        self.preparar_fase()
        self.gerar_novos_caminhos()
        self.tela = "caminhos"

    def preparar_fase(self):
        #config caminho ate fase final
        if self.estagio < 8:
            self.nome_inimigo = random.choice(["Slime", "Guarda"])
            self.hp_inimigo = 45 + (self.estagio * 24)
        else:
            self.nome_inimigo = "Dragao"
            self.hp_inimigo = 450 
            
        self.hp_max_inimigo = self.hp_inimigo
        self.turno = "jogador"

    def gerar_novos_caminhos(self):
        #pesos de cada caminho baseado na classe do jogador
        peso_floresta = 3 if self.classe_escolhida == "Mago" else 1
        peso_atalho = 4 if self.classe_escolhida == "Assassino" else (3 if self.classe_escolhida == "Guerreiro" else 1)
        peso_treino = 4 if self.classe_escolhida == "Assassino" else (3 if self.classe_escolhida in ["Guerreiro", "Mago"] else 1)

        banco_caminhos = [
            {"titulo": "Floresta", "desc": "+1 Pocao", "tipo": "pocao", "val": 1, "cor": 11, "peso": peso_floresta},
            {"titulo": "Acampamento", "desc": "+40 HP & Recurso Max", "tipo": "cura_total", "val": 40, "cor": 3, "peso": 2},
            {"titulo": "Ruinas Antigas", "desc": "+40 XP", "tipo": "xp", "val": 40, "cor": 5, "peso": 1},
            {"titulo": "Treino/Medit", "desc": f"+25 Max {self.nome_recurso}", "tipo": "recurso_max", "val": 25, "cor": 12, "peso": peso_treino},
            {"titulo": "Atalho Sombrio", "desc": "-15 HP | Inimigo -30HP", "tipo": "atalho", "val": 30, "cor": 8, "peso": peso_atalho},
            {"titulo": "Fonte Magica", "desc": "+3 Dano Base", "tipo": "dano_bonus", "val": 3, "cor": 1, "peso": 3 if self.classe_escolhida == "Assassino" else 2}
        ]
        
        pool = []
        for item in banco_caminhos:
            for _ in range(item["peso"]):
                pool.append(item)
                
        escolhidos = []
        while len(escolhidos) < 3 and len(pool) > 0:
            item = random.choice(pool)
            if not any(e["titulo"] == item["titulo"] for e in escolhidos):
                escolhidos.append(item)
        self.opcoes_caminho_atual = escolhidos

    def aplicar_efeito_caminho(self, opcao):
        t = opcao["tipo"]
        v = opcao["val"]
        if t == "pocao":
            self.pocoes += v
        elif t == "cura_total":
            self.hp_jogador = min(self.hp_max, self.hp_jogador + v)
            self.recurso = self.max_recurso
        elif t == "xp":
            self.ganhar_xp(v)
        elif t == "recurso_max":
            self.max_recurso += v
            self.recurso = self.max_recurso
        elif t == "atalho":
            self.hp_jogador -= 15
            self.hp_inimigo = max(10, self.hp_inimigo - v)
        elif t == "dano_bonus":
            self.dano_base += v

    def gerar_novas_recompensas(self):
        #pool de recompensas baseado na classe do jogador
        if self.classe_escolhida == "Mago":
            banco_recompensas = [
                {"titulo": "Cajado Arcano", "desc": "+8 Dano Magico", "tipo": "dano", "val": 8, "cor": 5, "peso": 5},
                {"titulo": "Armadura Magica", "desc": "+15 HP | +15% Esquiva", "tipo": "armadura_magica", "val": 15, "esq": 15, "cor": 12, "peso": 4},
                {"titulo": "Cristal de Mana", "desc": "+30 Max Mana", "tipo": "rec_max_up", "val": 30, "cor": 6, "peso": 4},
                {"titulo": "Bolsa de Pocoes", "desc": "+2 Pocoes", "tipo": "pocao", "val": 2, "cor": 9, "peso": 3}
            ]
        elif self.classe_escolhida == "Assassino":
            banco_recompensas = [
                {"titulo": "Adagas Venenosas", "desc": "+8 Dano Base", "tipo": "dano", "val": 8, "cor": 8, "peso": 5},
                {"titulo": "Cincho de Stamina", "desc": "+40 Max Stamina", "tipo": "rec_max_up", "val": 40, "cor": 4, "peso": 4},
                {"titulo": "Capa Sombria", "desc": "+15 HP | +10% Esquiva", "tipo": "armadura_magica", "val": 15, "esq": 10, "cor": 13, "peso": 3},
                {"titulo": "Pedra de Amolar", "desc": "+12 Dano / -10 HP", "tipo": "arrriscado", "val": 12, "cor": 11, "peso": 3}
            ]
        else: #guerreiro
            banco_recompensas = [
                {"titulo": "Espada de Aco", "desc": "+6 Dano Base", "tipo": "dano", "val": 6, "cor": 11, "peso": 4},
                {"titulo": "Armadura Pesada", "desc": "+35 HP Maximo", "tipo": "hp_max", "val": 35, "cor": 3, "peso": 4},
                {"titulo": "Cincho de Stamina", "desc": "+30 Max Stamina", "tipo": "rec_max_up", "val": 30, "cor": 4, "peso": 3},
                {"titulo": "Bolsa de Pocoes", "desc": "+2 Pocoes", "tipo": "pocao", "val": 2, "cor": 9, "peso": 2}
            ]

        pool = []
        for item in banco_recompensas:
            for _ in range(item["peso"]):
                pool.append(item)
                
        escolhidos = []
        while len(escolhidos) < 2 and len(pool) > 0:
            item = random.choice(pool)
            if not any(e["titulo"] == item["titulo"] for e in escolhidos):
                escolhidos.append(item)
        self.opcoes_recompensa_atual = escolhidos

    def aplicar_efeito_recompensa(self, item):
        t = item["tipo"]
        v = item["val"]
        if t == "dano":
            self.dano_base += v
        elif t == "hp_max":
            self.hp_max += v
            self.hp_jogador += v
        elif t == "armadura_magica":
            self.hp_max += v
            self.hp_jogador += v
            self.esquiva_chance += item["esq"]
        elif t == "rec_max_up":
            self.max_recurso += v
            self.recurso = self.max_recurso
        elif t == "pocao":
            self.pocoes += v
        elif t == "arrriscado":
            self.dano_base += v
            self.hp_max = max(20, self.hp_max - 10)
            if self.hp_jogador > self.hp_max:
                self.hp_jogador = self.hp_max

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        if self.xp >= self.xp_proximo:
            self.xp -= self.xp_proximo
            self.nivel += 1
            self.xp_proximo = int(self.xp_proximo * 1.5) 
            self.hp_max += 30
            #cura parcial ao upar
            cura_nivel = int(self.hp_max * 0.20)
            self.hp_jogador = min(self.hp_max, self.hp_jogador + cura_nivel)

    def avancar_proxima_fase(self):
        self.estagio += 1
        self.preparar_fase()
        self.gerar_novos_caminhos()
        self.tela = "caminhos"

    def desenhar_fundo(self):
        #renderiza o fundo
        pyxel.cls(0) 
        for y in range(0, 150, 15):
            for x in range(0, 200, 30):
                offset = 15 if (y // 15) % 2 == 0 else 0
                pyxel.rect(x + offset, y + 1, 28, 13, 13)

    #draw (carregamento do jogo)
    def draw(self):
        self.desenhar_fundo()
        
        #menu principal
        if self.tela == "menu":
            pyxel.rect(30, 30, 140, 35, 0)
            pyxel.rectb(30, 30, 140, 35, 7)
            pyxel.text(45, 40, "AVERAGE RPG PYXEL", 7)
            pyxel.text(65, 50, "ROGUELIKE", 6)
            
            pyxel.rect(50, 75, 100, 20, 3)
            pyxel.text(68, 82, "NOVA CAMPANHA", 7)
            
        #classes
        elif self.tela == "selecionar_classe":
            pyxel.text(50, 15, "ESCOLHA SUA CLASSE", 7)
            
            #botao guerreiro
            pyxel.rect(10, 45, 180, 20, 3)
            pyxel.rectb(10, 45, 180, 20, 0)
            pyxel.text(18, 51, "Guerreiro : HP 120 | Dano 18 | Stamina", 7)
            
            #botao assassino
            pyxel.rect(10, 75, 180, 20, 8)
            pyxel.rectb(10, 75, 180, 20, 0)
            pyxel.text(18, 81, "Assassino : HP 95 | Dano 22 | Stamina Alta", 7)
            
            #botao mago
            pyxel.rect(10, 105, 180, 20, 5)
            pyxel.rectb(10, 105, 180, 20, 0)
            pyxel.text(18, 111, "Mago : HP 80 | Dano 26 | Mana & Esquiva", 7)
            
        #tela caminhos
        elif self.tela == "caminhos":
            pyxel.text(45, 12, f"FASE {self.estagio}/{self.max_estagios} - ESCOLHA", 7)
            pyxel.text(20, 24, f"{self.classe_escolhida} | Lv:{self.nivel} | XP: {self.xp}/{self.xp_proximo}", 10)
            
            y_pos = 45
            for op in self.opcoes_caminho_atual:
                pyxel.rect(10, y_pos, 180, 20, op["cor"])
                pyxel.rectb(10, y_pos, 180, 20, 0)
                pyxel.text(18, y_pos + 6, f"{op['titulo']} : {op['desc']}", 7)
                y_pos += 30
            
        #tela recompensas
        elif self.tela == "recompensa":
            pyxel.text(45, 18, "ESCOLHA SEU EQUIPAMENTO", 7)
            pyxel.text(40, 28, "Espolios de guerra encontrados!", 10)
            
            y_pos = 55
            for it in self.opcoes_recompensa_atual:
                pyxel.rect(10, y_pos, 180, 22, it["cor"])
                pyxel.rectb(10, y_pos, 180, 22, 0)
                pyxel.text(18, y_pos + 7, f"{it['titulo']} : {it['desc']}", 7)
                y_pos += 30
            
        #tela batalha
        elif self.tela == "batalha":
            # hud superior
            pyxel.rect(5, 5, 190, 42, 0)
            pyxel.rectb(5, 5, 190, 42, 5)
            
            # status do jogador
            pyxel.text(10, 8, f"HP: {self.hp_jogador}/{self.hp_max}", 7)
            pyxel.text(10, 17, f"[{self.classe_escolhida}] Dano:{self.dano_base}", 6)
            pyxel.text(10, 26, f"{self.nome_recurso}: {self.recurso}/{self.max_recurso}", 12)
            pyxel.text(10, 35, f"Poc: {self.pocoes} | Esq: {self.esquiva_chance}%", 10)
            
            # status do inimigo
            pyxel.text(125, 12, f"{self.nome_inimigo}", 8)
            pyxel.text(125, 24, f"HP: {self.hp_inimigo}", 8)
            
            # carregar as sprites do inimigo dependendo do nome
            if self.nome_inimigo == "Slime":
                pyxel.blt(84, 55, 0, 32, 0, 32, 32, 0)
            elif self.nome_inimigo == "Guarda":
                pyxel.blt(84, 55, 0, 64, 0, 32, 32, 0)
            else:
                pyxel.blt(84, 55, 0, 0, 0, 32, 32, 0) # dragao chefe
            
            #botao de acoes
            if self.turno == "jogador":
                #botao atacar
                pyxel.rect(15, 115, 50, 20, 8)
                pyxel.text(25, 121, "ATACAR", 7)
                
                #btao defender
                pyxel.rect(70, 115, 60, 20, 12)
                pyxel.text(78, 121, "DEFENDER", 7)
                
                #botao curar
                if self.pocoes > 0:
                    pyxel.rect(135, 115, 50, 20, 11)
                    pyxel.text(147, 121, "CURAR", 7)
                else:
                    pyxel.rect(135, 115, 50, 20, 5)
                    pyxel.text(147, 121, "VAZIO", 7)
                
                #avisa q acabo os recurso
                if self.msg_aviso:
                    pyxel.text(20, 98, self.msg_aviso, 8)
                
            elif self.turno == "inimigo_espera":
                cor_msg = 11 if self.msg_inimigo == "ESQUIVOU!" else (8 if self.msg_inimigo == "CRITICO!" else 9)
                pyxel.text(75, 30, self.msg_inimigo, cor_msg)

        #tela vitoria
        elif self.tela == "vitoria":
            pyxel.text(45, 60, "PARABENS! ZEROU O JOGO!", 7)
            pyxel.text(55, 80, "Aperte ESC para sair", 6)
            
        #tela derrota
        elif self.tela == "derrota":
            pyxel.text(70, 60, "VOCE MORREU...", 8)
            pyxel.text(55, 80, "Aperte ESC para sair", 6)

#executa o jogo
RPG()
