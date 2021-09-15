from connectMongo import get_database
from datetime import datetime

# connect db
db = get_database()
collectionJobTitleWord = db["jobTitleWord"]
collectionJobTitleWordCount = db["jobTitleWordCount"]

# select distinct 
words = collectionJobTitleWord.distinct( "word" )

# pipeline = [
#     {"$group": {"_id": "$word", "count": {"$sum": 1}}},
#     {"$skip":0},
#     {"$limit":20}
#  ]
# allWords = collectionJobInfo.aggregate( pipeline )

row = 1
for word in words:
    wordCount = collectionJobTitleWord.count_documents({"word":word})
    # add word and count to db
    wordCount2Db = {
            "word" : word,
            "count"  : wordCount,
            "timeStamp" : datetime.today().replace(microsecond=0)
    }
    collectionJobTitleWordCount.insert_one(wordCount2Db)
    if(row%100)==0:
        print("added ", row)
    row = row + 1

    # result.find().sort("_id"):
    #print(row, " ", word, " ", allRowsNum)
    #row = row + 1
# collectionJobInfo.aggregate([
#     {$sort:{"created_at":-1}},
#     {$project:{"event_type_id":1}},
#     {$group:{"_id":"$event_type_id"}},
#     {$skip:10},
#     {$limit:20}
# ])
# count rows number
#allRowsNum = collectionJobList.count_documents({})