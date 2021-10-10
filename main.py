from wordCount import WordCount
from wordTokenize import WordTokenize
from getJobs import GetJobs

gt = GetJobs()
retrunCode = gt.getJobThai('jouThaiUsr01','jobpass','jobThai','jobList')

# wt = WordTokenize()
# wt.segWord('jouThaiUsr01','jobpass','jobThai','jobList','jobTitle','jobTitleWord',{'lastAct' : 'newAdded'})

# wdCount = WordCount('jouThaiUsr01','jobpass','jobThai','jobDetailWord','jobDetailWordCount',"wordJobDetail",'seqNum')
# wdCount.counting()