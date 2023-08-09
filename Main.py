import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
from datetime import datetime
import threading
import time
import os
import speech_recognition as sr

import Functions.OpenWeather as openWeather
import Functions.Learninh as learninh
import Functions.ComandPacks as cp
import Functions.Read_Write_Json as Json


engine = pyttsx3.init()
# Defina o pitch (tom) da voz (valor entre 0 e 1)
engine.setProperty('pitch', .5)

# Defina o rate (velocidade) da voz (valor padrão é 200)
engine.setProperty('rate', 200)
os.chdir("json")

largura = 375*2
altura = 375*2

voices = engine.getProperty('voices')#getting details of current voice
engine.setProperty('voice', voices[1].id)

AudioMode = False
TreaningMode = False
EstaOuvindo = False

language =  'pt-BR' #"en-US"

caminho_arquivo_AsistantData = "data.json"
caminho_arquivo_ExprecionsData = "Exprecao.json"

def Fala(Texto):

    frases = Texto.split("/$")

    for frase in frases:
        frase_limpa = frase.strip()

        Json.WriteData("Rosto","Falando",caminho_arquivo_AsistantData)
        ler_arquivo_json()

        #print(frase_limpa)
        
        engine.say(frase_limpa)
        engine.runAndWait()

        Json.WriteData("Rosto","Normal",caminho_arquivo_AsistantData)
        ler_arquivo_json()

def ProcessarComandos(comando):
    global TreaningMode
    #resposta = "Olá!/$Tudo bem?/$Eu sou um assistente virtual."

    dat = Json.ReadData(caminho_arquivo_AsistantData)

    if comando == "MTreinar":
        clear_console()
        TreaningMode = True

    if dat['Rosto'] == "Dormir":

        if comando == "Kiri" or comando == "Kit":
            Json.WriteData("Rosto","Normal",caminho_arquivo_AsistantData)
            resposta = 'Como posso ajudar?'
            return


    else:
        if comando == "Diga":
            textoArepitir = input("Oque devo dizer:>")
            resposta = textoArepitir
        
        elif comando == "Qualidade do ar":
            resposta = openWeather.Return_air_pollution_Data({'Lat': -20.896505, 'Lon': -51.3742765})

        else:   
            try:
                knowledge_base: dict = learninh.load_knowledge_base('Knowledge.json')

                best_match  = learninh.find_best_match(comando, [
                    q['Questao'] for q in knowledge_base["Questoes"]
                ])
                
                if best_match:
                    resp: str = learninh.get_answer(best_match,knowledge_base)
                    comandoextra = ""
                    if "/$/" in resp:
                        try:
                            comandoextra = resp.replace("/$/", "")
                            resp = cp.ExecuteComands(comandoextra)
                        except Exception as e:
                            print(e)

                        ##print(resp)
                    resposta = resp

                    if comandoextra == " Sleep()":
                        Json.WriteData("Rosto", "Dormir", caminho_arquivo_AsistantData)

                    ##print(comandoextra)
            except Exception as e:
                print(e)

    # Chamar a função de leitura do texto em uma thread separada
    Fala("")
    thread_leitura_texto = threading.Thread(target=Fala, args=(resposta,))
    thread_leitura_texto.daemon = True
    thread_leitura_texto.start()

def ouvir_comandos():
    reconhecedor = sr.Recognizer()

    with sr.Microphone() as source:
        #print('Estou ouvindo')
        audio = reconhecedor.listen(source)
    try:
        comando = reconhecedor.recognize_google(audio, language=language)
        ProcessarComandos(comando)

    except sr.UnknownValueError:
        print("Não entendi o áudio.")
    except sr.RequestError as e:
        print("Erro na solicitação ao serviço de reconhecimento de fala; {0}".format(e))

def ler_comandos(texto):
    ##print(texto)
    comando = input_usuario.get()

    os.system('cls')

    ##print(comando)

    input_usuario.delete(0, tk.END)

    if comando != "":
        ProcessarComandos(comando)

def TreaningBot():
    knowledge_base: dict = learninh.load_knowledge_base('Knowledge.json')
    global TreaningMode

    while True:
        user: str = input('Voce: ')

        if user.lower() == 'exitmt':
            clear_console()
            TreaningMode = False
            break

        best_match  = learninh.find_best_match(user, [
            q['Questao'] for q in knowledge_base["Questoes"]
        ])

        if best_match:
            answer: str = learninh.get_answer(best_match,knowledge_base)
            Fala(answer)
        else:
            Fala('não sei a resposta para isso poderia me ensinar?')
            novaResposta: str = input('Resposta (skip para pular): ')

            if novaResposta == "exitMT":
                clear_console()
                TreaningMode = False
                break

            novaRespostaArray = novaResposta.split(" // ")
            #print(novaRespostaArray)
            if novaResposta != "skip":
                knowledge_base['Questoes'].append({
                    'Questao': user,
                    'resposta': novaRespostaArray
                })
                learninh.save_knowledge_base('Knowledge.json',knowledge_base)
                Fala('Obrigado, agora aprendi algo novo')
            else:
                Fala('ok, posso aprender mais tarde')

