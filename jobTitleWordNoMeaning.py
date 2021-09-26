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

if isAddNoMeanWord:
    addNoMeanWord(noMeanWord1)
    addNoMeanWord(noMeanWord2)
    addNoMeanWord(noMeanWord3)
    addNoMeanWord(noMeanWord4)
    addNoMeanWord(noMeanWord5)
    addNoMeanWord(noMeanWord6)
    addNoMeanWord(noMeanWord7)

    addNoMeanWord(noMeanWordF)
    addNoMeanWord(noMeanWordI)
    addNoMeanWord(noMeanwordO)
    addNoMeanWord(noMeanWordS)
    addNoMeanWord(noMeanWordT)

    addNoMeanWord(noMeanWordKorr)
    addNoMeanWord(noMeanWordKor)
    addNoMeanWord(noMeanWordNgong)
    addNoMeanWord(noMeanWordJau)
    addNoMeanWord(noMeanWordTor)
    addNoMeanWord(noMeanWordNoor)
    addNoMeanWord(noMeanWordPor)
    addNoMeanWord(noMeanWordLor)
    addNoMeanWord(moMeanWordRor)
    addNoMeanWord(noMeanWordPorP)
    addNoMeanWord(noMeanWordOr)
    addNoMeanWord(noMeanWordSor)
    addNoMeanWord(noMeanWordDoor)  
    addNoMeanWord(noMeanWordHoor)