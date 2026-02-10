import copy
import sys
import random

class MiniJogo:
    
    #Construtor
    def __init__(self, jogo, ganhado, jogador):
        self.jogo = jogo
        self.ganhado = ganhado
        self.jogador = jogador

    #Metodo usado para a linha para o print do jogo_grande
    def imprimindo_linha(self, linha:int):
        return self.jogo[linha]
    
    #Metodo usado para imprimir um MiniJogo
    def imprimindo_mini_jogo(self):
        print("    1   2   3") #Numeros da coluna

        for i in range(3): #Seleciona a linha a ser impressa
            linha = str(i+1) + "   " + str(' | '.join(self.jogo[i]))#Linha a ser impressa, ja contem a numeração

            # for g in range (3): #Seleciona os numeros a serem colocados - Monta a linha
            #     if(self.jogo[i][g] == ''): #Se não tiver sido marcado linha recebe espaço
            #         linha += "   "
            #     else:
            #         linha += " " + self.jogo[i][g] + " " #Se tiver sido marcado coloca o simbulo
                
            #     if(g!=2): #Verifica se deve colocar traço entre as colunas, se for a ultiza, não precisa
            #         linha += "|"
            #     else:
            #         linha += ""
            
            
            print(linha) #imprimi a linha
            if(i!= 2): #Demarca o final da linha se não for a ultima
                print("   -----------")
        print(self.ganhado)

    def trocando_jogo(self, simbulo:str):
        self.jogo = [
            ['*','*','*'],
            ['*',simbulo,'*'],
            ['*','*','*']

        ]
    #Metodo usado para verificar venceder -> Muda ganhado e jogador
    def verificando_vencedor(self):

        #HORIZONTAL
        for i in self.jogo: #Traz as linhas
            set_jogadores = set(i)

            if len(set_jogadores) == 1 and next(iter(set_jogadores)) != ' ':
                self.ganhado = True
                self.jogador = next(iter(set_jogadores))
                return

        
        #DIAGONAL
        #Como existem apenas duas vertical, optei por mapear cada e 
        # depois apenas verificar se os simbulos são iguais.
        #Tambem verifico se o meio nao esta vazio antes, pois se estiver sequer vale a pena 
        if(self.jogo[1][1] != ' '):
            if self.jogo[0][0] == self.jogo[1][1] and self.jogo[2][2] == self.jogo[1][1]:
                self.ganhado = True
                self.jogador = self.jogo[1][1]
                return
            
            if self.jogo[2][0] == self.jogo[1][1] and self.jogo[0][2] == self.jogo[1][1]:
                self.ganhado = True
                self.jogador = self.jogo[1][1]
                return
            
        #VERTICAL
        #Aqui cada coluna da vertical é montada, depois verifica se todos 
        # são iguais e sem não contem ' '
        for coluna in range(3):
            resultado = []
            for linha in range(3):
                resultado.append(self.jogo[linha][coluna])

            if len(set(resultado)) == 1 and ' ' not in resultado:
                self.ganhado = True
                self.jogador = resultado[0]
                return
        

    #Verifica se o jogo esta empatado qunado a matriz esta cheia
    def esta_empatada(self):
        global rodadas
        #Montando set dos valores do jogo
        valores = set()

        for linha in self.jogo:
            for coluna in linha:
                valores.add(coluna)

        #Se ela estiver cheia e ninguem tiver ganhado, reseta
        if (' ' not in valores) and (self.ganhado == False):
            print("Nananinão! Odiamos empate nesse jogo! Vamos resetar os valores desse aqui! O jogo continua normalmente")
            self.jogo = [
                [' ', ' ', ' '],
                [' ', ' ', ' '],
                [' ', ' ', ' ']
            ]
            rodadas -= 9

        
    #Aqui ocorrem uma serie 
    def adicionando_jogada(self, posicao:str, jogador:str) -> str:
        while True:
            try:#Tenta adicionar
                linha = int(posicao[0]) - 1
                coluna = int(posicao[1]) - 1

                if self.jogo[linha][coluna] == ' ':
                    self.jogo[linha][coluna] = jogador
                    break

                else:#Se ja houver um valor naquela posição
                    print("Posição invalida!")
                    posicao = str(input("Tente de novo: "))
                    continue

            #SE o valor tiver erro de escrita ele lança essa mensagem e pede outro valor
            except (ValueError, IndexError, TypeError):
                print('Valor não valido, coloque uma combinação de dois numero de 1 a 3')
                posicao = str(input("Tente de novo: "))

        self.verificando_vencedor()
        if self.ganhado == True:
            self.trocando_jogo(self.jogador)
        self.esta_empatada()
        return posicao



#A partir daqui começa as funçoes do jogo grande e que auxiliam no gerenciamento dele

#Essa funcao é responsavel por auxiliar em dizer quem esta jogando Par == X e Impar == O
def ePar(numero : int) -> bool:
    if numero % 2 == 0:
        return True
    else:
        return False

def imprimindoJogoGrande():
    for i in range(3):#Define a linha do jogo grande
        for gg in range(3): #Define a linha do MiniJogo
            linha = str(gg+1) + ''
            for g in range (3): #Define a coluna do jogo grande
                jogo = jogo_grande[i][g]
                linha += "  " + str(MiniJogo.imprimindo_linha(jogo, gg))

                if g != 2:
                    linha += "  |"
            print(linha)

        if(i!= 2):
             print(" -------------------+-------------------+-------------------")

