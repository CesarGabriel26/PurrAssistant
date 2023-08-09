import json

def WriteData(Key,Value,caminho_arquivo):
    dados = ReadData(caminho_arquivo)
    dados[Key] = Value

    # Escrevendo os dados no arquivo JSON
    try:
        with open(caminho_arquivo, "w") as arquivo:
            json.dump(dados, arquivo)
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")

def ReadData(caminho_arquivo):
    # Lendo o arquivo JSON
    try:
        with open(caminho_arquivo, 'r') as f:
            dados = json.load(f)
        return dados
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")
    