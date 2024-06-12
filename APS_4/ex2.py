import cv2
import numpy as np


class Atividade2():
    def __init__(self):
        # Filtro amarelo HSV
        self.lower = (20, 100, 120)
        self.upper = (40,255,255)

    def run(self, bgr: np.ndarray) -> np.ndarray:
        """Esta função deve processar o frame de entrada chamando as funções necessárias. 
        Crie quantas funções auxiliares achar necessário dentro dessa classe ou dentro da classe ImageModule.

        Se desejar pode retornar uma máscara durante o desenvolvimento para facilitar a visualização

        Args:
            bgr (np.ndarray): Frame de entrada

        Returns:
            bgr (np.ndarray): Frame com a atividade 5 desenhada
        """
        # Esta função deve ser implementada para executar a atividade 5
        
        mask = filtra_amarelo(bgr)
        texto = direcao(mask)
        bgr = cv2.putText(bgr, texto, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)



        return bgr


def filtra_amarelo(bgr):

    RodaAtividade = Atividade2()
    lower = RodaAtividade.lower
    upper = RodaAtividade.upper
    bgr_HRV = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(bgr_HRV,lower, upper)
    
    return mask

def direcao(bgr):
    height, width = bgr.shape[:2]


    #cortando em três colunas
    cortado = bgr.copy()
    

    
    
    # Corte Vertical
    tres_cortado_esquerda = cortado[:, :width // 3]
    tres_cortado_centro = cortado[:, width // 3: 2 * width // 3] 
    tres_cortado_direita = cortado[:, 2 * width // 3:] 
    
    
    
    # Calculando Media dos cortes
    tres_cortado_media_esquerda = np.mean(tres_cortado_esquerda)
    tres_cortado_media_centro = np.mean(tres_cortado_centro)
    tres_cortado_media_direita = np.mean(tres_cortado_direita)
    
    # Calculando Areas
    Area_esquerda =(np.sum(tres_cortado_media_esquerda))
    Area_centro = (np.sum(tres_cortado_media_centro))
    Area_direita = (np.sum(tres_cortado_media_direita))
    
    # Condições
    valor = 6
    texto = ' '

    if  (Area_esquerda > valor and  Area_centro > valor and Area_direita > valor):
        print('Cruzamento Detectado')
        texto = 'Cruzamento Detectado'
       
    elif (Area_esquerda > valor  and Area_centro > valor) or (Area_direita > valor  and Area_centro > valor) or (Area_esquerda > valor  and Area_direita > valor):
        print('Curva Detectada')
        texto = 'Curva Detectada'

        
    return texto
    
    
    
    # print(f'Esquerda: {Area_esquerda},Centro: {Area_centro}, Direita: {Area_direita}')

        
    # print(f'Esquerda: {Area_esquerda},Centro: {Area_centro}, Direita: {Area_direita}')

    
    
    

    

def rodar_frame():
    RodaAtividade = Atividade2()
    
    bgr = cv2.imread("img/q2/frame01.png") # Escolha aqui a imagem que deseja usar para testar
    # bgr = cv2.imread("img/q2/frame02.png")
    # bgr = cv2.imread("img/q2/frame03.png")
    # bgr = cv2.imread("img/q2/frame04.png")
    # bgr = cv2.imread("img/q2/cruz01.png")
    # bgr = cv2.imread("img/q2/cruz02.png")
    
    


    bgr = RodaAtividade.run(bgr)

    cv2.imshow("Imagem", bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rodar_video():
    RodaAtividade = Atividade2()

    cap = cv2.VideoCapture('img/q2/pista.mp4') # Confira se o video esta na pasta img/q2

    while(cap.isOpened()):
        ret, bgr = cap.read()

        if ret == True:
            bgr = RodaAtividade.run(bgr)
            cv2.imshow('Frame', bgr)

            if cv2.waitKey(int(1000/60)) & 0xFF == ord('q'): # !!! Pressione q para sair
                break
            
def main():
    # Selecione se deseja rodar seu codigo com uma imagem ou um video:

    # rodar_frame()
    rodar_video()

if __name__ == "__main__":
    main()