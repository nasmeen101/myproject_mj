from connectMongo import get_database
from pymongo import MongoClient
import pymongo

# show all by sorting
# connect db
def getAllWord(limitRow):
    db = get_database() 
    collectionJobTitleWordCount = db["jobTitleWordCount"]
    collectionNoMeaningWord = db["noMeaningWord"]

    results = collectionJobTitleWordCount.find().sort("count",pymongo.DESCENDING).limit(limitRow)
    row = 1
    for result in results:
        # skip no meaning word
        if collectionNoMeaningWord.count_documents({"word":result['word']}) == 0:
            print(row, " ", end=" ")
            print(result['word']," ", result["count"])
        row = row + 1

def getJob(jobStr):
    db = get_database() 
    collectionJobTitleWordCount = db["jobTitleWordCount"]
    collectionSimilarWord = db["similarWord"]

    # get similar word for this job
    simWords = collectionSimilarWord.find({"mean":jobStr},{'simWord':1,'_id':0})
    # convert key to word
    simWordList = []
    for w in simWords:
        simWordList.append({'word':w['simWord']})
    # count all jobs
    countJobs = 0
    jobAllRows = collectionJobTitleWordCount.find({'$or':simWordList},{'count':1,'_id':0})
    for r in jobAllRows:
        countJobs = countJobs + r['count']
    return countJobs

def getAllCustomWord():
    db = get_database() 
    collectionJobTitleWordCount = db["jobTitleWordCount"]
    collectionSimilarWord = db["similarWord"]

    # all custom words
    means = collectionSimilarWord.distinct( "mean" )
    for m in means:
        print(m ,' = ', getJob(m)  )
        #print(m)

# print('dataAnalyst = ', getJob('dataAnalyst')  )
# print('programmer = ', getJob('programmer')  )
# getAllWord(50)
getAllCustomWord()

