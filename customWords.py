class CustomWord:
    def __init__(self, dbUsr, dbPass, dbName):
        """
        add custom word to DB for grouping known technical words & no meaning words
        :param dbUsr: database user name
        :param dbPass: database password
        :param dbName: database name
        """
        # connect to db
        CONNECTION_STRING = "mongodb://"+dbUsr+":"+dbPass+"@t2u-th.com/"+dbName
        from pymongo import MongoClient
        client = MongoClient(CONNECTION_STRING)
        self.db = client[dbName]

       
        # self.isDebug = False
        # self.isAddNewCusWord = True

    # add customword to db
    def addTechJobWord(self,mean,simWordList):
        from datetime import datetime
        # connect db
        collectionSimilarWord = self.db["similarWord"]

        for w in simWordList:
            # insert if not exist
            if collectionSimilarWord.count_documents({"simWord":w}) == 0:
                newSimWord = {  'mean'      :mean,
                                'simWord'   :w,
                                'lastAct'   :'newAdded',
                                'updateDate':datetime.today().replace(microsecond=0),
                                'createDate':datetime.today().replace(microsecond=0)}
                collectionSimilarWord.insert_one(newSimWord)

    def addNewTechJobWord(self):
        # job titles
        # insert if not exist (set upsert to True)
        itSupport   = [ "IT Support" ]
        fullStack   = [ "full stack", "Full Stack", "Fullstack", "Full stack", "Full-Stack", "Full-Stacked",
                        "FullStack"]
        frontEnd    = [ "Frontend","Front – end", "Front-end",  "Front end" ]
        backEnd     = [ "Backend" ,"Back - end",  "Back-end",   "Back end"]
        programmer  = [ "Programmer", "programmer", "Programmers","programmers", "โปรแกรมเมอร์"]
        developer   = [ 'Developer','developer','นักพัฒนา']
        sysAnalyst  = [ "System Analyst", "system analyst", "วิเคราะห์ระบบ" ]
        dataAnalyst = [ "Data Analyst", "Data Scientist", "data analyst", "data scientist", "วิเคราะห์ข้อมูล"]
        busAnalyst  = [ "Business Analyst", "business analyst"]              
        progAnalyst = [ "Programmer Analyst", "programmer analyst", "วิเคราะห์โปรแกรม", "วิเคราะห์แอปพลิเคชัน"]  
        softAnalyst = [ "Software Analyst", "software analyst", "SAP Support Analyst",
                        "Technical Analyst", "technical analyst", "IT Analyst"]              
        secAnalyst  = [ "Security Analyst", "security analyst", "Cyber Security", "cyber security"]  
        webMaster   = [ 'Webmaster', 'web master', 'Web master', 'ผู้ดูแลเว็บไซต์', 'เว็บแอดมิน']
        tester      = [ 'Tester','Test Engineer', 'Software Tester','Software Testers','Software Test','Software Test Engineer','Software Quality Assurance','เทสเตอร์']

        # if self.isAddNewCusWord:
        self.addTechJobWord('itSupport'  ,itSupport)
        self.addTechJobWord('fullStack'  ,fullStack)
        self.addTechJobWord('frontEnd'   ,frontEnd)
        self.addTechJobWord('backEnd'    ,backEnd)
        self.addTechJobWord('programmer' ,programmer)
        self.addTechJobWord('developer'  ,developer)
        self.addTechJobWord('sysAnalyst' ,sysAnalyst)
        self.addTechJobWord('dataAnalyst',dataAnalyst)
        self.addTechJobWord('busAnalyst' ,busAnalyst)
        self.addTechJobWord('progAnalyst',progAnalyst)
        self.addTechJobWord('softAnalyst',softAnalyst)
        self.addTechJobWord('secAnalyst' ,secAnalyst)
        self.addTechJobWord('webMaster'  ,webMaster)
        self.addTechJobWord('tester'     ,tester)

        # programming languages & database
        langCpp = [ "C++", "c++" ]
        langCsh = [ "C#", "c#" ]
        langNet = [ ".net", ".NET", ".Net" ]
        langVb  = [ "VB", "vb" ]
        react   = [ "React",'react']
        angular = [ "Angular", "angular"]
        flutter = [ "Flutter", 'flutter']
        database = [ 'ฐานข้อมูล','Database','database','data base']

        # if self.isAddNewCusWord:
        self.addTechJobWord('langCpp'    ,langCpp)
        self.addTechJobWord('langCsh'    ,langCsh)
        self.addTechJobWord('langNet'    ,langNet)
        self.addTechJobWord('langVb'     ,langVb)
        self.addTechJobWord('react'      ,react)
        self.addTechJobWord('angular'    ,angular)
        self.addTechJobWord('flutter'    ,flutter)
        self.addTechJobWord('database'   ,database)

        # operating system
        iOS         = ['iOS','IOS']
        androidOS   = ['Android','android']
        linuxOS     = ['Linux','linux']

        # if self.isAddNewCusWord:
        self.addTechJobWord('iOS'        ,iOS)
        self.addTechJobWord('androidOS'  ,androidOS)
        self.addTechJobWord('linuxOS'    ,linuxOS)

        # experience
        jobExp0y = ['จบใหม่']
        jobExp1y = ['1 ปี','1ปี',
                    '1-2ปี','1-2 ปี','1 - 2ปี','1 - 2 ปี','1- 2ปี','1 -2ปี','1- 2 ปี','1 -2 ปี',
                    '1-3ปี','1-3 ปี','1 - 3ปี','1 - 3 ปี','1- 3ปี','1 -3ปี','1- 3 ปี','1 -3 ปี',
                    '1 year','1year','1yr.','1yr',
                    '1-2years','1-2 years','1-2year','1-2 year',
                    '1-3years','1-3 years','1-3year','1-3 year']
        jobExp2y = ['2 ปี','2ปี',
                    '1-2ปี','1-2 ปี','1 - 2ปี','1 - 2 ปี','1- 2ปี','1 -2ปี','1- 2 ปี','1 -2 ปี',
                    '2 year','2year','2 years','2years','2yr.','2yr',
                    '1-2years','1-2 years','1-2year','1-2 year']
        jobExp3y = ['3 ปี','3ปี',
                    '1-3ปี','1-3 ปี','1 - 3ปี','1 - 3 ปี','1- 3ปี','1 -3ปี','1- 3 ปี','1 -3 ปี',
                    '3 year','3year','3 years','3years','3yr.','3yr',
                    '1-3years','1-3 years','1-3year','1-3 year']
        jobExp5y = ['5 ปี','5ปี','5 year','5year','5 years','5years','5yr.','5yr']
        jobExp10y = ['10 ปี','10ปี','10 year','10year','10 years','10years','10yr.','10yr']

        # if self.isAddNewCusWord:
        self.addTechJobWord('jobExp0y' ,jobExp0y)
        self.addTechJobWord('jobExp1y' ,jobExp1y)
        self.addTechJobWord('jobExp2y' ,jobExp2y)
        self.addTechJobWord('jobExp3y' ,jobExp3y)
        self.addTechJobWord('jobExp5y' ,jobExp5y)
        self.addTechJobWord('jobExp10y' ,jobExp10y)

    def addNoMeaningWord(self,noMeanWordList):
        from datetime import datetime
        # connect db
        collectionNoMeaningWord = self.db["noMeaningWord"]

        for w in noMeanWordList:
            # insert if not exist
            if collectionNoMeaningWord.count_documents({"word":w}) == 0:
                wordAdd = {
                    "word"      : w,
                    'lastAct'   :'newAdded',
                    'updateDate':datetime.today().replace(microsecond=0),
                    'createDate':datetime.today().replace(microsecond=0)
                }
                collectionNoMeaningWord.insert_one(wordAdd)
    
    def addNewNoMeaningWord(self):
        # no meaning word for jot title
        noMeanWord1 = ['(',')',')(','/',')/',':(','[',']',')]','+','+','*','•','IT',':',',','-','–','&','@','K','.','!!!!']
        noMeanWord2 = ['Project','Technical','Officer','1','นัก','T','Service','คอมพิวเตอร์','and']
        noMeanWord3 = ['Data','นักศึกษา','Desk','Front','End','**']
        noMeanWord4 = ['Development']
        noMeanWord5 = ['ยินดี','3','Company','Staff','staff','2','Analyst','บริษัท']
        noMeanWord6 = ['Solution','Quality','ฝ่าย','บาง','Job']
        noMeanWord7 = ['ติดต่อ','อ.','Back','Services','Product','คุณ']

        noMeanWordF = ['for']
        noMeanWordI = ['in']
        noMeanwordO = ['of','or']
        noMeanWordS = ['Section','Support','SUPPORT','System','Systems','support']
        noMeanWordT = ['the']

        noMeanWordKorr  = ['การ','กับ','ใกล้']
        noMeanWordKor   = ['ของ']
        noMeanWordNgong = ['งาน']
        noMeanWordJau   = ['จาก','เจ้าหน้าที่','จบ','จ.','จังหวัด']
        noMeanWordTor   = ['ที่ไหน','ไทย','เทคโนโลยีสารสนเทศ','ที่','ทำงาน']
        noMeanWordNoor  = ['ใน']
        noMeanWordPor   = ['ประจำ','ปฏิบัติงาน']
        moMeanWordRor   = ['ระบบ','รับ','รับสมัคร']
        noMeanWordLor   = ['และ']
        noMeanWordPorP  = ['พัฒนา','พนักงาน','เพื่อ']
        noMeanWordOr    = ['อุตสาหกรรม','ไอที']
        noMeanWordSor   = ['สารสนเทศ','สนับสนุน','สาขา','สัญญาจ้าง','สาขา','สำนักงานใหญ่','สามารถ']
        noMeanWordDoor  = ['ดูแล','เดือน','ได้','ด้าน']
        noMeanWordHoor  = ['ให้','หรือ','ใหม่']

        self.addNoMeaningWord(noMeanWord1)
        self.addNoMeaningWord(noMeanWord2)
        self.addNoMeaningWord(noMeanWord3)
        self.addNoMeaningWord(noMeanWord4)
        self.addNoMeaningWord(noMeanWord5)
        self.addNoMeaningWord(noMeanWord6)
        self.addNoMeaningWord(noMeanWord7)

        self.addNoMeaningWord(noMeanWordF)
        self.addNoMeaningWord(noMeanWordI)
        self.addNoMeaningWord(noMeanwordO)
        self.addNoMeaningWord(noMeanWordS)
        self.addNoMeaningWord(noMeanWordT)

        self.addNoMeaningWord(noMeanWordKorr)
        self.addNoMeaningWord(noMeanWordKor)
        self.addNoMeaningWord(noMeanWordNgong)
        self.addNoMeaningWord(noMeanWordJau)
        self.addNoMeaningWord(noMeanWordTor)
        self.addNoMeaningWord(noMeanWordNoor)
        self.addNoMeaningWord(noMeanWordPor)
        self.addNoMeaningWord(noMeanWordLor)
        self.addNoMeaningWord(moMeanWordRor)
        self.addNoMeaningWord(noMeanWordPorP)
        self.addNoMeaningWord(noMeanWordOr)
        self.addNoMeaningWord(noMeanWordSor)
        self.addNoMeaningWord(noMeanWordDoor)  
        self.addNoMeaningWord(noMeanWordHoor)

    # generate tecnical & job related word list
    def getTechJobWordList(self):
        # connect db
        collectionSimilarWord = self.db["similarWord"]

        # query all costom words
        simWords = collectionSimilarWord.find({},{'simWord':1})
        allCusWords = []
        for w in simWords:
            allCusWords.append(w['simWord'])
        return allCusWords

    def countTechJobWordRowByDate(self,date):
        # connect db
        collectionSimilarWord = self.db["similarWord"]  
        return collectionSimilarWord.count_documents({"createDate": {"$gt": date}})

    def getTechJobWordListByGreaterDate(self,dateSearch,skip,limit):
        # connect db
        collectionSimilarWord = self.db["similarWord"]

        # query costom words that greater giving date
        simWords = collectionSimilarWord.find({"createDate": {"$gt": dateSearch}},{'simWord':1,'_id':0}).skip(skip).limit(limit)

        allCusWords = []
        for w in simWords:
            allCusWords.append(w['simWord'])
        return allCusWords

    #customWords = getTechJobWordList()

    def debug(self):
        # debug
        # if self.isDebug:
        for w in self.getTechJobWordList():
            print(w)

# cw = CustomWord('jouThaiUsr01','jobpass','jobThai')
# cw.addNewNoMeaningWord()
# cw.addNewTechJobWord()