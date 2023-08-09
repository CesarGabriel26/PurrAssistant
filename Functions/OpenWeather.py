import datetime as dt
import requests


APY_KEY = "KEY"

#Andradina #{'Lat': -20.896505, 'Lon': -51.3742765}

def Return_Cliamte_Data():
    BASE_URL_weather = "http://api.openweathermap.org/data/2.5/weather?"
    pass

def Return_air_pollution_Data(Data_Lat_Lon):
    lat = Data_Lat_Lon["Lat"]
    lon = Data_Lat_Lon["Lon"]

    AirQualityIndex = {
        1: "Boa",
        2: "Justa acima de Moderada porem abaixo de Boa",
        3: "Moderada",
        4: "Ruim",
        5: "Muito ruim",
    }

    BASE_URL_air_pollution = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={APY_KEY}"

    resposta = requests.get(BASE_URL_air_pollution).json()

    aqi = resposta["list"][0]["main"]["aqi"]

    Componentes = resposta["list"][0]["components"]

    co = f"a {Componentes['co']:.3f} microgramas por metro cúbico"
    no = f"a {Componentes['no']:.3f} microgramas por metro cúbico"
    no2 = f"a {Componentes['no2']:.3f} microgramas por metro cúbico"
    o3 = f"a {Componentes['o3']:.3f} microgramas por metro cúbico"
    so2 = f"a {Componentes['so2']:.3f} microgramas por metro cúbico"
    pm2_5 = f"a {Componentes['pm2_5']:.3f} microgramas por metro cúbico"
    pm10 = f"a {Componentes['pm10']:.3f} microgramas por metro cúbico"
    nh3 = f"a {Componentes['nh3']:.3f} microgramas por metro cúbico"

    textoelementos = f"""
        Monóxido de carbono {co} /$
        monóxido de nitrogênio {no} /$
        Dióxido de nitrogênio {no2} /$
        Ozônio {o3} /$
        Dióxido de enxofre {so2} /$
        Partículas matéria finas {pm2_5} /$
        Partículas matéria grossa {pm10} /$
        Amônia {nh3}
    """

    texto = f"A qualidade do ar esta {AirQualityIndex[aqi]}, com uma concentração de \n {textoelementos}"

    return texto


def Return_Geocoding_Data(Cidade):
    BASE_URL_Geocoding = f"http://api.openweathermap.org/geo/1.0/direct?q={Cidade}&limit=5&appid={APY_KEY}"
    resposta = requests.get(BASE_URL_Geocoding).json()
    #print(resposta)

    Data = {
        "Lat": resposta[0]['lat'],
        "Lon": resposta[0]['lon']
    }

    return Data

