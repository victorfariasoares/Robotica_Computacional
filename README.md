# Repositório do Curso de Robótica Computacional

Este repositório contém todas as atividades práticas supervisionadas (APSs) e projetos desenvolvidos durante o curso de Robótica Computacional. Abaixo está uma descrição de cada atividade e dos projetos e arquivos adicionais presentes no repositório.

## Conteúdo

- [APS 1](#aps-1)
- [APS 2](#aps-2)
- [APS 3](#aps-3)
- [APS 4](#aps-4)
- [APS 5](#aps-5)
- [Projetos Adicionais](#projetos-adicionais)
  - [Image Tool](#image-tool)
  - [Reconhecimento de Creeper](#reconhecimento-de-creeper)
  - [Reconhecimento de ArUco](#reconhecimento-de-aruco)
  - [Identificação de Imagem com MobileNet](#identificação-de-imagem-com-mobilenet)
  - [Recepção de Informações do Laser e Odom](#recepção-de-informações-do-laser-e-odom)
  - [Códigos Utilitários para Robô](#códigos-utilitários-para-robô)

## APS 1

**Simulação de Carro Autônomo Desviando de Obstáculos**

Nesta atividade, o objetivo foi treinar o uso de classes e funções em Python, desenvolvendo um programa que simulasse um carro autônomo desviando de obstáculos. A parte visual do programa já estava pronta e utilizava a classe `Mapa` para criar uma grade 2D de 30 linhas e 7 colunas, com células representando paredes (valor 2), o carro (valor 1) e células livres (valor 0).

O desafio consistiu em implementar a lógica de movimentação do carro na classe `Control`, que herdava de `Mapa`. A lógica deveria verificar se havia obstáculos na linha acima do carro e decidir se ele deveria mover-se para a esquerda, para a direita ou continuar para frente. O carro deveria continuar a se mover até alcançar a primeira linha, momento em que deveria parar.


## APS 2

**Criação de Nós Publisher e Subscriber no ROS2**

Nesta atividade, o objetivo foi criar dois nós ROS2 que publicassem e subscrevessem mensagens do tipo std_msgs/String. Esta atividade foi dividida em dois exercícios.

### Exercício 1

Baseando-se no código `first_node.py` do módulo 2, foi necessário criar um nó denominado publisher que publicasse uma mensagem no tópico `publisher` do tipo `std_msgs/String`. A mensagem deveria conter o horário atual em segundos e um contador que começava em 0 e era incrementado a cada mensagem publicada. Ambos deveriam ser separados por um espaço. A mensagem tinha o formato: "{tempo_atual} {contador}". O nó também deveria imprimir no terminal uma mensagem de alerta como: "Ola, são {tempo_atual} e estou publicando pela {contador} vez". O comando `ros2 topic echo /publisher` foi utilizado para verificar se o exercício estava correto.

### Exercício 2

Baseando-se no código second_node.py do módulo 2, foi necessário criar um nó denominado `subscriber` que se inscrevesse no tópico `publisher` do tipo `std_msgs/String`. A cada nova mensagem recebida, a função callback deveria separar o tempo do contador no conteúdo da mensagem. A função deveria calcular o tempo que passou e imprimir o número da mensagem recebida e o delay entre quando a mensagem foi publicada e quando foi recebida, no formato: "Ola, estou recebendo a mensagem: {contador} que demorou {delay} segundos para ser recebida".


## APS 3

**Desenvolvimento de Nós ROS2 para Controle de Robôs**

Nesta atividade, o objetivo foi criar nós ROS2 que permitissem controlar o movimento de robôs reais em diferentes cenários, utilizando odometria e sensores laser. A atividade foi dividida em três exercícios.

### Exercício 1 - Robô Quadrado

Neste exercício, foi criado um nó denominado `quadrado_node`, que fazia o robô real se mover em uma trajetória que se aproximava de um quadrado. O nó tinha dois estados: andar e girar. Utilizou-se a odometria para girar em 90 graus e o método Dead Reckoning para andar os lados do quadrado. Não foram utilizadas funções de sleep; em vez disso, o tempo decorrido foi calculado para controlar a movimentação.

### Exercício 2 - Robô Quase Indeciso

Neste exercício, foi criado um nó denominado `indeciso_node` que fazia com que o robô real se afastasse da parede quando um obstáculo estivesse a menos de 0.95m e se aproximasse quando estivesse a mais de 1.05m, ficando parado em outras situações. O nó tinha três estados: forward, backward e stop.

### Exercício 3 - Robô Limpador

Neste exercício, foi criado um nó denominado `limpador_node` que fazia o robô real mover-se em frente até encontrar um obstáculo a menos de 0.5m. O robô então girava até que o obstáculo mais próximo estivesse à direita inferior (aproximadamente 225 graus), e repetia o processo.


## APS 4

**Conversão 2D->3D e Detecção de Linhas Amarelas e Cruzamentos**

### Exercício 1 - Conversão 2D->3D

Neste exercício, foi realizada a estimativa da distância 𝐷 da webcam até uma folha com um padrão específico, utilizando a geometria do modelo pinhole. Para isso, a imagem foi convertida para o modelo de cor HSV, e foram obtidas as máscaras para os círculos ciano e magenta. A área desses círculos foi calculada e, com base na diferença entre as áreas, determinou-se se a distância seria retornada como -1 ou se seria calculada a média das áreas para obter o diâmetro do círculo e, consequentemente, a distância. Essas informações foram exibidas na imagem. Além disso, foi feita a calibração da câmera utilizando imagens fornecidas, ajustando a função main para capturar vídeo ao vivo e mostrando a distância e o diâmetro do círculo na tela. Um vídeo foi gravado mostrando a implementação, com o link adicionado ao README.md do repositório.

### Exercício 2 - Linha Amarela e Cruzamento

Neste exercício, foi realizada a detecção de linhas amarelas e cruzamentos em um vídeo. Primeiro, filtrou-se a cor amarela do frame, binarizando a imagem e ajustando a máscara para detectar apenas a linha amarela. A imagem foi dividida em três colunas, e a área da linha amarela em cada coluna foi calculada. Se duas colunas tivessem área maior que um valor definido, indicava-se "Curva Detectada" na imagem; se três colunas tivessem área maior que o valor, indicava-se "Cruzamento Detectado". Os parâmetros foram ajustados cuidadosamente para minimizar falsos positivos e garantir detecções corretas. Um vídeo foi gravado mostrando a execução do programa, com o link adicionado ao README.md do repositório.

## APS 5

**Seguindo Linhas e Aproximando-se de Creepers**

### Exercício 1 - Segue Linha

Neste exercício, foi criado um nó denominado `seguidor_node`, no arquivo `segue_linha.py`, que permite ao robô real seguir uma linha amarela no chão. O nó possui dois estados: `centraliza` e `segue`. Um subscriber foi adicionado para se inscrever no tópico de imagem comprimida, direcionando as imagens recebidas para a função `image_callback`. Esta função filtra a faixa amarela na pista e armazena o centro da linha e a largura da imagem nas variáveis `self.x`, `self.y` e `self.w`, respectivamente. A função `image_callback` só é executada se a variável `self.running` for True. No estado `centraliza`, o robô é centralizado na linha amarela, enquanto no estado `segue`, o robô segue a linha amarela movendo-se para frente. Um vídeo mostrando o robô executando esses comportamentos, navegando por uma volta completa na pista sem colidir com obstáculos, foi gravado e o link foi adicionado ao README.md do repositório.

### Exercício 2 - Aproxima Creeper

Neste exercício, foram criados dois nós: `aproxima_node` no arquivo `aproxima.py` e `filtro_cor_node` no arquivo `filtro_cor.py`. O nó `aproxima_node` controla o robô para se aproximar de um creeper de uma cor selecionada. Este nó possui três estados: `segue`, `centraliza` e `stop`. No estado `centraliza`, o robô gira até encontrar o creeper da cor selecionada. No estado `segue`, o robô se aproxima do creeper e, ao estar a menos de 0.5m do creeper, entra no estado `stop` e para. Se o creeper for retirado da frente do robô, ele volta ao estado `centraliza`. O nó `filtro_cor_node` filtra a cor do creeper e publica uma mensagem do tipo `geometry_msgs/Point` com a posição do creeper na imagem (x, y) e a largura da imagem (z).

## Projeto do Semestre

**Descrição das Missões**

O projeto do semestre é composto por quatro missões de complexidade crescente, envolvendo tanto o design de software quanto a utilização dos sensores e comportamentos do robô. 

### Missão C

Nesta missão, o robô deve visitar todos os locais onde os creepers podem aparecer, identificar e armazenar suas posições em um dicionário. O robô começa na posição inicial e, ao encontrar um creeper, registra sua localização. Após encontrar todos os creepers, o robô retorna à posição inicial e imprime o dicionário com as posições dos creepers.

### Missão B

Nesta missão, o robô deve ser capaz de derrubar um creeper específico com base na cor e ID fornecidos como argumento na linha de comando. O robô localiza e derruba o creeper desejado, retorna à pista e volta à posição inicial, onde para.

### Missão A

Nesta missão, o robô deve pegar um creeper específico, novamente definido pela cor e ID fornecidos como argumento na linha de comando, e entregá-lo na drop area especificada. O robô localiza o creeper desejado, o pega, transporta-o até a drop area e, em seguida, retorna à posição inicial e para.

## Projetos Adicionais

### Image Tool

Ferramenta desenvolvida para manipulação de imagens, incluindo funcionalidades como carregamento, processamento e visualização de imagens.

### Reconhecimento de Creeper

Código para reconhecimento de creeper utilizando técnicas de visão computacional. Inclui detecção e identificação de creepers em imagens.

### Reconhecimento de ArUco

Código para reconhecimento de marcadores ArUco. Este projeto envolve a detecção e identificação de marcadores ArUco em imagens e vídeos.

### Identificação de Imagem com MobileNet

Projeto que utiliza a arquitetura MobileNet para identificar e classificar imagens. Inclui exemplos de uso e código para treino e inferência.

### Recepção de Informações do Laser e Odom

Código responsável por receber e processar informações de sensores laser e odometria do robô. Inclui exemplos de uso e integração com outros sistemas do robô.

### Códigos Utilitários para Robô

Diversos códigos utilitários que podem ser usados para diferentes atividades do robô, como seguir linha, girar uma certa quantidade de graus, entre outros.
