# Arquivo: analysis_engine.py

import pandas as pd
import numpy as np

def calcular_forcas(df, time_casa, time_fora):
    """
    Calcula a taxa de gols esperada para dois times específicos com base nos dados históricos.
    Args:
        df: DataFrame com dados históricos (colunas: Time_Casa, Time_Fora, Gols_Casa, Gols_Fora, etc.)
        time_casa: Nome do time da casa (string)
        time_fora: Nome do time visitante (string)
    Returns:
        tuple: (taxa_casa, taxa_fora), taxas de gols esperadas como floats
    """
    # Calcula média de gols marcados por time_casa
    jogos_casa_time1 = df[df['Time_Casa'] == time_casa]
    jogos_fora_time1 = df[df['Time_Fora'] == time_casa]
    gols_marcados_casa = jogos_casa_time1['Gols_Casa'].mean() if not jogos_casa_time1.empty else 0
    gols_marcados_fora = jogos_fora_time1['Gols_Fora'].mean() if not jogos_fora_time1.empty else 0
    taxa_casa = (gols_marcados_casa + gols_marcados_fora) / 2 or 1  # Média de gols marcados

    # Calcula média de gols marcados por time_fora
    jogos_casa_time2 = df[df['Time_Casa'] == time_fora]
    jogos_fora_time2 = df[df['Time_Fora'] == time_fora]
    gols_marcados_casa = jogos_casa_time2['Gols_Casa'].mean() if not jogos_casa_time2.empty else 0
    gols_marcados_fora = jogos_fora_time2['Gols_Fora'].mean() if not jogos_fora_time2.empty else 0
    taxa_fora = (gols_marcados_casa + gols_marcados_fora) / 2 or 1  # Média de gols marcados

    return taxa_casa, taxa_fora

def calcular_probabilidades_placar(time_casa, time_fora, taxas, max_gols=5):
    """
    Calcula probabilidades de placares usando um modelo Poisson.
    Args:
        time_casa: Nome do time da casa
        time_fora: Nome do time visitante
        taxas: Tuple (taxa_casa, taxa_fora) com taxas de gols esperadas
        max_gols: Máximo de gols a considerar
    Returns:
        pandas.DataFrame: DataFrame com colunas 'Placar' e 'Probabilidade'
    """
    from scipy.stats import poisson
    
    lambda_casa, lambda_fora = taxas  # Unpack the tuple
    
    placares = []
    probabilidades = []
    
    for gols_casa in range(max_gols + 1):
        for gols_fora in range(max_gols + 1):
            prob = poisson.pmf(gols_casa, lambda_casa) * poisson.pmf(gols_fora, lambda_fora)
            placares.append(f"{gols_casa}-{gols_fora}")
            probabilidades.append(prob)
    
    return pd.DataFrame({
        'Placar': placares,
        'Probabilidade': probabilidades
    })

def extrair_prob_finais(probs_placar):
    """
    Extrai probabilidades de vitória, empate e derrota a partir das probabilidades de placar.
    Args:
        probs_placar: DataFrame com colunas 'Placar' e 'Probabilidade'
    Returns:
        dict: Probabilidades de vitória, empate e derrota
    """
    prob_casa = 0
    prob_empate = 0
    prob_fora = 0
    
    for _, row in probs_placar.iterrows():
        gols_casa, gols_fora = map(int, row['Placar'].split('-'))
        prob = row['Probabilidade']
        if gols_casa > gols_fora:
            prob_casa += prob
        elif gols_casa == gols_fora:
            prob_empate += prob
        else:
            prob_fora += prob
    
    return {
        'Vitoria_Casa': prob_casa,
        'Empate': prob_empate,
        'Vitoria_Fora': prob_fora
    }