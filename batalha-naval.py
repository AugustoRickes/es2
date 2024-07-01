import random, time, os
from colorama import Fore, Style

def cria_matriz(tamanho=5):
    return [["⬜" for _ in range(tamanho)] for _ in range(tamanho)]

def adiciona_navios(matriz): # Thalia (Refatoração)
    adicionar_navio("🚤", matriz, 3)
    adicionar_navio("⛵", matriz, 2)
    adicionar_navio("🚢", matriz, 1)

def adicionar_navio(tipo_navio, matriz, quantidade):
    navios_adicionados = 0
    while navios_adicionados < quantidade:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if pode_colocar_navio(x, y, tipo_navio, matriz):
            if tipo_navio == "⛵":
                if random.choice(["H", "V"]) == "H":
                    matriz[x][y] = "⛵"
                    matriz[x][y + 1] = "⛵"
                else:
                    matriz[x][y] = "⛵"
                    matriz[x + 1][y] = "⛵"
            elif tipo_navio == "🚢":
                if random.choice(["H", "V"]) == "H":
                    matriz[x][y] = "🚢"
                    matriz[x][y + 1] = "🚢"
                    matriz[x][y + 2] = "🚢"
                else:
                    matriz[x][y] = "🚢"
                    matriz[x + 1][y] = "🚢"
                    matriz[x + 2][y] = "🚢"
            else:
                matriz[x][y] = "🚤"
            navios_adicionados += 1

def pode_colocar_navio(x, y, tipo_navio, matriz):
    if tipo_navio == "🚤":
        return matriz[x][y] == "⬜"
    elif tipo_navio == "⛵":
        return (y < 4 and matriz[x][y] == "⬜" and matriz[x][y + 1] == "⬜") or (x < 4 and matriz[x][y] == "⬜" and matriz[x + 1][y] == "⬜")
    elif tipo_navio == "🚢":
        return (y < 3 and matriz[x][y] == "⬜" and matriz[x][y + 1] == "⬜" and matriz[x][y + 2] == "⬜") or (x < 3 and matriz[x][y] == "⬜" and matriz[x + 1][y] == "⬜" and matriz[x + 2][y] == "⬜")
    return False

def mostra_matriz(matriz):
    print("   1   2   3   4   5")
    for i in range(5):
        print(f"{i + 1} ", end="")
        for j in range(5):
            if matriz[i][j] in ["🚤", "⛵", "🚢", "❌", "⬜"]:
                print(f" {matriz[i][j]} ", end="")
            else:
                print("🌊", end="")
        print("\n")
def fazer_ataque(): # Karol adicionar mais tratativas de erro
    while True:
        tentativa = input("informe a linha e a coluna que voce quer atirar ").split()
        if len(tentativa) !=2:
            print("informe a LINHA e a COLUNA separadas por espaco")
            continue
        try:
            x = int(tentativa[0]) - 1
            y = int(tentativa[1]) - 1
            return x, y
        except ValueError:
            print("insira NUMEROS para a LINHA e a COLUNA")

# --------------------------- Programa Principal ---------------------------------------------
def jogar():

    nome = input("Nome do Jogador: ")
    pontos = 0
    hora_inicial = time.time()

    matriz_posicaoNavios = cria_matriz()
    adiciona_navios(matriz_posicaoNavios)
    matriz_atualizada = cria_matriz()

    total_navios = sum(row.count("🚤")+ row.count("⛵") +row.count("🚢") for row in matriz_posicaoNavios)

    while True:
        mostra_matriz(matriz_atualizada)

        x, y = fazer_ataque()
 
        if matriz_posicaoNavios[x][y] in ["🚤","⛵","🚢"]:
            print("Acertou um navio! boa")
            matriz_atualizada[x][y] = matriz_posicaoNavios[x][y]
            matriz_posicaoNavios[x][y] = "⬜"
            pontos += 1
        else:
            print("Vocẽ errou o tiro, tente novamente")
            matriz_atualizada[x][y] = "❌"
            sair = input("Tecle ENTER para continuar E  Q para Desistir: ").upper()
            if sair == "Q":
                break
        if pontos == total_navios :
            print("Você afundou todos os navios e ganhou, parabéns!")
            break

    hora_final = time.time()
    duracao = hora_final-hora_inicial

    print(f"{nome} - Você fez um total de {pontos} pontos!")
    print(f"Tempo: {duracao:.3f} segundos") 

    if os.path.isfile("ranking.txt"):
        with open("ranking.txt", "r") as arq:
            dados = arq.readlines()
    else:
        dados = []

    jogadores = []
    pontuacoes = []
    tempos = []

    for linha in dados:
        partes = linha.split(";")
        jogadores.append(partes[0])
        pontuacoes.append(int(partes[1]))
        tempos.append(float(partes[2]*-1))

    jogadores.append(nome)
    pontuacoes.append(pontos)
    tempos.append(duracao*-1)

    juntas = sorted(zip(pontuacoes, tempos, jogadores), reverse=True)
    pontuacoes2, tempos2, jogadores2 = zip(*juntas)

    print("\nNº Nome do Jogador...: Pontos Tempo......:")
    print("------------------------------------------")

    posicao = 0
    with open("ranking.txt", "w") as arq:
        for jogador, pontuacao, tempo in zip(jogadores2, pontuacoes2, tempos2):
            arq.write(f"{jogador};{pontuacao};{tempo*1:.3f}\n")
            posicao += 1
        if jogador == nome:
            print(Fore.RED + f"{posicao:2d} {jogador:20s}  {pontuacao:4d}  {tempo*-1:7.3f} seg")
            print(Style.RESET_ALL, end="")      
        else:
            print(f"{posicao:2d} {jogador:20s}  {pontuacao:4d}  {tempo*-1:7.3f} seg")

jogar()

#adicionar testes unitários (lilweek)
# adicionar tratativa para não aceitar nome vazio (nath)
# Melhorar quando acerta um navio não deve deixar atacar ali novamente (mensagem de erro) (pedrao)