def criandoJogoGrande():
    jogo_pequeno_matriz = [
        [' ', ' ',' '],
        [' ',' ',' '],
        [' ',' ',' ']
    ]

    for linha in range(3):
        for coluna in range(3):
            jogo_pequeno = MiniJogo(copy.deepcopy(jogo_pequeno_matriz), False, None)
            jogo_grande[linha][coluna] = jogo_pequeno

#Para se qualificar como vencido, uma linha toda tem que estar Ganhado == True e vencedor iguais
def existe_vencedor_grande() -> bool:
    listaDeGanhado = [] #True e False -
    setDeVencedor = set() #X e O

    #HORIZONTAL
    #Ele monta uma linha e verifica se so existe um unico vencedor e se todos os jogos estão vencidos
    for j in jogo_grande: #Aqui ele pega a linha do jogo grande
        for jj in j: #Aqui ele pega um jogo 3X
            listaDeGanhado.append(jj.ganhado)
            setDeVencedor.add(jj.jogador)
            
        if listaDeGanhado.count(True) == 3 and len(setDeVencedor) == 1:
            return [True, next(iter(setDeVencedor))]
        
        listaDeGanhado.clear()
        setDeVencedor.clear()

    #DIAGONAL
    listaDeGanhado.clear()
    setDeVencedor.clear()

    #Monto uma diagonal
    for i in range(3):
        listaDeGanhado.append(jogo_grande[i][i].ganhado)
        setDeVencedor.add(jogo_grande[i][i].jogador)

    if listaDeGanhado.count(True) == 3 and len(setDeVencedor) == 1:
            return [True, next(iter(setDeVencedor))]
    
    listaDeGanhado.clear()
    setDeVencedor.clear()

    #Monto outra diagonal
    for coluna in range(3):
            linha = 2
            listaDeGanhado.append(jogo_grande[linha][coluna].ganhado)
            setDeVencedor.add(jogo_grande[linha][coluna].jogador)
            linha-= 1

    if listaDeGanhado.count(True) == 3 and len(setDeVencedor) == 1:
            return [True, next(iter(setDeVencedor))]
    
    listaDeGanhado.clear()
    setDeVencedor.clear()

    #VERTICAL
    for coluna in range(3):
        for linha in range(3):
            listaDeGanhado.append(jogo_grande[linha][coluna].ganhado)
            setDeVencedor.add(jogo_grande[linha][coluna].jogador)

        if listaDeGanhado.count(True) == 3 and len(setDeVencedor) == 1:
            return [True, next(iter(setDeVencedor))]
        
        listaDeGanhado.clear()
        setDeVencedor.clear()

    return[False, 'V']

#Função que escolhe o novo jogo caso o seguinte ja esteja vencido
def escolhendo_minijogo_aleatorio():
    print("Esse jogo já foi vencido! Então vamos para um jogo aleatorio!")
    indice_minijogo_novo = random.randint(0, len(lista_de_jogos_disponiveis) - 1)
    novo_minijogo = lista_de_jogos_disponiveis[indice_minijogo_novo]

    return [int(novo_minijogo[0]),int(novo_minijogo[1])]

def tirando_quando_ganha(mini_jogo:MiniJogo):
    if mini_jogo.ganhado == True:
        jogo = str(linha_grande) + str(coluna_grande)
        lista_de_jogos_disponiveis.remove(jogo)
#Aqui começao jogo de fato

#Preparacoes
jogo_grande = [
    ['','',''],
    ['','',''],
    ['','','']
]

lista_de_jogos_disponiveis = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
criandoJogoGrande()
imprimindoJogoGrande()
rodadas = 0
simbulo = ''

#Gerenciamento

jogo_em_questão = str(input("Jogador X! Digide onde o jogo vai começar no jogo grande: "))
linha_grande = int(jogo_em_questão[0]) - 1
coluna_grande = int(jogo_em_questão[1]) - 1

while rodadas<81:

    if ePar(rodadas):
        simbulo = 'X'
    else:
        simbulo= 'O'
    
    imprimindoJogoGrande()

    if (str(linha_grande) + str(coluna_grande)) not in lista_de_jogos_disponiveis:
        novo_jogo = escolhendo_minijogo_aleatorio()
        linha_grande = (novo_jogo[0])
        coluna_grande = (novo_jogo[1])

    print("\nJogo em questão: " + str(linha_grande + 1) + str(coluna_grande + 1))
    MiniJogo.imprimindo_mini_jogo(jogo_grande[linha_grande][coluna_grande])
    
    posicao = str(input("Jogador " + simbulo + " digite sua posição: "))
    print("\n")

    posicao = MiniJogo.adicionando_jogada(jogo_grande[linha_grande][coluna_grande], posicao, simbulo)

    tirando_quando_ganha(jogo_grande[linha_grande][coluna_grande])

    alguem_ganhou = existe_vencedor_grande()
    if alguem_ganhou[0] == True:
        print("Jogador " + alguem_ganhou[1] + " ganhou!")
        imprimindoJogoGrande()
        sys.exit()

    linha_grande = int(posicao[0]) - 1
    coluna_grande = int(posicao[1]) - 1
    rodadas += 1

print("Empate!? Que absurdo!")