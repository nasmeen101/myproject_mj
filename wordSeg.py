from pythainlp import sent_tokenize, word_tokenize
from connectMongo import get_database
import math

# connect db
db = get_database()
collectionJobList = db["jobList"]
collectionJobInfo = db["jobInfo"]

# get rows number
allRowsNum = collectionJobList.count_documents({})

# travel through all rows
jobPerLoop = 3
for currSet in range( math.ceil(allRowsNum/50) ):
    jobs = collectionJobList.find({},None,currSet*jobPerLoop,jobPerLoop)
    for job in jobs:
        #print( job["jobTitle"],"\n")
        print("no whitespace:", word_tokenize(job["jobTitle"], keep_whitespace=False))
    print("\n")
    if currSet==5:
        break
# text = "เมืองเชียงรายมีประวัติศาสตร์อันยาวนาน    i am a book    เป็นที่ตั้งของหิรัญนครเงินยางเชียงแสน"
# print("sent_tokenize:", sent_tokenize(text))
# print("word_tokenize:", word_tokenize(text))
# print("no whitespace:", word_tokenize(text, keep_whitespace=False))
