from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from columnar import columnar
import telebot
import sys
import os


def pause():
    print('\n Parando análises. . . \n')


def crawler(message):
    print('\n Coletando a relação de jogos. . . \n')
    
    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    #chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #chrome_options.add_argument("--headless")
    
    
    
    # Chamando o browser com as opções e maximizando a janela
    
    #caminho = "geckodriver.exe"
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)    
    #browser = webdriver.Chrome(caminho,chrome_options=chrome_options)
    #browser = webdriver.Firefox()
    
    #browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    #browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'})
    #print(browser.execute_script("return navigator.userAgent;"))

    browser.get(r"https://www.bet365.com/#/AVR/B144/")
    browser.maximize_window()
    time.sleep(10)  
    
    browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]').click()  # aceitar cookies
    browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]').click()  # selecionando o esporte Futebol
    time.sleep(7)
    browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/span').click() # selecionando o campeonato
    xpath_horario_jogos = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div'
    
    while True:
        if browser.find_elements_by_xpath(xpath_horario_jogos):
            contagem_jogos = len(browser.find_elements_by_xpath(xpath_horario_jogos)) # lendo o horario das partidas
            break
        else:
            browser.refresh()
            time.sleep(10)
            
    #Percorrendo o horário dos jogos
    try:
        for j in range(2,contagem_jogos+1):
            xpath_horario_jogo = '/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[{}]'.format(j)
            element_horario_jogo = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[{}]'.format(j)) #xpath dinâmico do horário dos jogos
            text_horario_jogo = browser.execute_script("return arguments[0].innerText;", element_horario_jogo) #texto horário dos jogos
            
            #clicando no horario
            browser.find_element_by_xpath(xpath_horario_jogo).click()
            time.sleep(2)
            
            while True:
                if browser.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[{}]'.format(j)):
                    break
                else:
                    browser.refresh()
                    time.sleep(10)
                    try:
                        browser.find_element_by_xpath(xpath_horario_jogo).click()
                    except:
                        browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[7]').click()
            
            
            time.sleep(3)
            
            
            #Mapeando os times e ODDs
            time1 = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[1]/span[1]')
            odd1 = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[1]/span[2]')
            text_odd1 = browser.execute_script("return arguments[0].innerText;", odd1)
            text_time1 = browser.execute_script("return arguments[0].innerText;", time1)
            
            empate = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[2]/span[1]')
            odd_empate = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[2]/span[2]')
            text_odd_empate = browser.execute_script("return arguments[0].innerText;", odd_empate)
            text_empate = browser.execute_script("return arguments[0].innerText;", empate)
            
            time2 = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[3]/span[1]')
            odd2 = browser.find_element_by_xpath('html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[3]/span[2]')    
            text_odd2 =  browser.execute_script("return arguments[0].innerText;", odd2)   
            text_time2 = browser.execute_script("return arguments[0].innerText;", time2)
            
            if browser.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]'):
                t = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]')
                tempo = browser.execute_script("return arguments[0].innerText;", t)
            if tempo == "":
                tempo = '00:00'
                
            telegram(text_horario_jogo, text_time1, text_odd1, text_empate, text_odd_empate, text_time2, text_odd2, tempo)
            
        # Buscando novo evento
        novo_evento(browser, message, text_horario_jogo)
    except:
        novo_evento(browser, message, text_horario_jogo)



def novo_evento(browser, message, text_horario_jogo):
      
    while True:
        try:
            xpath_horario_jogo = ('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[8]')
            element_horario_jogo = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[8]') #xpath dinâmico do horário dos jogos
            proximo_text_horario_jogo = browser.execute_script("return arguments[0].innerText;", element_horario_jogo)
            
            if browser.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[8]') and proximo_text_horario_jogo > text_horario_jogo:
                #clicando no horario
                browser.find_element_by_xpath(xpath_horario_jogo).click()
                time.sleep(2)
                
                while True:
                    if browser.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[8]'):
                        break
                    else:
                        browser.refresh()
                        time.sleep(10)
                        try:
                            browser.find_element_by_xpath(xpath_horario_jogo).click()
                        except:
                            browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div[7]').click()
        
                time.sleep(3)
            else:
                continue
            
            
            #Mapeando os times e ODDs
            time1 = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[1]/span[1]')
            odd1 = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[1]/span[2]')
            text_odd1 = browser.execute_script("return arguments[0].innerText;", odd1)
            text_time1 = browser.execute_script("return arguments[0].innerText;", time1)
            
            empate = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[2]/span[1]')
            odd_empate = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[2]/span[2]')
            text_odd_empate = browser.execute_script("return arguments[0].innerText;", odd_empate)
            text_empate = browser.execute_script("return arguments[0].innerText;", empate)
            
            time2 = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[3]/span[1]')
            odd2 = browser.find_element_by_xpath('html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div/div/div[3]/span[2]')    
            text_odd2 =  browser.execute_script("return arguments[0].innerText;", odd2)   
            text_time2 = browser.execute_script("return arguments[0].innerText;", time2)
            
            if browser.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]'):
                t = browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/div[1]/div[1]/span[2]')
                tempo = browser.execute_script("return arguments[0].innerText;", t)
            if tempo == "":
                tempo = '00:00'
    
            telegram(proximo_text_horario_jogo, text_time1, text_odd1, text_empate, text_odd_empate, text_time2, text_odd2, tempo)
            text_horario_jogo = proximo_text_horario_jogo 
        
        except:
            time.sleep(60)
            pass
            
        
    

        
def telegram(text_horario_jogo, text_time1, text_odd1, text_empate, text_odd_empate, text_time2, text_odd2, tempo ):
    # Formatando para envio no telegram
    headers = [' 📡 Novo Evento ⚽⏳                               ']

    data = [
        ['⏰ '+ text_horario_jogo],
        ['✅ ' + text_time1 + " " + text_odd1],
        ['⛔ '+ text_empate+ " " + text_odd_empate],
        ['✅ ' + text_time2 + " " + text_odd2],
        ['⏳ '  + 'Encerrará em ' + tempo],
        ['🌐 '   +  "https://www.bet365.com/#/AVR/B146/R%5E1/"],
    ]
    
    table = columnar(data, headers, no_borders=True)
    
    # Enviando mensagem para o Telegram
    bot.send_message(canal,table)
   




######## CONFIGURAÇÕES TELEGRAM ########

CHAVE_API = '5355473408:AAHXPRg7dQ1N-EFtN6QjHA6CG2ZvXHM6bhA'
canal = -1001775325949
bot = telebot.TeleBot(CHAVE_API)

#bot.send_message(canal, "OLÁ")

print('\n\n##### AGUARDANDO COMANDOS ######\n\n')


def restart_program():
    python = sys.executable
    os.execl(python, * sys.argv)
    

def aaa ():
    os.system('python coleta.py')    
    


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '🤖 Robô iniciado 📊✅')
    bot.send_message(canal, '🤖 Robô iniciado 📊✅')
    bot.send_message(canal, '🤖 Capturando Eventos 📡⚽')
    
    crawler(message)
    
    
@bot.message_handler(commands=["pause"])
def pause(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '🤖 Robô parado 📊❌')
    #bot.send_message(canal, '🤖 Robô parado 📊❌')
    restart_program()
    

@bot.message_handler(commands=["restart"])
def restart(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '🤖 Robô reiniciando 📊❌')
    #bot.send_message(canal, '🤖 Robô parado 📊❌')
    aaa()
    
    
    
    
#@bot.message_handler(func=lambda m: True)
#def text(message):
#    bot.reply_to(message, 'ok')

bot.polling()