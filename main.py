import pyxel

class RPG:
    def __init__(self):
        pyxel.init(160, 120, title="Avarage RPG Pyxel")
        pyxel.mouse(True)
        self.tela = "menu"
        
        self.hp_jogador = 100
        self.hp_max_jogador = 100 # trava para n ter sobrevida
        self.hp_chefe = 150
        self.turno = "jogador"
        
        # pocoes defesa tempo
        self.pocoes = 3
        self.defendendo = False
        self.timer_chefe = 0
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if self.tela == "menu":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if 40 <= pyxel.mouse_x <= 120 and 50 <= pyxel.mouse_y <= 70:
                    self.tela = "batalha"
                    
        elif self.tela == "batalha":
            if self.hp_chefe <= 0:
                self.tela = "vitoria"
            elif self.hp_jogador <= 0:
                self.tela = "derrota"
            
            # turno do jogador
            elif self.turno == "jogador":
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    
                    # botao atacar
                    if 10 <= pyxel.mouse_x <= 45 and 90 <= pyxel.mouse_y <= 105:
                        self.hp_chefe -= 15
                        self.defendendo = False
                        self.turno = "chefe_espera"
                        self.timer_chefe = 30
                        
                    # botao defender
                    elif 50 <= pyxel.mouse_x <= 95 and 90 <= pyxel.mouse_y <= 105:
                        self.defendendo = True
                        self.turno = "chefe_espera"
                        self.timer_chefe = 30
                        
                    # botao curar
                    elif 100 <= pyxel.mouse_x <= 140 and 90 <= pyxel.mouse_y <= 105:
                        if self.pocoes > 0:
                            self.hp_jogador += 30
                            # limite vida
                            if self.hp_jogador > self.hp_max_jogador:
                                self.hp_jogador = self.hp_max_jogador
                            
                            self.pocoes -= 1
                            self.defendendo = False
                            self.turno = "chefe_espera"
                            self.timer_chefe = 30
                        
            # turno chefe tempo
            elif self.turno == "chefe_espera":
                self.timer_chefe -= 1
                if self.timer_chefe <= 0:
                    self.turno = "chefe_ataque"
                    
            # turno chefe dano
            elif self.turno == "chefe_ataque":
                dano_chefe = 10
                
                if self.defendendo:
                    dano_chefe = 5 
                    
                self.hp_jogador -= dano_chefe
                self.turno = "jogador"

    def draw(self):
        pyxel.cls(0)
        
        if self.tela == "menu":
            pyxel.rect(40, 50, 80, 20, 1)
            pyxel.text(55, 57, "NOVA CAMPANHA", 7)
            
        elif self.tela == "batalha":
            pyxel.text(5, 5, f"Seu HP: {self.hp_jogador}", 11)
            pyxel.text(100, 5, f"Chefe HP: {self.hp_chefe}", 8)
            pyxel.text(5, 15, f"Pocoes: {self.pocoes}", 10)
            
            if self.turno == "jogador":
                # desenho atacar
                pyxel.rect(10, 90, 35, 15, 5)
                pyxel.text(14, 95, "ATACAR", 7)
                
                # desenho defesa
                pyxel.rect(50, 90, 45, 15, 13)
                pyxel.text(56, 95, "DEFENDER", 7)
                
                # desenho curar
                if self.pocoes > 0:
                    pyxel.rect(100, 90, 35, 15, 11)
                    pyxel.text(106, 95, "CURAR", 7)
                else:
                    # desliga se acaba
                    pyxel.rect(100, 90, 35, 15, 13)
                    pyxel.text(106, 95, "VAZIO", 7)
                
            elif self.turno == "chefe_espera":
                pyxel.text(40, 50, "O Chefe ataca!", 9)

        elif self.tela == "vitoria":
            pyxel.text(50, 50, "VOCE VENCEU!", 11)
            pyxel.text(10, 100, "Aperte Q para sair", 7)
            
        elif self.tela == "derrota":
            pyxel.text(50, 50, "VOCE MORREU...", 8)
            pyxel.text(10, 100, "Aperte Q para sair", 7)

RPG()