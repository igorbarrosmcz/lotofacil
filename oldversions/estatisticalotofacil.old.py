# import sqlite3
# from collections import Counter

# # Caminho para o banco de dados criado anteriormente
# DATABASE_PATH = "lotofacil.db"

# def buscar_resultados(banco_de_dados):
#     """Busca os últimos 30 concursos no banco de dados."""
#     try:
#         conn = sqlite3.connect(banco_de_dados)
#         cursor = conn.cursor()

#         # Seleciona as dezenas dos últimos 30 concursos
#         cursor.execute('''
#         SELECT dezenas FROM resultados
#         ORDER BY concurso DESC
#         LIMIT 30
#         ''')
#         resultados = cursor.fetchall()
#         conn.close()

#         # Retorna as dezenas como lista de strings
#         return [resultado[0].split(",") for resultado in resultados]
#     except sqlite3.Error as e:
#         print(f"Erro ao acessar o banco de dados: {e}")
#         return []

# def calcular_estatisticas(dezenas):
#     """Calcula as estatísticas de frequência das dezenas."""
#     # Junta todas as dezenas em uma única lista
#     todas_dezenas = [dezena for sublista in dezenas for dezena in sublista]

#     # Conta a frequência de cada número
#     contagem = Counter(todas_dezenas)

#     # Retorna os números mais frequentes, ordenados pela frequência
#     return contagem.most_common()

# def salvar_estatisticas_em_arquivo(estatisticas, arquivo="estatisticas.txt"):
#     """Salva as estatísticas em um arquivo de texto."""
#     try:
#         with open(arquivo, "w") as f:
#             f.write("Estatísticas de incidência nos últimos 30 concursos:\n")
#             f.write("-" * 40 + "\n")
#             for numero, frequencia in estatisticas:
#                 f.write(f"Número {numero}: apareceu {frequencia} vezes\n")
#         print(f"Estatísticas salvas no arquivo '{arquivo}' com sucesso!")
#     except IOError as e:
#         print(f"Erro ao salvar estatísticas no arquivo: {e}")

# def main():
#     # Passo 1: Buscar resultados do banco de dados
#     dezenas = buscar_resultados(DATABASE_PATH)
#     if not dezenas:
#         print("Nenhum dado encontrado. Verifique o banco de dados.")
#         return

#     # Passo 2: Calcular estatísticas
#     estatisticas = calcular_estatisticas(dezenas)

#     # Passo 3: Salvar estatísticas em arquivo
#     salvar_estatisticas_em_arquivo(estatisticas)

# if __name__ == "__main__":
#     main()

# Código que analisa os resultados, mas também sugere um jogo com maior chance de acerto

import sqlite3
import random
from collections import Counter
import datetime

DATABASE_PATH = "lotofacil.db"

def buscar_resultados(banco_de_dados):
    """Busca os últimos 30 concursos no banco de dados."""
    try:
        conn = sqlite3.connect(banco_de_dados)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT dezenas FROM resultados
        ORDER BY concurso DESC
        LIMIT 30
        ''')
        resultados = cursor.fetchall()
        conn.close()
        return [resultado[0].split(",") for resultado in resultados]
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return []

def calcular_estatisticas(dezenas):
    """Calcula as estatísticas de frequência das dezenas."""
    todas_dezenas = [dezena for sublista in dezenas for dezena in sublista]
    contagem = Counter(todas_dezenas)
    return contagem.most_common()

def gerar_jogo(estatisticas):
    """Gera um jogo otimizado com base nas estatísticas."""
    # Pegamos as 10 dezenas mais frequentes
    top_10 = [num for num, _ in estatisticas[:10]]

    # Pegamos as restantes e escolhemos 5 aleatoriamente
    restantes = [num for num, _ in estatisticas[10:]]
    random.shuffle(restantes)
    top_5 = restantes[:5]

    # Montamos o jogo final
    jogo = sorted(map(int, top_10 + top_5))
    return jogo

def salvar_jogo(jogo):
    """Salva o jogo gerado em um arquivo de texto com a data atual no nome."""
    data_atual = datetime.datetime.now().strftime("%d.%m.%Y")
    arquivo = f"jogo_recomendado_{data_atual}.txt"
    
    try:
        with open(arquivo, "w") as f:
            f.write("Jogo recomendado com maior probabilidade:\n")
            f.write("-" * 40 + "\n")
            f.write(" ".join(f"{num:02d}" for num in jogo) + "\n")
        print(f"Jogo salvo no arquivo '{arquivo}' com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar jogo no arquivo: {e}")
        
def main():
    dezenas = buscar_resultados(DATABASE_PATH)
    if not dezenas:
        print("Nenhum dado encontrado. Verifique o banco de dados.")
        return

    estatisticas = calcular_estatisticas(dezenas)
    jogo = gerar_jogo(estatisticas)

    print("Jogo sugerido:", jogo)
    salvar_jogo(jogo)

if __name__ == "__main__":
    main()
