class WordCount:
    def __init__(self, dbUsr, dbPass, dbName, wordCollName, wordCountCollName, wordFieldName, seqNumFieldName):
        """:param dbPass: database password
        :param dbName: database name
        :param wordCollName: source collection name 
        :param wordCountCollName: distination collection name (counted words)
        :param wordFieldName: source word field name
        :param seqNumFieldName: source word sequence field name
        """
        # connect to db
        CONNECTION_STRING = "mongodb://"+dbUsr+":"+dbPass+"@t2u-th.com/"+dbName
        from pymongo import MongoClient
        client = MongoClient(CONNECTION_STRING)
        self.db = client[dbName]
        self.collectionWord = self.db[wordCollName]
        self.collectionWordCount = self.db[wordCountCollName]
        self.wordFieldName = wordFieldName
        self.seqNumFieldName = seqNumFieldName

    def counting(self):
        # select distinct
        # words = self.collectionWord.distinct( self.wordFieldName )
        pipeline = [{"$group": 
                        {   "_id"   : '$'+self.wordFieldName, 
                            'avgSeq': { '$avg': "$"+self.seqNumFieldName },
                            "count" : {"$sum": 1}
                        }
                    } ]
        words = self.collectionWord.aggregate( pipeline )
        from datetime import datetime
        row = 0
        for word in words:
            print(word)
            # add word and count to db
            wordCount2Db = {
                    "word"      : word['_id'],
                    "count"     : word['count'],
                    'avgSeq'    : word['avgSeq'],
                    "timestamp" : datetime.today().replace(microsecond=0)
            }
            self.collectionWordCount.insert_one(wordCount2Db)
            if(row%100)==0:
                print("added ", row)
            row = row + 1

        # pipeline = [
        #     {"$group": {"_id": "$word", "count": {"$sum": 1}}},
        #     {"$skip":0},
        #     {"$limit":20}
        #  ]
        # allWords = collectionJobInfo.aggregate( pipeline )

        # couunt distince key/value
        # pipeline = [ {"$group": {"_id": '$'+self.wordFieldName, "count": {"$sum": 1}}} ]
        

