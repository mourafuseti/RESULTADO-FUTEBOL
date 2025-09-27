# Arquivo: data_collector.py

import pandas as pd
import requests
from bs4 import BeautifulSoup
import io  # Adicionado o módulo io necessário para StringIO

def fazer_web_scraping_de_resultados(url):
    """
    Tenta raspar dados de resultados de jogos de um URL fornecido.
    
    ESTE É UM EXEMPLO DIDÁTICO. Os seletores HTML (.score-time, .home-team, .away-team)
    devem ser ajustados para o site real que você escolher.
    """
    resultados = []
    
    # Simula um cabeçalho de navegador para evitar bloqueios simples
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"-> Tentando acessar: {url}")
    
    try:
        # Configurações para lidar com proxies ou redes restritas no Kali
        response = requests.get(url, headers=headers, timeout=10, verify=True)
        response.raise_for_status()  # Lança erro se o status for 4xx ou 5xx
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- Lógica de EXTRAÇÃO ---
        
        # Iremos simular a busca por um 'container' de jogo na página
        # Você deve identificar no HTML do site real qual é a tag/classe que envolve cada jogo
        containers_jogo = soup.find_all('div', class_='game-container') 
        
        if not containers_jogo:
            print("AVISO: Nenhum container de jogo encontrado. Verifique os seletores HTML ou use dados SIMULADOS.")
            return carregar_dados_simulados()
        
        for container in containers_jogo:
            try:
                # 1. Extrair os Nomes dos Times
                time_casa_elem = container.find('span', class_='home-team')
                time_fora_elem = container.find('span', class_='away-team')
                
                time_casa = time_casa_elem.text.strip() if time_casa_elem else 'N/A'
                time_fora = time_fora_elem.text.strip() if time_fora_elem else 'N/A'
                
                # 2. Extrair o Placar
                placar_elem = container.find('span', class_='score-time')
                
                if placar_elem and '-' in placar_elem.text:
                    placar = placar_elem.text.strip().split('-')
                    try:
                        gols_casa = int(placar[0].strip())
                        gols_fora = int(placar[1].strip())
                    except ValueError:
                        print(f"AVISO: Placar inválido encontrado ({placar_elem.text}). Pulando jogo.")
                        continue
                else:
                    print(f"AVISO: Placar não encontrado ou jogo não finalizado. Pulando jogo.")
                    continue
                
                resultados.append({
                    'Time_Casa': time_casa,
                    'Time_Fora': time_fora,
                    'Gols_Casa': gols_casa,
                    'Gols_Fora': gols_fora,
                    'Campeonato': 'Scraped Data'  # Pode ser adaptado
                })
            except Exception as e:
                print(f"Erro ao processar um jogo: {e}")
                continue
                
        if resultados:
            print(f"-> Sucesso! {len(resultados)} jogos raspados.")
            return pd.DataFrame(resultados)
        else:
            print("-> A raspagem de dados não retornou resultados válidos. Usando dados SIMULADOS.")
            return carregar_dados_simulados()

    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO ou HTTP: Não foi possível acessar o site. {e}")
        print("-> Verifique sua conexão de rede ou configurações de proxy no Kali Linux.")
        print("-> Usando dados SIMULADOS.")
        return carregar_dados_simulados()

def carregar_dados_simulados():
    """Função de backup caso o Web Scraping falhe."""
    dados_csv = """
Time_Casa,Time_Fora,Gols_Casa,Gols_Fora,Campeonato
Flamengo,Palmeiras,2,1,Brasileirao
Sao Paulo,Corinthians,0,0,Brasileirao
Gremio,Internacional,1,1,Brasileirao
Santos,Vasco,3,0,Brasileirao
Flamengo,Sao Paulo,1,2,Brasileirao
Palmeiras,Gremio,3,1,Brasileirao
Corinthians,Santos,0,2,Brasileirao
Internacional,Vasco,2,0,Brasileirao
Sao Paulo,Flamengo,1,1,Brasileirao
Gremio,Palmeiras,0,0,Brasileirao
Vasco,Corinthians,1,0,Brasileirao
Santos,Internacional,2,2,Brasileirao
"""
    return pd.read_csv(io.StringIO(dados_csv))

def carregar_dados_historicos(url_alvo=None):
    """Função principal para o módulo de coleta de dados."""
    if url_alvo:
        return fazer_web_scraping_de_resultados(url_alvo)
    else:
        print("-> Nenhuma URL fornecida. Carregando dados SIMULADOS.")
        return carregar_dados_simulados()
