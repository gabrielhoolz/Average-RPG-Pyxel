import pyxel

class MeuRPG:
    def __init__(self):
        pyxel.init(160, 120, title="RPG de Turnos")
        
        # mouse
        pyxel.mouse(True)
        
        # variavel da tela
        self.tela = "menu"
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        # logica menu
        if self.tela == "menu":
            # bottao esquerdo
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # verifica se ta na tela
                if 40 <= pyxel.mouse_x <= 120 and 50 <= pyxel.mouse_y <= 70:
                    self.tela = "batalha" # troca a tela

    def draw(self):
        pyxel.cls(0)
        
        if self.tela == "menu":
            # desenho do botao
            pyxel.rect(40, 50, 80, 20, 1)
            pyxel.text(55, 57, "NOVA CAMPANHA", 7)
            
        elif self.tela == "batalha":
            pyxel.text(45, 50, "CHEFE ENCONTRADO!", 8)
            pyxel.text(10, 100, "Aperte Q para sair", 7)

MeuRPG()