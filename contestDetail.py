import requests
import constant
import json
import datetime
import db

contestCollection = db.startDB()

contestResult = (json.loads(requests.get(constant.API_URL).text))['results']
upcomingContest = contestResult[constant.UPCOMING]

def getDuration(startTime):
    contestDay = datetime.datetime.fromtimestamp(startTime).timetuple()[2]
    currDay = datetime.datetime.now().timetuple()[2]
    contestHour = datetime.datetime.fromtimestamp(startTime).timetuple()[3]
    daysLeft = contestDay - currDay
    return [contestHour , daysLeft]

for contest in upcomingContest:
    if(str(contest['platform']) in constant.webList):
        isSend = False
        platform = str(contest['platform'])
        contestUrl = contest['url']
        if platform == 'atcoder':
            contestUrl = constant.ATCODER + contestUrl
        duration = getDuration(contest[constant.CONTEST_START_TIME])
        if duration[0] <= 3:
            isSend = True
        if contestCollection.find_one({"_id" : contestUrl}):
            print('url already exist')
        else:
            db.storeData(contestCollection,{"_id" : contestUrl})
            if duration[1] <= 1 and duration[1] >=0:
                isSend = True
        if(isSend):
            print('sending message to bot')

