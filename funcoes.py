import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



def recuperar_dados():
    """
    Função para recuperar os dados dos jogos de futebol da ESPN.
    Variáveis com xPath (caso haja remontagem do siste): time_casa, time_fora
    """
    try:
        driver = webdriver.Chrome()

        campeonatos_desejados = ['Campeonato Brasileiro', 'Brazilian Serie B', 'Campeonato Inglês', 'Spanish LALIGA', 'Campeonato Francês', 'Campeonato Italiano', 'Campeonato Português', 'Campeonato Chinês', 'CONMEBOL Libertadores', 'CONMEBOL Sudamericana', 'Bundesliga - Campeonato Alemão', 'UEFA Champions League', 'UEFA Europa League', 'UEFA Conference League']

        data_desejada = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

        driver.get(f"https://www.espn.com.br/futebol/calendario/_/data/{data_desejada}")
        
        time.sleep(5)

        data_jogos = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        data_jogos_string = str(data_jogos)

        html = driver.page_source
    
        soup = BeautifulSoup(html, 'html.parser')
        
        campeonatos_importantes = soup.find_all('div', class_='ResponsiveTable')

        print(campeonatos_importantes)

        dados_jogo = []  

        for campeonato in campeonatos_importantes:
            campeonato_title = campeonato.find('div', class_='Table__Title').text
            if campeonato_title in campeonatos_desejados:
                # Encontra todos os jogos usando BeautifulSoup
                jogos = campeonato.find_all('tbody', class_='Table__TBODY')

                links_unicos = set()

                for jogo in jogos:
                    links = jogo.find_all('a', class_='AnchorLink')
                    for link in links:
                        href = link.get('href')
                        if "jogoId" in href:
                            id_jogos = href.split("/")[5]
                            links_estatisticas = f"https://www.espn.com.br/futebol/partida-estatisticas/_/jogoId/{id_jogos}"
                            links_unicos.add(links_estatisticas)

                for link in links_unicos:
                    try:
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.get(link)

                        placar_lista = []

                        time_casa = driver.find_element(By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2').text
                        time_fora = driver.find_element(By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2').text

                        time.sleep(5)

                        soup_estatisticas = BeautifulSoup(driver.page_source, 'html.parser')
                        
                        campeonato = soup_estatisticas.find('div', class_='ScoreCell__NotesWrapper w-100').text
                        estadio = soup_estatisticas.find('div', class_='GameInfo__Location').text
                        posse_bola_casa = soup_estatisticas.select_one('span.bLeWt.ZfQkn.JoGSb.VZTD.pgHdv.uHRs').text
                        posse_bola_fora = soup_estatisticas.select_one('span.bLeWt.ZfQkn.JoGSb.VZTD.nljvg').text
                        placar = soup_estatisticas.find_all('div', class_='Gamestrip__Score relative tc w-100 fw-heavy-900 h2 clr-gray-01')
                        for item in placar:
                            placar_numeros = ''.join(filter(str.isnumeric, item.text))
                            placar_lista.append(placar_numeros)

                        div_principal = soup_estatisticas.find('div', class_='eZKkr aoVnJ Shbrf')

                        if div_principal:
                            divs_estatisticas = div_principal.find_all('div', class_='LOSQp Kiog LVdfu lEHQF Pxeau lGIsP nbAEp aRBRX trLLY')

                            chutes_no_gol_casa = chutes_no_gol_fora = chutes_casa = chutes_fora = ""
                            faltas_casa = faltas_fora = cartoes_amarelos_casa = cartoes_amarelos_fora = ""
                            cartoes_vermelhos_casa = cartoes_vermelhos_fora = escanteios_casa = escanteios_fora = ""
                            defesas_casa = defesas_fora = ""

                            for div in divs_estatisticas:
                                if "Chutes no gol" in div.text:
                                    chutes_no_gol_casa = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp vIfRz ANdqi').text
                                    chutes_no_gol_fora = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp SolpO VyZCd').text

                                if "Chutes" in div.text and "Chutes no gol" not in div.text:
                                    chutes_casa = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp vIfRz ANdqi').text
                                    chutes_fora = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp SolpO VyZCd').text
                                    
                                if "faltas" in div.text:
                                    faltas_casa = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp vIfRz ANdqi').text
                                    faltas_fora = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp SolpO VyZCd').text

                                if "Cartões amarelos" in div.text:
                                    cartoes_amarelos_casa = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp vIfRz ANdqi').text
                                    cartoes_amarelos_fora = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp SolpO VyZCd').text
                                
                                if "Cartões Vermelhos" in div.text:
                                    cartoes_vermelhos_casa = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp vIfRz ANdqi').text
                                    cartoes_vermelhos_fora = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp SolpO VyZCd').text
                                
                                if "Escanteios" in div.text:
                                    escanteios_casa = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp vIfRz ANdqi').text
                                    escanteios_fora = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp SolpO VyZCd').text
                                
                                if "defesas" in div.text:
                                    defesas_casa = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp vIfRz ANdqi').text
                                    defesas_fora = div.find('div', class_='UGvDX ubOdK WtEci FfVOu seFhp SolpO VyZCd').text

                            dados_jogo.append({
                                'TIME CASA': time_casa,
                                'TIME FORA': time_fora,
                                'GOLS CASA': placar_lista[0],
                                'GOLS FORA': placar_lista[1],
                                'CHUTES GOL CASA': chutes_no_gol_casa,
                                'CHUTES GOL FORA': chutes_no_gol_fora,
                                'FINALIZAÇÕES CASA': chutes_casa,
                                'FINALIZAÇÕES FORA': chutes_fora,
                                'CARTÃO AMARELO CASA': cartoes_amarelos_casa,
                                'CARTÃO AMARELO FORA': cartoes_amarelos_fora,
                                'ESCANTEIOS CASA': escanteios_casa,
                                'ESCANTEIOS FORA': escanteios_fora,
                                'FALTAS CASA': faltas_casa,
                                'FALTAS FORA': faltas_fora,
                                'POSSE BOLA CASA': posse_bola_casa,
                                'POSSE BOLA FORA': posse_bola_fora,
                                'ESTADIO': estadio,
                                'CAMPEONATO': campeonato,
                                'DATA' : str(data_jogos)
                            })

                        else:
                            print("A div principal especificada não foi encontrada.")

                    except Exception as e:
                        print("Erro ao coletar dados dos times:", e)
                    finally:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
            
            else:
                print(f"O campeonato {campeonato_title} não está na lista de campeonatos desejados.")

    except Exception as e:
        print("Erro durante a execução:", e)

    finally:
        driver.quit()

    return dados_jogo

# Recupera os dados
dados = recuperar_dados()

# Converte os dados em um DataFrame do pandas
df_novos_dados = pd.DataFrame(dados)

# Caminho do arquivo Excel
caminho_arquivo = 'dados.xlsx'

try:
    df_existente = pd.read_excel(caminho_arquivo)
except FileNotFoundError:
    df_existente = pd.DataFrame()

df_atualizado = pd.concat([df_existente, df_novos_dados], ignore_index=True)

df_atualizado.to_excel(caminho_arquivo, index=False)

print(df_atualizado)