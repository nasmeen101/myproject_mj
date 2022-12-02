from wordCount import WordCount
from wordTokenize import WordTokenize
from getJobs import GetJobs

gt = GetJobs()
retrunCode = gt.getJobThai('jouThaiUsr01','jobpass','jobThai','jobList')

wt = WordTokenize()
wt.segWord('jouThaiUsr01','jobpass','jobThai','jobList' ,'jobTitle'
                                                        ,'jobTitleWord'
                                                        ,{'lastAct' : 'newAdded'})
wt.segWord('jouThaiUsr01','jobpass','jobThai','jobList' ,'jobDetail'
                                                        ,'jobDetailWord'
                                                        ,{'lastAct' : 'seg_jobTitle'})
wt.segWord('jouThaiUsr01','jobpass','jobThai','jobList' ,'jobRequire'
                                                        ,'jobRequireWord'
                                                        ,{'lastAct' : 'seg_jobDetail'})
wt.segWord('jouThaiUsr01','jobpass','jobThai','jobList' ,'jobDetail'
                                                        ,'jobDetailWord'
                                                        ,{"$or":[   {'lastAct' : 'newAdded'}, 
                                                                    {'lastAct' : 'seg_jobTitle'}
                                                                ]})
wt.segWord('jouThaiUsr01','jobpass','jobThai','jobList' ,'jobRequire'
                                                        ,'jobRequireWord'
                                                        ,{"$or":[   {'lastAct' : 'newAdded'}, 
                                                                    {'lastAct' : 'seg_jobTitle'},
                                                                    {'lastAct' : 'seg_jobDetail'}
                                                                ]})



wdCount = WordCount('jouThaiUsr01','jobpass','jobThai','jobDetailWord','jobDetailWordCount',"wordJobDetail",'seqNum')
wdCount.counting()