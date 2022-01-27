import time
import requests
import pandas as pd
import filecmp
import telegram
from telegram import ParseMode, parsemode
from bs4 import BeautifulSoup

def notificacion(message):
    bot = telegram.Bot('YOUR_BOT_ID')
    bot.sendMessage('YOUR_CHAT_ID', text=message, parse_mode="markdown")

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True

    except FileNotFoundError as e:
        return False

    except IOError as e:
        return False

url = 'https://www.minecrafteo.com/categoria/mods-minecraft/page/1'
cont = 0
while(True):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #Mods
    mods = soup.find_all('a', class_='entry-title-link')
    modsConverted = list()

    count = 0
    for i in mods:
        if count < 24:
            modsConverted.append(i.text)
        else: 
            break
        count += 1

    modsList = list()
    versionList = list()
    linkList = list()

    for i in modsConverted:
        modsList.append(i.split(' para Minecraft ')[0])
        versionList.append(i.split(' para Minecraft ')[1])

    aux = list()

    for a in soup.find_all('a', href=True):
        aux.append(a['href'])

    for i in aux:
        if i not in linkList:
            linkList.append(i)

    linkList = linkList[12:36]

    df = pd.DataFrame({'MODS':modsList, 'VERSIONES':versionList, 'ENLACE':linkList})
    df.index += 1

    if checkFileExistance("mods.csv"):
        df.to_csv("aux.csv", sep="\t")

        path = "mods.csv"
        path2 = "aux.csv"

        if filecmp.cmp(path, path2) != True:
            notificacion("Hay un nuevo mod de Minecraft disponible:\n*" + modsList[0] + "* para Minecraft *" + versionList[0] + "*\n\n" + linkList[0])
        
        df.to_csv("mods.csv", sep="\t")
    
    else:
        df.to_csv("mods.csv", sep="\t")
