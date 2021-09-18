# job title word segment then count it
from pythainlp import sent_tokenize
from pythainlp import word_tokenize, Tokenizer
from pythainlp.util import dict_trie
from pythainlp.corpus.common import thai_words
import math
from datetime import datetime

# connect db
def get_database():
    from pymongo import MongoClient
    import pymongo

    CONNECTION_STRING = "mongodb://jouThaiUsr01:jobpass@t2u-th.com/jobThai"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['jobThai']
db = get_database()
collectionJobList = db["jobList"]

def getCusWordList():
    # connect db
    db = get_database()
    collectionSimilarWord = db["similarWord"]

    # query all costom words
    simWords = collectionSimilarWord.find({},{'simWord':1})
    allCusWords = []
    for w in simWords:
        allCusWords.append(w['simWord'])
    return allCusWords

customWords = getCusWordList()
custom_words_list = set(thai_words())
## add multiple words
custom_words_list.update(customWords)
## add word
trie = dict_trie(dict_source=custom_words_list)
custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm', keep_whitespace=False)

###################### Config for Colab ###############################################

# create collection
collectionJobTitleWord = db["jobTitleWord"]
# drop old collection before start new segmentation and counting
collectionJobTitleWord.drop()

# get rows number
allRowsNum = collectionJobList.count_documents({})

# travel through all rows
print("Start job title word segmentation")
jobPerLoop  = 50
jobNum      = 1
for currSet in range( math.ceil(allRowsNum/jobPerLoop) ):
    jobs = collectionJobList.find({},None,currSet*jobPerLoop,jobPerLoop)
    for job in jobs:
        wordSeq = 1
        jobTitleWords = custom_tokenizer.word_tokenize(job["jobTitle"])
        for jobTitleWord in jobTitleWords:
            #print(wordSeq," ", jobTitleWord)
            wordSeq = wordSeq+1
            word = {
                "jobId"     : job["jobId"],
                "word"      : jobTitleWord,
                "seqNum"    : wordSeq,
                "timestamp" : datetime.today().replace(microsecond=0)
            }
            collectionJobTitleWord.insert_one(word)
        if(jobNum%100)==0:
            print(jobNum, end =" ")
            print(" segmented and added to db")
            #print(jobTitleWords, " segmented and added to db")
        jobNum = jobNum+1

#####################################################################

# job title word count
# create collection
collectionJobTitleWordCount = db["jobTitleWordCount"]
# drop old collection before start new segmentation and counting
collectionJobTitleWordCount.drop()

# select distinct 
words = collectionJobTitleWord.distinct( "word" )

# pipeline = [
#     {"$group": {"_id": "$word", "count": {"$sum": 1}}},
#     {"$skip":0},
#     {"$limit":20}
#  ]
# allWords = collectionJobInfo.aggregate( pipeline )

print("Start job title word count")
row = 1
for word in words:
    wordCount = collectionJobTitleWord.count_documents({"word":word})
    # add word and count to db
    wordCount2Db = {
            "word" : word,
            "count"  : wordCount,
            "timestamp" : datetime.today().replace(microsecond=0)
    }
    collectionJobTitleWordCount.insert_one(wordCount2Db)
    if(row%100)==0:
        print("added ", row)
    row = row + 1
