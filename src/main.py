import json
import os
import requests
import discord
import datetime
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
configFilePath = r'src/config.ini'
config.read(configFilePath)

TOKEN = config.get('TOKEN','BOT_TOKEN')
print(TOKEN)

bot = commands.Bot(command_prefix='!')
client = discord.Client()

TEST_SERVER = config.getint('CHANNEL','TEST_SERVER')
IIIT_SERVER_MAINTAIN = config.getint('CHANNEL','IIIT_SERVER_MAINTAIN')
IIIT_CONTEST_ALERT = config.getint('CHANNEL','IIIT_CONTEST_ALERT')

#String Contest
ATCODER_STR = "Beginner"
CF_DIV = "Div. 1"
CF = "Codeforces"
#URL CONSTANT
ATCODER = "https://atcoder.jp"

#JSON KEYS
UPCOMING = "upcoming"
CONTEST_URL = "url"
CONTEST_NAME = "name"
CONTEST_START_TIME = "startTime"

#API ENDPOINT
API_URL = "http://api.codercalendar.io/"


class Contest(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)



@client.event
async def on_ready():
    print('Bot started')
    response = requests.get(API_URL)
    conResponse = Contest(response.text)
    conResult = conResponse.results
    upcomingContest = conResult[UPCOMING]#d["upcoming"] ls
    urlFile = open('url.txt','a+')
    urlFileRead = open('url.txt','r')
    readFile = urlFileRead.readlines()
    urlSet = set()
    for elem in readFile:
        r = elem.rstrip() #removes new line from end
        urlSet.add(r)

    channel = client.get_channel(IIIT_CONTEST_ALERT)

    for elem in upcomingContest:
        conName = elem[CONTEST_NAME]#elem["name"]
        conUrl = elem[CONTEST_URL]#elem["url"]
        startTime = elem[CONTEST_START_TIME]#elem["startTime"]
        conDay = datetime.datetime.fromtimestamp(startTime).timetuple()[2]
        currDay = datetime.datetime.now().timetuple()[2]
        conHour = datetime.datetime.fromtimestamp(startTime).timetuple()[3]
        daysLeft = conDay - currDay
        if (daysLeft <= 1 and daysLeft >=0)or (conHour <= 3 ):
            if ATCODER_STR in conName:
                conUrl = ATCODER + conUrl
            if conUrl not in urlSet:
                urlFile.write(conUrl)
                urlFile.write('\n')
                if CF in conName  and CF_DIV not in conName:
                    await channel.send(conUrl)
                else:
                    await channel.send(conUrl)

    urlFile.close()
    print('All Message sent')

client.run(TOKEN)
