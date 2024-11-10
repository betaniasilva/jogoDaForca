from random import choice
import string
import os
import time

# Função para limpar o terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para salvar o ranking com tempo de duração
def salvar_ranking(nome, pontuacao, duracao):
    with open('ranking.txt', 'a') as arquivo:
        arquivo.write(f"{nome} - {pontuacao} - {duracao:.3f} segundos\n")

# Função para exibir o ranking
def exibir_ranking():
    if os.path.exists('ranking.txt'):
        print("\nRanking dos Jogadores:")
        with open('ranking.txt', 'r') as arquivo:
            linhas = arquivo.readlines()
            pontuacoes = []
            for linha in linhas:
                try:
                    # Dividir a linha e converter pontuação e tempo
                    nome, pontos, tempo = linha.strip().split(" - ")
                    pontos = int(pontos)
                    tempo = float(tempo.split()[0])
                   # Converter tempo para float
                    pontuacoes.append((nome, pontos, tempo))
                except ValueError:
                    print(f" {linha}")
            
            # Ordenar por pontuação (descrescente) e tempo (ascendente)
            pontuacoes.sort(key=lambda x: (-x[1], x[2]))

            # Exibir o ranking
            for nome, pontos, tempo in pontuacoes:
                print(f"{nome} - {pontos} pontos - {tempo:.3f} segundos")
    else:
        print("\nNenhum ranking disponível.")

# Carregar a lista de palavras
with open('palavras.txt') as arquivo:
    linhas = arquivo.read().strip()
    lista_palavras = linhas.split('\n')

# Escolher uma palavra aleatória
palavra = choice(lista_palavras).upper()

# Determinar o multiplicador de pontuação com base no tamanho da palavra
if len(palavra) >= 10:
    multiplicador = 2
elif len(palavra) >= 7:
    multiplicador = 1.5
else:
    multiplicador = 1

# Estados do boneco para cada erro
forca = """ 
____
    |
    |
-"""

vazio = """
"""

cabeca = """
   😂
"""

tronco = """
   😂
    |
"""

braco_esquerdo = """
   😂
   /|
"""

braco_direito = """
   😂
   /|\\
"""

perna_direito = """
   😂
   /|\\
   /
"""

perna_esquerda = """
   😂
   /|\\
   / \\
"""

# Lista de partes do boneco
chances_do_boneco = [vazio, cabeca, tronco, braco_esquerdo, braco_direito, perna_direito, perna_esquerda]

# Variáveis de controle
erros = 0
letras_acertadas = []
letras_erradas = []
pontos_jogador = 0
jogo_sem_erros = True  # Variável para rastrear se o jogador não errou

# Nome do Jogador
limpar_tela()  # Limpar a tela no início do jogo
print("-" * 46)
print("| Bem-vindo ao jogo da forca!                 |")
print(f"| A palavra tem {len(palavra)} letras        ")
print("| Você tem 6 chances para acertar a palavra.  |")
print("| Boa sorte!                                  |")
print("-" * 46)

nome_jogador = input("Nome do Jogador: ")
hora_inicial = time.time()

# Letras disponíveis para escolha
letras_disponiveis = list(string.ascii_uppercase)

# Loop principal do jogo
while True:
    limpar_tela()  # Limpar a tela no início de cada rodada

    # Exibir o estado do boneco
    print(forca + chances_do_boneco[erros])

    # Exibir a palavra com traços e letras acertadas abaixo da forca
    mensagem = ''
    for letra in palavra:
        if letra in letras_acertadas:
            mensagem += f'{letra} '
        else:
            mensagem += '_ '
    print(mensagem.strip())  # Remover o último espaço

    # Exibir letras disponíveis
    print("-" * 90)
    print("Letras disponíveis: ", ' '.join(letras_disponiveis))
    print("-" * 90)

    # Verificar condição de vitória
    if all(letra in letras_acertadas for letra in palavra):
        print(f"Parabéns, {nome_jogador}! Você acertou a palavra!")
        break

    # Verificar condição de derrota
    if erros == 6:
        print("Você perdeu! A palavra era:", palavra)
        jogo_sem_erros = False  # Não aplicará o bônus de perfeição
        break

    # Mostrar o placar atual
    print(f"\nPontos: {pontos_jogador}")

    # Pedir uma letra ao jogador
    letra = input(f"{nome_jogador}, digite uma letra: ").upper().strip()

    # Validar se a letra já foi escolhida ou não está disponível
    if letra not in letras_disponiveis:
        print('Você já tentou essa letra ou a letra não é válida!')
        input("Pressione Enter para continuar...")  # Esperar o jogador ler a mensagem
        continue

    # Remover a letra das letras disponíveis
    letras_disponiveis.remove(letra)

    # Verificar se a letra está na palavra
    if letra in palavra:
        print('Você acertou a letra!')
        letras_acertadas.append(letra)
        pontos_jogador += 10 * palavra.count(letra)  # 10 pontos por letra correta

    else:
        print('Você errou a letra!')
        letras_erradas.append(letra)
        pontos_jogador -= 5  # -5 pontos por erro
        erros += 1
        jogo_sem_erros = False  # Marcar que houve um erro

    # Exibir informações de debug (opcional)
    print("-" * 46)
    print(f"Letras acertadas: {letras_acertadas}")
    print(f"Letras erradas: {letras_erradas}")
    print(f"Erros: {erros}")
    print("-" * 46)

    # Esperar um momento para o jogador ler o feedback antes de limpar a tela
    input("Pressione Enter para continuar...")

# Calcular a duração do jogo
hora_final = time.time()
duracao = hora_final - hora_inicial

# Aplicar bônus de tempo
if duracao < 30:
    pontos_jogador += 20
elif duracao <= 60:
    pontos_jogador += 10

# Aplicar o multiplicador de dificuldade
pontos_jogador *= multiplicador

# Bônus de perfeição se o jogador não tiver cometido erros
if jogo_sem_erros:
    pontos_jogador += 50

# Exibir pontuação final e duração do jogo
print("-"*40)
print(f"{nome_jogador}, você fez um total de {pontos_jogador} pontos")
print(f"Duração do Jogo: {duracao:.3f} segundos")

# Salvar a pontuação do jogador no ranking com tempo de jogo
salvar_ranking(nome_jogador, int(pontos_jogador), duracao)

# Exibir o ranking após o jogo
exibir_ranking()
