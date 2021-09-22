# jobDetail word segmentation

# config for VS Code ####################################################################33

def segAll():
    import math
    from datetime import datetime
    # connect db
    from connectMongo import get_database
    db = get_database()
    collectionJobList = db["jobList"]
    collectionJobDetailWord = db["jobDetailWord"]

    from customWords import getCusWordList
    from pythainlp import Tokenizer
    from pythainlp.util import dict_trie
    from pythainlp.corpus.common import thai_words
    custom_words_list = set(thai_words())
    ## add multiple technical words
    custom_words_list.update(getCusWordList())
    ## add technical words
    trie = dict_trie(dict_source=custom_words_list)
    custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm', keep_whitespace=False)
    
    # travel through all jobList
    # get rows number
    allRowsNum = collectionJobList.count_documents({})
    jobPerLoop  = 50    # 50 rows per loop
    jobNum      = 1
    wordNum     = 1
    for currSet in range( math.ceil(allRowsNum/jobPerLoop) ):
        # find find(
        #           {}->select all ,
        #           None, 
        #           currSet*jobPerLoop->skip from first ,
        #           jobPerLoopall->limit per query 
        jobs = collectionJobList.find(
                {},
                {'jobId':1,'jobDetail':1,'_id':0},
                currSet*jobPerLoop,
                jobPerLoop)
        # travel through all job rows in range (50 jobs per loop)
        for job in jobs:
            wordSeq = 1
            jobDetailWords = custom_tokenizer.word_tokenize(job["jobDetail"])
            # check existing job
            isJobExist = False
            if( not(collectionJobDetailWord.find_one(
                    {"jobId":job["jobId"]},
                    {'seqNum':1,'_id':0}) is None) ):
                isJobExist = True
            # travel through all word rows
            for jobDetailWord in jobDetailWords:
                # skip existing word in existing job
                if isJobExist and not( 
                        collectionJobDetailWord.find_one(
                            {"jobId":job["jobId"],"wordJobDetail":jobDetailWord},
                            {'seqNum':1,'_id':0}) is None ):
                    continue
                wordSeq = wordSeq+1
                wordNum = wordNum+1
                word = {
                    "jobId" : job["jobId"],
                    "wordJobDetail"  : jobDetailWord,
                    "seqNum": wordSeq,
                    "timestamp" : datetime.today().replace(microsecond=0)
                }
                collectionJobDetailWord.insert_one(word)
                if (wordNum%1000)==0:
                    print('Word num ', wordNum,  "added")
            jobNum = jobNum+1
            if (jobNum%100)==0:
                print('jobNum ', jobNum,  "added")

def segUpdateCusWord():
    # update segmented word by new cusWord added
    import math
    from datetime import datetime

    import pymongo
    from customWords import getCusWordListByGreaterDate
    from customWords import countNewCusWordRowByDate

    from customWords import getCusWordList
    from pythainlp import Tokenizer
    from pythainlp.util import dict_trie
    from pythainlp.corpus.common import thai_words
    # get newest detailWord update
    # connect db
    from connectMongo import get_database
    db = get_database()
    collectionJobDetailWord = db["jobDetailWord"]
    newestDetailWordDateObj = collectionJobDetailWord.find(
                                {},
                                {'timestamp':1,'_id':0}).sort(  "timestamp",
                                                                pymongo.DESCENDING).limit(1)
    newestDetailWordDate = datetime.today()
    for wd in newestDetailWordDateObj:
        newestDetailWordDate = wd['timestamp']
    
    # count number of new cusWord
    newCusWordNum       = countNewCusWordRowByDate(newestDetailWordDate)
    checkedCusWordNum   = 0
    newWordFound        = 0
 
    if newCusWordNum>0:
        # prepare all cusWord list and custom_tokenizer
        custom_words_list = set(thai_words())
        ## add multiple technical words
        custom_words_list.update(getCusWordList())
        ## add technical words
        trie = dict_trie(dict_source=custom_words_list)
        custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm', keep_whitespace=False)

        # for get job list
        collectionJobList = db["jobList"]

        # do loop through newCusWordList
        cusWordPerLoop = 50
        for numLoop in range( math.ceil(newCusWordNum/cusWordPerLoop) ):
            # query cusWord that newwer than newsest detailWord update
            newCusWordList = []
            newCusWordList = newCusWordList+getCusWordListByGreaterDate(
                                                newestDetailWordDate,
                                                numLoop*cusWordPerLoop,
                                                cusWordPerLoop)   
            
            # query jobs by 'like' new cusWord
            for w in newCusWordList:
                checkedCusWordNum = checkedCusWordNum+1
                # travel through all jobList that match 'like' new cusWord
                allRowsNum = collectionJobList.count_documents({'jobDetail':{'$regex': '/.*'+w+'.*/'}})
                print(w,' ', allRowsNum)
                jobPerLoop  = 50    # 50 jobs per loop
                jobNum      = 1
                wordNum     = 1
                for currSet in range( math.ceil(allRowsNum/jobPerLoop) ):
                    # query job only 'like' new cusWord
                    jobs = collectionJobList.find(
                                                {'jobDetail':{'$regex': '/.*'+w+'.*/'}},
                                                {'jobId':1,'jobDetail':1,'_id':0},
                                                currSet*jobPerLoop,
                                                jobPerLoop)
                    
                    # travel through all job rows in range (50 jobs per loop)
                    for job in jobs:
                        wordSeq = 1
                        jobDetailWords = custom_tokenizer.word_tokenize(job["jobDetail"])
                        # check existing job
                        isJobExist = False
                        if( not(collectionJobDetailWord.find_one(
                                                            {"jobId":job["jobId"]},
                                                            {'seqNum':1,'_id':0}) is None) ):
                            isJobExist = True
                        # travel through all word rows
                        for jobDetailWord in jobDetailWords:
                            # skip existing word in existing job
                            if isJobExist and not( 
                                                collectionJobDetailWord.find_one(    
                                                                    {"jobId":job["jobId"],
                                                                    "wordJobDetail":jobDetailWord},
                                                                    {'seqNum':1,'_id':0}) is None ):
                                continue
                            wordSeq = wordSeq+1
                            wordNum = wordNum+1
                            word = {
                                "jobId" : job["jobId"],
                                "wordJobDetail"  : jobDetailWord,
                                "seqNum": wordSeq,
                                "timestamp" : datetime.today().replace(microsecond=0)
                            }
                            collectionJobDetailWord.insert_one(word)
                            newWordFound = newWordFound + 1
                            if (wordNum%1000)==0:
                                print('Word num ', wordNum,  "added")
                        jobNum = jobNum+1
                        if (jobNum%100)==0:
                            print('jobNum ', jobNum,  "added")
    
    print('newCusWordNum ',newCusWordNum)
    print('checkedCusWordNum ',checkedCusWordNum)
    print('newWordFound',newWordFound)
    # update latest jobDetailWord timestamp if no new word added
    if newWordFound == 0:
        collectionJobDetailWord.find_one_and_update({'timestamp':newestDetailWordDate},{'$set': {'timestamp': datetime.today().replace(microsecond=0)}})
        print("jobDetailWord timestamp updated")

segUpdateCusWord()
# segAll()
