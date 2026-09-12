import pyxel
import random
import os

class RPG:
    def __init__(self):
        pyxel.init(160, 120, title="Average RPG Pyxel")
        pyxel.mouse(True)
        
        # identificar local da imagem
        pasta_do_jogo = os.path.dirname(os.path.abspath(__file__))
        caminho_da_arte = os.path.join(pasta_do_jogo, "rpg.pyxres")
        
        try:
            pyxel.load(caminho_da_arte)
        except:
            pass
            
        self.tela = "menu"
        
        self.hp_jogador = 100
        self.hp_max = 100
        self.hp_chefe = 150
        self.turno = "jogador"
        
        self.pocoes = 3
        self.defendendo = False
        
        self.timer_chefe = 0
        self.dano_pendente = 0
        self.msg_chefe = ""
        
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
            
            elif self.turno == "jogador":
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    
                    if 10 <= pyxel.mouse_x <= 45 and 90 <= pyxel.mouse_y <= 105: # ataque
                        self.hp_chefe -= 15
                        self.defendendo = False
                        self.turno = "chefe_decide"
                        
                    elif 50 <= pyxel.mouse_x <= 95 and 90 <= pyxel.mouse_y <= 105: # defende
                        self.defendendo = True
                        self.turno = "chefe_decide"
                        
                    elif 100 <= pyxel.mouse_x <= 140 and 90 <= pyxel.mouse_y <= 105: # cura
                        if self.pocoes > 0:
                            self.hp_jogador += 30
                            if self.hp_jogador > self.hp_max:
                                self.hp_jogador = self.hp_max
                            self.pocoes -= 1
                            self.defendendo = False
                            self.turno = "chefe_decide"
                        
            elif self.turno == "chefe_decide":
                chance = random.randint(1, 100)
                
                if chance <= 20: 
                    self.dano_pendente = 25
                    self.msg_chefe = "ATAQUE CRITICO!"
                else: 
                    self.dano_pendente = random.randint(8, 12)
                    self.msg_chefe = "O Chefe ataca!"
                
                if self.defendendo:
                    self.dano_pendente = self.dano_pendente // 2 
                    
                self.timer_chefe = 45 
                self.turno = "chefe_espera"
                    
            elif self.turno == "chefe_espera":
                self.timer_chefe -= 1
                if self.timer_chefe <= 0:
                    self.hp_jogador -= self.dano_pendente
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
            
            pyxel.blt(64, 30, 0, 0, 0, 32, 32, 0)
            
            if self.turno == "jogador":
                pyxel.rect(10, 90, 35, 15, 5)
                pyxel.text(14, 95, "ATACAR", 7)
                
                pyxel.rect(50, 90, 45, 15, 13)
                pyxel.text(56, 95, "DEFENDER", 7)
                
                if self.pocoes > 0:
                    pyxel.rect(100, 90, 35, 15, 11)
                    pyxel.text(106, 95, "CURAR", 7)
                else:
                    pyxel.rect(100, 90, 35, 15, 13)
                    pyxel.text(106, 95, "VAZIO", 7)
                
            elif self.turno == "chefe_espera":
                cor_msg = 8 if self.msg_chefe == "ATAQUE CRITICO!" else 9
                pyxel.text(55, 15, self.msg_chefe, cor_msg)

        elif self.tela == "vitoria":
            pyxel.text(50, 50, "VOCE VENCEU!", 11)
            pyxel.text(10, 100, "Aperte Q para sair", 7)
            
        elif self.tela == "derrota":
            pyxel.text(50, 50, "VOCE MORREU...", 8)
            pyxel.text(10, 100, "Aperte Q para sair", 7)

RPG()