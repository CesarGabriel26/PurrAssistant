#import OpenWeather as openWeather

import json

def ExecuteComands(code_string: str):
    val = eval(code_string)
    return val

caminho_arquivo_Data = "data.json"

def ChangeData(Key, Value, caminho_arquivo):
    dados = ReadData(caminho_arquivo)
    dados[Key] = Value

    # Escrevendo os dados no arquivo JSON
    with open(caminho_arquivo, "w") as arquivo:
        json.dump(dados, arquivo)

def ReadData(caminho_arquivo):
    # Lendo o arquivo JSON
    
    with open(caminho_arquivo, 'r') as f:
        dados = json.load(f)
    return dados


def Sleep():
    ChangeData("Rosto", "Dormir", caminho_arquivo_Data)
    return "ok /$ até mais tarde"

#def Return_air:
#	value = openWeather.Return_air_pollution_Data({'Lat': -20.896505, 'Lon': -51.3742765})
#	return value