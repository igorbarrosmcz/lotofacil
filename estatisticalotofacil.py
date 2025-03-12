import sqlite3
import random
from collections import Counter
import datetime

DATABASE_PATH = "lotofacil.db"
ULTIMOS_CONCURSOS = 50  # Ajustado para pegar os últimos 50 concursos
ULTIMOS_JOGOS_NO_TXT = 10  # Número de jogos recentes a serem salvos no arquivo

def buscar_resultados(banco_de_dados, limite=ULTIMOS_CONCURSOS):
    """Busca os últimos concursos no banco de dados."""
    try:
        with sqlite3.connect(banco_de_dados) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT concurso, dezenas FROM lotofacil
                ORDER BY concurso DESC
                LIMIT ?
            ''', (limite,))
            resultados = cursor.fetchall()
        return [(row[0], row[1].split(",")) for row in resultados]
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return []

def calcular_estatisticas(dezenas):
    """Calcula a frequência das dezenas nos últimos concursos."""
    todas_dezenas = [int(dezena) for _, sublista in dezenas for dezena in sublista]
    return Counter(todas_dezenas).most_common()

def gerar_jogo(estatisticas):
    """Gera um jogo com maior probabilidade de acerto."""
    if len(estatisticas) < 15:
        print("Estatísticas insuficientes para gerar um jogo confiável.")
        return []
    
    # Pegamos as 10 dezenas mais frequentes
    top_10 = [num for num, _ in estatisticas[:10]]

    # Escolhemos 5 aleatórias entre as restantes
    restantes = [num for num, _ in estatisticas[10:]]
    top_5 = random.sample(restantes, 5) if len(restantes) >= 5 else restantes

    # Retorna o jogo ordenado
    return sorted(top_10 + top_5)

def salvar_jogo(jogo, ultimos_jogos):
    """Salva o jogo gerado e os últimos 10 concursos em um arquivo de texto."""
    if not jogo:
        print("Nenhum jogo foi gerado para salvar.")
        return

    data_atual = datetime.datetime.now().strftime("%d.%m.%Y")
    arquivo = f"jogo_recomendado_{data_atual}.txt"

    try:
        with open(arquivo, "w") as f:
            f.write("Jogo recomendado com maior probabilidade:\n")
            f.write("-" * 40 + "\n")
            f.write(" ".join(f"{num:02d}" for num in jogo) + "\n\n")

            f.write("Últimos 10 jogos sorteados:\n")
            f.write("-" * 40 + "\n")
            for concurso, dezenas in ultimos_jogos[:ULTIMOS_JOGOS_NO_TXT]:
                f.write(f"Concurso {concurso}: " + " ".join(f"{int(num):02d}" for num in dezenas) + "\n")

        print(f"Jogo salvo no arquivo '{arquivo}' com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar jogo no arquivo: {e}")

def main():
    resultados = buscar_resultados(DATABASE_PATH)
    if not resultados:
        print("Nenhum dado encontrado. Verifique o banco de dados.")
        return

    estatisticas = calcular_estatisticas(resultados)
    jogo = gerar_jogo(estatisticas)

    if jogo:
        print("Jogo sugerido:", jogo)
        salvar_jogo(jogo, resultados)
    else:
        print("Não foi possível gerar um jogo.")

if __name__ == "__main__":
    main()
