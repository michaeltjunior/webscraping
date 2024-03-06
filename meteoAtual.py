from bs4 import BeautifulSoup
import requests
import json

headers = {'Accept': 'text/plain'}
dados = {'wx': []}

cidade = 'Criciúma'
estado = 'SC'
estacao = 'Verão'

def celsius(fahrenheit):
    tempF = fahrenheit.replace('F','')
    tempCelsius = (float(tempF.replace('°','')) - 32) * 5/9
    return round(tempCelsius, 2)

def hPa(mmhg):
    press = float(mmhg) / 0.02953
    return round(press, 1)

page = requests.get("https://www.wunderground.com/weather/br/crici%C3%BAma")
#soup = BeautifulSoup(page.content, "html.parser")
soup = BeautifulSoup(page.content, "lxml")

dados = soup.find(title='Additional Conditions')
dados2 = dados.find(class_=['test-true', 'wu-unit-temperature', 'is-degree-visible', 'ng-star-inserted'])
dados3 = dados2.find_all(class_='wu-value-to')

condicao = soup.find(class_='conditions-extra')
condicao2 = condicao.find(class_='condition-icon')

temperatura = soup.find(class_='current-temp')
temp2 = temperatura.find_all('span', class_=['wu-unit-temperature','wu-value-to'])

sensacao = soup.find(class_='feels-like')
sensacao2 = sensacao.find_all(class_='temp')

vento = soup.find(class_='wind-compass-wrap')
dirVento = vento.find(class_='wind-compass')
velVento = vento.find(class_='wind-speed')

nuvens = soup.find(class_='wx-value')

# ------------------------------------ RADIAÇÃO ULTRAVIOLETA ---------------------------------------

page2 = requests.get("https://www.wunderground.com/health/br/crici%C3%BAma?cm_ven=localwx_moduv")
soup2 = BeautifulSoup(page2.content, "html.parser")

dadosUV = soup2.find(class_='uv-index')
dadosUV2 = dadosUV.find(class_=['status', 'label-xlarge', 'ng-star-inserted'])
dadosUV3 = dadosUV.find(class_=['uvIndex-label'])

#print(dadosUV2.get_text())      # UV status

# ------------------------------------ PRECIPITAÇÃO ACUMULADA ---------------------------------------

page3 = requests.get("https://www.wunderground.com/precipitation/br/crici%C3%BAma?cm_ven=localwx_modprecip")
soup3 = BeautifulSoup(page3.content, "html.parser")

dadosChuva = soup3.find(class_=['liquid-immediate'])
dadosChuva2 = dadosChuva.find(class_=['precip-amount-value'])
# --------------------------------------------- VALORES ----------------------------------------------

temperatura = float(celsius(temp2[0].get_text()))
sensacao = float(celsius(sensacao2[0].get_text()))
pressao = float(hPa(dados3[0].get_text()))
visibilidade = float(dados3[1].get_text())
orvalho = float(celsius(dados3[2].get_text()))
umidade = float(dados3[3].get_text())
cobertura = nuvens.get_text()
UV = dadosUV3.get_text()
descUV = dadosUV2.get_text()
precipitacao = float(dadosChuva2.get_text().replace("in", ""))
direcaoVento = str(dirVento)[str(dirVento).find('rotate')+7:str(dirVento).find('deg')]
velocidadeVento = velVento.get_text()
descCondicao = condicao2.get_text()

"""

#PARA TESTES SOMENTE
temperatura = 40
sensacao = 50
pressao = 1001
visibilidade = 10
orvalho = 15
umidade = 50
cobertura = 'Cloudy'
UV = 10
precipitacao = 0
descUV = 'Very high'

print(cidade)
print(estado)
print(estacao)
print(temperatura)
print(sensacao)
print(pressao) 
print(visibilidade)
print(orvalho)
print(umidade)
print(cobertura)
print(UV)
print(precipitacao)

print('Temperatura : ' + str(temperatura))             # temperatura
print('Sensação térmica : '+ str(sensacao))     # sensacao termica

print('Pressão : ' + str(pressao))                    # pressao
print('Visibilidade : ' + str(visibilidade) + ' Nm')            # visibilidade (nm)
print('Ponto de orvalho : ' + str(orvalho))       # ponto de orvalho
print('Umidade relativa : ' + str(umidade) + '%')         # humidade (%)
print('Cobertura : ' + cobertura)                               # cobertura de nuvens

print('Radiação UV : ' + UV + ' ('+descUV+')')      # UV index
print('Precipitação acumulada : ' + str(precipitacao) + ' mm')   # precipitação acumulada

print('Dir. Vento : ' + str(direcaoVento) + ' °')   # velocidade do vento (em nós)
print('Vel. Vento : ' + str(velocidadeVento) + ' kt')   # velocidade do vento (em nós)

print('Condição : ' + descCondicao)   
"""
# ----------------------------------------- ENVIO PARA API -------------------------------------------
dados['wx'] = {'cidade': cidade, 'estado': estado, 'estacao': estacao, 'temperatura': temperatura, 'sensacao': sensacao, 'orvalho': orvalho, 'umidade': umidade, 'pressao': pressao, 'uv': UV, 'visibilidade': visibilidade, 'cobertura': descCondicao, 'precipitacao': precipitacao, 'direcaovento': direcaoVento, 'velocidadevento': velocidadeVento}

r = requests.post('https://intelliseven.com.br/meteo/currentwx/add',  json=dados['wx'], headers=headers)

print(r.text)
