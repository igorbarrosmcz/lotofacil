import sqlite3
import random
from collections import Counter
import datetime
import os

DATABASE_PATH = "lotofacil.db"
ULTIMOS_CONCURSOS = 50  # Ajustado para pegar os últimos 50 concursos
ULTIMOS_JOGOS_NO_TXT = 30  # Número de jogos recentes a serem salvos no arquivo
NUM_JOGOS = 3  # Quantidade de jogos a serem gerados
PASTA_APOSTAS = "Apostas"  # Nome da pasta onde os jogos serão salvos

def buscar_resultados(banco_de_dados, limite=None):
    """Busca concursos no banco de dados. Se limite for None, retorna todos."""
    try:
        with sqlite3.connect(banco_de_dados) as conn:
            cursor = conn.cursor()
            if limite:
                cursor.execute('''
                    SELECT concurso, dezenas FROM lotofacil
                    ORDER BY concurso DESC
                    LIMIT ?
                ''', (limite,))
            else:
                cursor.execute('''
                    SELECT concurso, dezenas FROM lotofacil
                    ORDER BY concurso DESC
                ''')
            resultados = cursor.fetchall()
        return [(row[0], row[1].split(",")) for row in resultados]
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return []


def calcular_estatisticas(dezenas):
    """Calcula a frequência das dezenas nos últimos concursos."""
    todas_dezenas = [int(dezena) for _, sublista in dezenas for dezena in sublista]
    return Counter(todas_dezenas).most_common()

def gerar_jogos(estatisticas, num_jogos=NUM_JOGOS):
    """Gera múltiplos jogos com maior probabilidade de acerto."""
    if len(estatisticas) < 15:
        print("Estatísticas insuficientes para gerar jogos confiáveis.")
        return []

    jogos = []
    
    for _ in range(num_jogos):
        # Pegamos as 10 dezenas mais frequentes
        top_10 = [num for num, _ in estatisticas[:10]]

        # Escolhemos 5 aleatórias entre as restantes
        restantes = [num for num, _ in estatisticas[10:]]
        top_5 = random.sample(restantes, 5) if len(restantes) >= 5 else restantes

        # Adicionamos o jogo ordenado à lista de jogos
        jogos.append(sorted(top_10 + top_5))

    return jogos

def salvar_jogos(jogos, ultimos_jogos):
    """Salva os jogos gerados e os últimos 30 concursos em um arquivo de texto."""
    if not jogos:
        print("Nenhum jogo foi gerado para salvar.")
        return

    # Verificar se a pasta Apostas existe, senão cria
    if not os.path.exists(PASTA_APOSTAS):
        os.makedirs(PASTA_APOSTAS)

    # Definindo o caminho completo do arquivo
    data_atual = datetime.datetime.now().strftime("%d.%m.%Y")
    arquivo = os.path.join(PASTA_APOSTAS, f"jogos_recomendados_{data_atual}.txt")

    try:
        with open(arquivo, "w") as f:
            f.write("Jogos recomendados com maior probabilidade:\n")
            f.write("-" * 40 + "\n")
            
            for i, jogo in enumerate(jogos, 1):
                f.write(f"Jogo {i}: " + " ".join(f"{num:02d}" for num in jogo) + "\n")
            
            f.write("\nÚltimos 10 jogos sorteados:\n")
            f.write("-" * 40 + "\n")
            for concurso, dezenas in ultimos_jogos[:ULTIMOS_JOGOS_NO_TXT]:
                f.write(f"Concurso {concurso}: " + " ".join(f"{int(num):02d}" for num in dezenas) + "\n")

        print(f"Jogos salvos no arquivo '{arquivo}' com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar jogos no arquivo: {e}")

def main():
    resultados = buscar_resultados(DATABASE_PATH, limite=None)  # Pegando todos os concursos
    if not resultados:
        print("Nenhum dado encontrado. Verifique o banco de dados.")
        return

    estatisticas = calcular_estatisticas(resultados)
    jogos = gerar_jogos(estatisticas)

    if jogos:
        print("Jogos sugeridos:")
        for i, jogo in enumerate(jogos, 1):
            print(f"Jogo {i}: {jogo}")
        salvar_jogos(jogos, resultados)
    else:
        print("Não foi possível gerar jogos.")
