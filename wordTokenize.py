class WordTokenize:
    def __init__(self):
        """
        """
  
    def segWord(self, dbUsr, dbPass, dbName, srcJobsCollName, srcFieldName, dstCollName, queryFilter):
        """
        word segmentation 
        query filter for new job -> {'lastestAction' : 'newAdded'}
        :param dbUsr: database user name
        :param dbPass: database password
        :param dbName: database name
        :param srcJobsCollName: source collection name 
        :param srcFieldName: source field name
        :param dstCollName: distination collection name (counted words)
        """
        # connect to db
        CONNECTION_STRING = "mongodb://"+dbUsr+":"+dbPass+"@t2u-th.com/"+dbName
        from pymongo import MongoClient
        client = MongoClient(CONNECTION_STRING)
        self.db = client[dbName]
        self.collectionSrcJobsCollName = self.db[srcJobsCollName]
        self.srcFieldName = srcFieldName
        self.collectionDstCollName = self.db[dstCollName]
        self.queryFilter = queryFilter

        import math
        from datetime import datetime

        # from customWords import getCusWordList
        from customWords import CustomWord
        cw = CustomWord('jouThaiUsr01','jobpass','jobThai')
        from pythainlp import Tokenizer
        from pythainlp.util import dict_trie
        from pythainlp.corpus.common import thai_words
        custom_words_list = set(thai_words())
        ## add multiple technical words
        custom_words_list.update( cw.getTechJobWordList() )
        ## add technical words
        trie = dict_trie(dict_source=custom_words_list)
        custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm', keep_whitespace=False)
        
        # travel through all new jobList
        # get lastest 
        # get rows number
        allRowsNum = self.collectionSrcJobsCollName.count_documents(self.queryFilter)
        print(self.queryFilter," | job num: ", allRowsNum)
        jobPerLoop  = 100    
        jobNum      = 1
        wordNum     = 1
        remainJobs  = allRowsNum
        while remainJobs > 0:
            jobs = self.collectionSrcJobsCollName.find(
                    self.queryFilter,
                    {'jobId':1,self.srcFieldName:1,'_id':0},
                    0,
                    jobPerLoop)
            # travel through all job rows in range (50 jobs per loop)
            for job in jobs:
                wordSeq = 1
                jobWords = custom_tokenizer.word_tokenize(job[self.srcFieldName])
                # check existing job
                if( not(self.collectionDstCollName.find_one(
                        {"jobId":job["jobId"]},
                        {'seqNum':1,'_id':0}) is None) ):
                    # remove old word segmented if exist
                    self.collectionDstCollName.remove({"jobId":job["jobId"]},True)
                # travel through all word rows
                for jobWord in jobWords:
                    wordSeq = wordSeq+1
                    wordNum = wordNum+1
                    word = {
                        "jobId" : job["jobId"],
                        "word_"+self.srcFieldName  : jobWord,
                        "seqNum": wordSeq,
                        'lastAct': 'newAdded',
                        "updateDate" : datetime.today().replace(microsecond=0),
                        'createDate' : datetime.today().replace(microsecond=0)
                    }
                    self.collectionDstCollName.insert_one(word)
                    if (wordNum%1000)==0:
                        print('Word num ', wordNum,  "added")
                #update lastest action for job to word segmented
                self.collectionSrcJobsCollName.update_one(
                    {'jobId':job["jobId"]},
                    {'$set' : { 'lastAct' :'seg_'+self.srcFieldName,
                                "updateDate"     : datetime.today().replace(microsecond=0)}})
                jobNum = jobNum+1
                if (jobNum%100)==0:
                    print('jobNum ', jobNum,  "added")
            remainJobs = self.collectionSrcJobsCollName.count_documents(self.queryFilter)