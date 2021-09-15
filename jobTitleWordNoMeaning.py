from connectMongo import get_database
from datetime import datetime
# connect db
db = get_database()
collectionNoMeaningWord = db["noMeaningWord"]

# no meaning word for jot title
noMeanWord1 = ['(',')','/','IT','เจ้าหน้าที่',',','Support','SUPPORT','System','-','ประจำ','&','ระบบ','K','พัฒนา','.']
noMeanWord2 = ['Project','Technical','Officer','1','นัก','สารสนเทศ','T','Service','คอมพิวเตอร์','and']
noMeanWord3 = ['ใหม่','จบ','–','รับ','สาขา','Data','สาขา','สัญญาจ้าง','นักศึกษา','Desk','และ','Front','End','**']
noMeanWord4 = ['สำนักงานใหญ่','*','Development','support','สนับสนุน','เทคโนโลยีสารสนเทศ','ที่','@','จ.']
noMeanWord5 = ['งาน','ยินดี','3','Company','ทำงาน','[','ไอที','Staff','staff','2','Analyst','บริษัท','ได้']
noMeanWord6 = ['ปฏิบัติงาน','Solution','Quality','ฝ่าย','พนักงาน','รับสมัคร','บาง','ไทย','Job','หรือ','ใกล้']
noMeanWord7 = ['ติดต่อ','อ.','Back',')(','Services','or','Product']

noMeanWordAll = noMeanWord1 + noMeanWord2 + noMeanWord3 + noMeanWord4 + noMeanWord5 + noMeanWord6 + noMeanWord7

for word in noMeanWordAll:
    wordAdd = {
                "word" : word,
                "timestamp" : datetime.today().replace(microsecond=0)
            }
    # insert if not exist (set upsert to True)
    collectionNoMeaningWord.update_one({"word":word},{"$set": wordAdd},True)