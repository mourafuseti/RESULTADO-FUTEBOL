# Previsão de Resultados de Partidas de Futebol

Este projeto é uma ferramenta baseada em Python para prever resultados de partidas de futebol usando dados históricos de jogos. Ele realiza web scraping de resultados de partidas de um site especificado, calcula os gols esperados para os times e prevê as probabilidades de placares usando um modelo Poisson. O projeto foi testado no Kali Linux e utiliza um ambiente virtual para gerenciar dependências.

## Estrutura do Projeto

- **`main.py`**: Script principal que orquestra o carregamento de dados, análise e saída de previsões.
- **`data_collector.py`**: Gerencia o web scraping de resultados de partidas e fornece dados simulados como fallback.
- **`analysis_engine.py`**: Contém funções para calcular forças dos times e prever resultados de partidas.
- **`futebol_venv/`**: Diretório do ambiente virtual (criado durante a configuração).

## Pré-requisitos

- **Python 3.8+**: Certifique-se de que o Python 3 está instalado no seu sistema.
- **Kali Linux**: O projeto foi testado no Kali Linux, mas deve funcionar em outras distribuições Linux ou sistemas operacionais.
- **Conexão com a Internet**: Necessária para realizar web scraping de dados reais de partidas.
- **Site Alvo**: Um URL válido para resultados de partidas de futebol (ex.: Flashscore, SofaScore). Verifique os termos de serviço e o `robots.txt` do site antes de realizar o scraping.

## Instalação

1. **Navegue até o diretório do projeto**:
   ```bash
   cd /home/kali/Área\ de\ trabalho/futebol
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python3 -m venv futebol_venv
   source futebol_venv/bin/activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install pandas requests beautifulsoup4 scipy
   ```

4. **Verifique os arquivos**:
   Certifique-se de que os seguintes arquivos estão presentes:
   ```
   main.py
   data_collector.py
   analysis_engine.py
   ```

## Configuração

- **URL para Web Scraping**:
  Edite o `main.py` para especificar o URL dos dados de partidas. Por exemplo:
  ```python
  URL_ALVO = 'https://www.flashscore.com.br/futebol/brasil/serie-a/resultados/'
  ```
  Atualize o `data_collector.py` com os seletores HTML corretos para o site alvo. Inspecione o HTML do site (ex.: usando as ferramentas de desenvolvedor do navegador) para encontrar as tags e classes apropriadas para os containers de partidas, nomes dos times e placares.

- **Nomes dos Times**:
  Defina `TIME_CASA` e `TIME_FORA` no `main.py` com os times que deseja analisar (ex.: `'Flamengo'`, `'Palmeiras'`). Certifique-se de que esses nomes correspondem aos dados raspados ou simulados.

## Uso

1. **Ative o ambiente virtual**:
   ```bash
   source futebol_venv/bin/activate
   ```

2. **Execute o script principal**:
   ```bash
   python3 main.py
   ```

3. **Saída esperada**:
   O script irá:
   - Tentar raspar dados de partidas do URL especificado.
   - Usar dados simulados se o URL for inválido ou o scraping falhar.
   - Calcular os gols esperados para os times especificados.
   - Exibir uma tabela de probabilidades de placares e probabilidades finais (vitória, empate, derrota).

   Exemplo de saída:
   ```
   -> Tentando acessar: https://www.flashscore.com.br/futebol/brasil/serie-a/resultados/
   -> Sucesso! 20 jogos raspados.
   Taxa de Gols Esperada para o Flamengo: 1.500 gols
   Taxa de Gols Esperada para o Palmeiras: 1.250 gols
   Probabilidades de Placares:
        Placar  Probabilidade
   0     0-0       0.082...
   ...
   Probabilidades Finais:
   Vitória Flamengo: 0.450
   Empate: 0.270
   Vitória Palmeiras: 0.280
   ```

4. **Desative o ambiente virtual**:
   ```bash
   deactivate
   ```

## Solução de Problemas

- **Dados Simulados Usados**:
  Se você vir a mensagem `-> Nenhuma URL fornecida. Carregando dados SIMULADOS.` ou um erro de scraping, verifique:
  - O `URL_ALVO` no `main.py` está correto.
  - Os seletores HTML no `data_collector.py` correspondem à estrutura do site alvo.
  - Sua conexão com a internet (execute `ping google.com`).
  - Configurações de proxy, se estiver em uma rede restrita:
    ```python
    proxies = {'http': 'http://seu_proxy:porta', 'https': 'https://seu_proxy:porta'}
    response = requests.get(url, headers=headers, timeout=10, verify=True, proxies=proxies)
    ```

- **Problemas com Dependências**:
  Verifique os pacotes instalados:
  ```bash
  pip list
  ```
  Confirme que `pandas`, `requests`, `beautifulsoup4` e `scipy` estão listados.

- **Nomes de Times Inválidos**:
  Verifique os times disponíveis nos dados:
  ```python
  print(pd.concat([df_historico['Time_Casa'], df_historico['Time_Fora']]).unique())
  ```

- **Especificidades do Kali Linux**:
  O Kali Linux restringe instalações globais com `pip`. Sempre use um ambiente virtual para evitar erros de `externally-managed-environment`.

## Notas

- **Ética no Web Scraping**: Certifique-se de que o site alvo permite scraping, verificando o `robots.txt` e os termos de serviço. Use limitação de taxa (ex.: `time.sleep(2)`) para evitar sobrecarregar o servidor.
- **Dados Simulados**: Para testes, mantenha `URL_ALVO = None` no `main.py` para usar dados simulados.
- **Personalização**: Para raspar um site específico, atualize a função `fazer_web_scraping_de_resultados` no `data_collector.py` com os seletores HTML corretos.

## Contribuição

Contribuições são bem-vindas! Por favor:
1. Faça um fork do repositório (se hospedado).
2. Crie uma branch para sua funcionalidade.
3. Envie um pull request com a descrição das alterações.

## Licença

Este projeto não possui licença definida. Use-o de forma responsável e respeite os termos de serviço de qualquer site que você raspar.
