# jobDetail word segmentation
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

############################ config for VS Code #####################################

# create collection
collectionJobDetailWord = db["jobDetailWord"]
# get rows number
allRowsNum = collectionJobList.count_documents({})

def segAll():
    # travel through all rows
    jobPerLoop  = 50    # 50 rows per loop
    jobNum      = 1
    for currSet in range( math.ceil(allRowsNum/jobPerLoop) ):
        # find find(
        #           {}->select all ,
        #           None, 
        #           currSet*jobPerLoop->skip from first ,
        #           jobPerLoopall->limit per query 
        jobs = collectionJobList.find({},None,currSet*jobPerLoop,jobPerLoop)
        for job in jobs:
            wordSeq = 1
            jobDetailWords = custom_tokenizer.word_tokenize(job["jobDetail"])
            for jobDetailWord in jobDetailWords:
                # skip exixting word
                if collectionJobDetailWord.count_documents({"jobId":job["jobId"],"wordJobDetail":jobDetailWord})!=0:
                    continue
                wordSeq = wordSeq+1
                word = {
                    "jobId" : job["jobId"],
                    "wordJobDetail"  : jobDetailWord,
                    "seqNum": wordSeq,
                    "timestamp" : datetime.today().replace(microsecond=0)
                }
                collectionJobDetailWord.insert_one(word)
                jobNum = jobNum+1
            if (jobNum%1000)==0:
                print(jobNum,  "added")

segAll()
            