"""
while True: 
    try:
        if TreaningMode:
            TreaningBot()
        else:
            if AudioMode:
                ouvir_comandos()
            else:
                ler_comandos()
    except Exception as e:
        #print(e)
        Fala(e)"""

def ler_arquivo_json():
    AssistantData = Json.ReadData(caminho_arquivo_AsistantData)
    ExprecionsData = Json.ReadData(caminho_arquivo_ExprecionsData)

    ##print(AssistantData)
    ##print(ExprecionsData)
    Exprecao = ExprecionsData[AssistantData['Rosto']]

    atualizar_imagem(Exprecao,f"#{AssistantData['Cor']}")


# definições e criação da janela principal do bot

def combinar_imagens(imagens):
    imagens_combinadas = Image.new('RGBA', (largura, altura), (0, 0, 0, 0))
    for img in imagens:
        imagem = Image.open(img[0]).convert("RGBA")
        imagem = imagem.resize((largura, altura))  # Redimensiona a imagem

        if img[2]:
            imagem = imagem.transpose(Image.FLIP_LEFT_RIGHT)  # Flip horizontal

        imagens_combinadas.paste(imagem, (0, 0), imagem)

    return imagens_combinadas

def aplicar_cor_com_multiply(imagem, cor_hex):
    r_cor = int(cor_hex[1:3], 16)
    g_cor = int(cor_hex[3:5], 16)
    b_cor = int(cor_hex[5:7], 16)

    # Aplica o efeito "multiply" da cor sobre a imagem original
    pixels = imagem.load()
    for y in range(imagem.size[1]):
        for x in range(imagem.size[0]):
            r, g, b, a = pixels[x, y]
            r = (r * r_cor) // 255
            g = (g * g_cor) // 255
            b = (b * b_cor) // 255
            pixels[x, y] = (r, g, b, a)

    return imagem

def atualizar_imagem(Exprecao, color):
    caminhos_imagens = [
        #["Caminho da imagem","PodeAplicar cor,PodeSerFlipado"]
        [f"../face parts and templates/Partes/Bigodes/{Exprecao['Bigode']}.png",True,False],
        [f"../face parts and templates/Partes/Narizes/{Exprecao['Nariz']}.png",True,False],
        [f"../face parts and templates/Partes/Bocas/{Exprecao['Boca']}.png",True,False],

        [f"../face parts and templates/Partes/Olhos/{Exprecao['Olhos'][0]}.png",True,False],
        [f"../face parts and templates/Partes/Olhos/{Exprecao['Olhos'][1]}.png",True,True],

        [f"../face parts and templates/Partes/Pupilas/{Exprecao['Pupilas'][0]}.png",False,False],
        [f"../face parts and templates/Partes/Pupilas/{Exprecao['Pupilas'][1]}.png",False,True],

        [f"../face parts and templates/Partes/Sombrancelhas/{Exprecao['Sombrancelhas'][0]}.png",True,False],
        [f"../face parts and templates/Partes/Sombrancelhas/{Exprecao['Sombrancelhas'][1]}.png",True,True],
    ]

    # Combina as imagens 
    imagem_combinada = combinar_imagens(caminhos_imagens)

    # Aplica uma cor por cima da imagem
    imagem_com_cor = aplicar_cor_com_multiply(imagem_combinada, color)

    # Converte a imagem combinada para o formato PhotoImage
    photo = ImageTk.PhotoImage(imagem_com_cor)

    # Atualiza a imagem na label
    label_imagem.config(image=photo)
    label_imagem.image = photo

def fechar_janela():
    janela.destroy()

# Criação da janela principal
janela = tk.Tk()
janela.title("Assistente Virtual")
janela.configure(bg="#000000")
janela.attributes('-fullscreen', True)

# Label para exibir a imagem
label_imagem = tk.Label(janela, width=largura, height=altura)
label_imagem.pack(pady=10)
label_imagem.configure(bg="#000000")
label_imagem.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Botão "Fechar" 
botao_fechar = tk.Button(janela, text="Fechar", command=fechar_janela)
botao_fechar.place(relx=1, rely=0, anchor=tk.NE)

# Input de texto para o usuário 
if not AudioMode:
    input_usuario = tk.Entry(janela, justify=tk.CENTER, font=("Arial", 14))
    input_usuario.place(relx=.9, rely=.98, anchor=tk.SE, relwidth=.8, relheight=.05)
    # Placeholder inicial para o input de texto
    input_usuario.bind("<Return>", ler_comandos)


# chamar a leitura do arquivo JSON 
ler_arquivo_json()

# Laço principal da interface 
janela.mainloop()