import requests
import pyttsx3
import speech_recognition as sr
import os
import webbrowser
from datetime import datetime

# Configurar o engine de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Velocidade da fala

# Função para falar
def falar(texto):
    engine.say(texto)
    engine.runAndWait()

# Função para ouvir o comando de voz
def ouvir():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        falar("Erro ao se conectar ao serviço de reconhecimento de voz.")
        return ""

# Função para consultar a API OpenWeatherMap (clima)
openweather_api_key = "fa89c5d2e9cb65ea98ba5b710ceeba8f"

def consultar_clima(cidade):
    cidade = 'Além Paraíba'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={openweather_api_key}&units=metric&lang=pt"
    response = requests.get(url)
    data = response.json()
    
    if data.get("main"):
        temperatura = data["main"]["temp"]
        descricao = data["weather"][0]["description"].lower()
        
        # Informar a temperatura e adicionar um comentário informal baseado na temperatura
        resposta = f"A temperatura em {cidade} é de {temperatura}°C com {descricao}."
        
        # Frases informais baseadas na temperatura
        if temperatura < 15:
            resposta += " Hoje está geladinho, ponha uma coberta!"
        elif 15 <= temperatura <= 25:
            resposta += " Tá uma temperatura agradável, dá pra sair de boa!"
        elif temperatura > 25:
            resposta += " Tá bem quente, seria um dia ótimo para uma praia!"
        
        # Verificar possibilidade de chuva
        if "chuva" in descricao or "garoa" in descricao:
            resposta += " Ah, e parece que pode chover! Melhor levar um guarda-chuva."
        else:
            resposta += " E olha, parece que não vai chover hoje, então pode sair tranquilo!"
        
        return resposta
    else:
        return "Desculpe, não consegui obter informações sobre o clima dessa localização."

# Função para consultar a API News
news_api_key = "636b5d1daca2416ba30995275cd0f149"

def consultar_noticias(tema="brasil"):
    url = f"https://newsapi.org/v2/everything?q={tema}&apiKey={news_api_key}&language=pt"
    response = requests.get(url)
    data = response.json()
    
    if data.get("articles"):
        noticia = data["articles"][0]
        titulo = noticia["title"]
        descricao = noticia["description"]
        return f"Notícia: {titulo}. {descricao}"
    else:
        return "Desculpe, não encontrei notícias sobre esse tema no momento."

# Função para obter a data atual
def obter_data():
    hoje = datetime.now()
    dia = hoje.strftime("%d de %B de %Y")  # Formatar a data
    return f"Hoje é {dia}."

# Função para obter a hora atual
def obter_hora():
    agora = datetime.now()
    hora = agora.strftime("%H:%M")  # Formatar a hora
    return f"A hora atual é {hora}."

# Função para abrir programas no computador
def abrir_programa(nome_programa, pesquisa=None):
    if nome_programa == "navegador":
        if pesquisa:
            url = f"https://www.google.com/search?q={pesquisa.replace(' ', '+')}"
            webbrowser.open(url)
            falar(f"Pesquisando por {pesquisa}.")
        else:
            caminho = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            os.startfile(caminho)
            falar("Abrindo o navegador.")
    else:
        programas = {
            "filmora": "D:/Wondershare Filmora/Wondershare Filmora Launcher.exe",
            "steam": "D:/Steam/steam.exe",
            "drive": "C:/Program Files/Google/Drive File Stream/99.0.0.0/GoogleDriveFS.exe",
            "cs": "D:/CS 1.6/cs.exe",
            "reset impressora": "D:/WicReset/wicreset.exe",
            "word": "C:/Program Files/Microsoft Office/root/Office16/WINWORD.exe",
            "excel": "C:/Program Files/Microsoft Office/root/Office16/EXCEL.exe",
            "corridinha": "D:/Need for Speed Most Wanted Black Edition/speed.exe",
            "cod": "D:/Games/Call of Duty - Black Ops/BlackOps.exe",
            "download": "C:/Users/Kauan Soares/Downloads"
        }
        caminho = programas.get(nome_programa)
        if caminho:
            os.startfile(caminho)
            falar(f"Abrindo {nome_programa}.")
        else:
            falar("Programa não localizado, finalizando automação.")

# Ativação/desativação por voz
def assistente_voz():
    falar("Olá! Sou a ALE. Para me ativar, diga 'Ok ALE'.")
    while True:
        comando = ouvir()

        # Verifica o comando de ativação
        if "ok ali" in comando:
            falar("Estou ouvindo, como posso ajudar?")
            comando = ouvir()

            # Processa o comando
            if "desliga" in comando:
                falar("Encerrando o assistente. Até logo!")
                break
            elif "pesquisar por" in comando:
                pesquisa = comando.replace("pesquisar por", "").strip()
                abrir_programa("navegador", pesquisa)
            elif "abrir" in comando:
                nome_programa = comando.replace("abrir", "").strip()
                abrir_programa(nome_programa)
            elif "clima" in comando:
                cidade = comando.replace("clima", "").strip()
                resposta = consultar_clima(cidade)
                falar(resposta)
            elif "notícias" in comando:
                tema = comando.replace("notícias", "").strip()
                resposta = consultar_noticias(tema)
                falar(resposta)
            elif "que horas são" in comando:
                resposta = obter_hora()
                falar(resposta)
            elif "que dia é hoje" in comando:
                resposta = obter_data()
                falar(resposta)
            else:
                falar("Desculpe, não entendi. Pode repetir?")
            
            # Pausa o assistente após executar o comando
            falar("Finalizado. Diga 'Ok ALE' para reativar.")

# Iniciar o assistente
if __name__ == "__main__":
    assistente_voz()