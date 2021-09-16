# add no meaning word to db
isAddNoMeanWord = True
def addNoMeanWord(wordList):
    from connectMongo import get_database
    from datetime import datetime
    # connect db
    db = get_database()
    collectionNoMeaningWord = db["noMeaningWord"]

    for w in wordList:
        # insert if not exist
        if collectionNoMeaningWord.count_documents({"word":w}) == 0:
            wordAdd = {
                "word" : w,
                "timestamp" : datetime.today().replace(microsecond=0)
            }
            collectionNoMeaningWord.insert_one(wordAdd)

# no meaning word for jot title
noMeanWord1 = ['(',')','/',')/',':(','[',']',')]','+','+','*','IT',':',',','-','–','&','@','K','.','!!!!']
noMeanWord2 = ['Project','Technical','Officer','1','นัก','T','Service','คอมพิวเตอร์','and']
noMeanWord3 = ['ใหม่','Data','นักศึกษา','Desk','และ','Front','End','**']
noMeanWord4 = ['Development']
noMeanWord5 = ['งาน','ยินดี','3','Company','ไอที','Staff','staff','2','Analyst','บริษัท','ได้']
noMeanWord6 = ['Solution','Quality','ฝ่าย','รับสมัคร','บาง','ไทย','Job','หรือ','ใกล้']
noMeanWord7 = ['ติดต่อ','อ.','Back',')(','Services','or','Product','คุณ','ที่ไหน']
noMeanWordS = ['Section','Support','SUPPORT','System','Systems','support']
noMeanWordJau   = ['จาก','เจ้าหน้าที่','จบ','จ.','จังหวัด']
noMeanWordTor   = ['ที่ไหน','เทคโนโลยีสารสนเทศ','ที่','ทำงาน']
noMeanWordPor   = ['ประจำ','ปฏิบัติงาน']
moMeanWordRor   = ['ระบบ','รับ']
noMeanWordPorP  = ['พัฒนา','พนักงาน']
noMeanWordOr    = ['อุตสาหกรรม']
noMeanWordSor   = ['สารสนเทศ','สนับสนุน','สาขา','สัญญาจ้าง','สาขา','สำนักงานใหญ่']
noMeanWordDoor  = ['ดูแล','เดือน']

if isAddNoMeanWord:
    addNoMeanWord(noMeanWord1)
    addNoMeanWord(noMeanWord2)
    addNoMeanWord(noMeanWord3)
    addNoMeanWord(noMeanWord4)
    addNoMeanWord(noMeanWord5)
    addNoMeanWord(noMeanWord6)
    addNoMeanWord(noMeanWord7)
    addNoMeanWord(noMeanWordS)
    addNoMeanWord(noMeanWordJau)
    addNoMeanWord(noMeanWordTor)
    addNoMeanWord(noMeanWordPor)
    addNoMeanWord(moMeanWordRor)
    addNoMeanWord(noMeanWordPorP)
    addNoMeanWord(noMeanWordOr)
    addNoMeanWord(noMeanWordSor)
    addNoMeanWord(noMeanWordDoor)  