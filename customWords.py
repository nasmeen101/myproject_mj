# technicalWords

isDebug = False
isAddNewCusWord = True

# add customword to db
def addCusWord(mean,simWordList):
    from connectMongo import get_database
    from datetime import datetime
    # connect db
    db = get_database()
    collectionSimilarWord = db["similarWord"]

    for w in simWordList:
        # insert if not exist
        if collectionSimilarWord.count_documents({"simWord":w}) == 0:
            newSimWord = {  'mean':mean,
                            'simWord':w,
                            'timestamp':datetime.today().replace(microsecond=0)}
            collectionSimilarWord.insert_one(newSimWord)

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

if isAddNewCusWord:
    addCusWord('itSupport'  ,itSupport)
    addCusWord('fullStack'  ,fullStack)
    addCusWord('frontEnd'   ,frontEnd)
    addCusWord('backEnd'    ,backEnd)
    addCusWord('programmer' ,programmer)
    addCusWord('developer'  ,developer)
    addCusWord('sysAnalyst' ,sysAnalyst)
    addCusWord('dataAnalyst',dataAnalyst)
    addCusWord('busAnalyst' ,busAnalyst)
    addCusWord('progAnalyst',progAnalyst)
    addCusWord('softAnalyst',softAnalyst)
    addCusWord('secAnalyst' ,secAnalyst)
    addCusWord('webMaster'  ,webMaster)
    addCusWord('tester'     ,tester)

# programming languages & database
langCpp = [ "C++", "c++" ]
langCsh = [ "C#", "c#" ]
langNet = [ ".net", ".NET", ".Net" ]
langVb  = [ "VB", "vb" ]
react   = [ "React",'react']
angular = [ "Angular", "angular"]
flutter = [ "Flutter", 'flutter']
database = [ 'ฐานข้อมูล','Database','database','data base']

if isAddNewCusWord:
    addCusWord('langCpp'    ,langCpp)
    addCusWord('langCsh'    ,langCsh)
    addCusWord('langNet'    ,langNet)
    addCusWord('langVb'     ,langVb)
    addCusWord('react'      ,react)
    addCusWord('angular'    ,angular)
    addCusWord('flutter'    ,flutter)
    addCusWord('database'   ,database)

# operating system
iOS         = ['iOS','IOS']
androidOS   = ['Android','android']
linuxOS     = ['Linux','linux']

if isAddNewCusWord:
    addCusWord('iOS'        ,iOS)
    addCusWord('androidOS'  ,androidOS)
    addCusWord('linuxOS'    ,linuxOS)

# experience
jobExp0y = ['จบใหม่']
jobExp1y = ['1 ปี','1ปี','1 year','1year','1yr.','1yr']
jobExp2y = ['2 ปี','2ปี','2 year','2year','2 years','2years','2yr.','2yr']
jobExp3y = ['3 ปี','3ปี','3 year','3year','3 years','3years','3yr.','3yr']
jobExp5y = ['5 ปี','5ปี','5 year','5year','5 years','5years','5yr.','5yr']
jobExp10y = ['10 ปี','10ปี','10 year','10year','10 years','10years','10yr.','10yr']

if isAddNewCusWord:
    addCusWord('jobExp0y' ,jobExp0y)
    addCusWord('jobExp1y' ,jobExp1y)
    addCusWord('jobExp2y' ,jobExp2y)
    addCusWord('jobExp3y' ,jobExp3y)
    addCusWord('jobExp5y' ,jobExp5y)
    addCusWord('jobExp10y' ,jobExp10y)

# generate customword list
def getCusWordList():
    from connectMongo import get_database
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

# debug
if isDebug:
    for w in customWords:
        print(w)
