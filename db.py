from pymongo import MongoClient

def startDB():
  client = MongoClient('mongodb://127.0.0.1:27017/')
  contestDB = client["contestdb"]
  contestCollection = contestDB["contestCollection"]
  return contestCollection

def storeData(contestCollection,constestInfo):
  contestCollection.insert_one(constestInfo)

# mycol = startDB()
# try:
#   constestInfo = {"_id" : "www.google.com"}
#   storeData(mycol,constestInfo)
# except:
#   pass

    # {
    #     "_id": "https://csacademy.com/contest/algorithms-2020-11-25-0",
    #     "startTime": 1606262400,
    #     "endTime": 1606265700
    #   }


