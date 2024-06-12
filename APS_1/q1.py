import time
from util import Mapa

class Control(Mapa): # Herdando de Mapa
    def __init__(self):
        # Inicializa a classe Pai
        Mapa.__init__(self)

        self.robot_state = 'forward'
        self.state_machine = {
            'forward': self.forward,
            'left': self.left,
            'right': self.right,
            'stop': self.stop,
        }
    
    def forward(self) -> None:
        # Move subtraindo 1 uma linha
        proxima_linha = self.posicao[0] - 1
        proxima_coluna = self.posicao[1]

        # Mapa().grade = Mapa().grade[:-1]

        # Atualiza a posição
        nova_position = (proxima_linha, proxima_coluna)
        self.atualizar_posicao(nova_position)
        pass

    def left(self) -> None:
        # Move subtraindo 1 uma coluna
        linha_atual = self.posicao[0]
        coluna_da_esquerda = self.posicao[1] - 1

        # Atualiza a posição
        nova_position = (linha_atual, coluna_da_esquerda)
        self.atualizar_posicao(nova_position)
        pass

    def right(self) -> None:
        # Move somando 1 uma coluna
        linha_atual = self.posicao[0]
        coluna_da_direita = self.posicao[1] + 1

        # Atualiza a posição
        nova_position = (linha_atual, coluna_da_direita)
        self.atualizar_posicao(nova_position)
        pass
    
    def stop(self) -> None:
        # Não faz nada
        pass

    def control(self) -> None:
        # Verifique se a posição acima está livre, se sim, mova para cima.
        linha_atual = self.posicao[0]
        coluna_atual = self.posicao[1]
        linha_da_frente = self.posicao[0] - 1
        coluna_da_frente = self.posicao[1]

        grade = self.grade

        # Pare quando estiver na primeira linha.
        if abs(linha_da_frente) > len(grade):
            self.state_machine['stop']()
            self.robot_state = 'stop'
        else:
            if grade[linha_da_frente, coluna_da_frente] == 0:
                self.state_machine['forward']()
                self.robot_state = 'forward'
            # Se não, verifique se a posição à esquerda ou à direita está livre, se sim, mova para um dos lados.
            elif coluna_da_frente < len(grade[0]) - 1 and grade[linha_atual, coluna_da_frente + 1] == 0:
                self.state_machine['right']()
                self.robot_state = 'right'
            elif grade[linha_atual, coluna_atual - 1] == 0 and coluna_atual > 0:
                self.state_machine['left']()
                self.robot_state = 'left'
            
        
        # Mostre a grade atual
        self.mostrar()
        
        pass
        
def main():
    control = Control()
    control.mostrar()

    i = 40
    
    while not control.robot_state == 'stop' and i > 0:
        control.control()
        time.sleep(0.1)
        i -= 1

if __name__=="__main__":
    main()