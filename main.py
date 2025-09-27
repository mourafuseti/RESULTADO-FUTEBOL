# Arquivo: main.py

from data_collector import carregar_dados_historicos
from analysis_engine import calcular_forcas, calcular_probabilidades_placar, extrair_prob_finais
import pandas as pd

# Definir times para análise
TIME_CASA = 'Flamengo'
TIME_FORA = 'Palmeiras'

# Definir URL para web scraping (substitua pelo site real)
URL_ALVO = 'https://www.flashscore.com.br/futebol/brasil/serie-a/resultados/'  # Exemplo; substitua pelo URL correto

# Carregar dados históricos
df_historico = carregar_dados_historicos(URL_ALVO)

# Verificar se os times existem nos dados
times_disponiveis = pd.concat([df_historico['Time_Casa'], df_historico['Time_Fora']]).unique()
if TIME_CASA not in times_disponiveis or TIME_FORA not in times_disponiveis:
    raise ValueError(f"Um ou ambos os times ({TIME_CASA}, {TIME_FORA}) não estão nos dados históricos.")

# Calcular taxas de gols esperadas
taxa_a, taxa_b = calcular_forcas(df_historico, TIME_CASA, TIME_FORA)
print(f"Taxa de Gols Esperada para o {TIME_CASA}: {taxa_a:.3f} gols")
print(f"Taxa de Gols Esperada para o {TIME_FORA}: {taxa_b:.3f} gols")

# Calcular probabilidades de placares
df_probabilidades = calcular_probabilidades_placar(TIME_CASA, TIME_FORA, (taxa_a, taxa_b), max_gols=4)
print("\nProbabilidades de Placares:")
print(df_probabilidades)

# Extrair probabilidades finais (vitória, empate, derrota)
resultados_finais = extrair_prob_finais(df_probabilidades)
print("\nProbabilidades Finais:")
print(f"Vitória {TIME_CASA}: {resultados_finais['Vitoria_Casa']:.3f}")
print(f"Empate: {resultados_finais['Empate']:.3f}")
print(f"Vitória {TIME_FORA}: {resultados_finais['Vitoria_Fora']:.3f}")