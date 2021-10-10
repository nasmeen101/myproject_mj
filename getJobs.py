class GetJobs:
    def __init__(self):
        """
        """

    def getJobThai(self, dbUsr, dbPass, dbName,dstCollName):
        """
        get jobs from jobTahi 
        query filter for new job -> {'lastestAction' : 'newAdded'}
        :param dbUsr: database user name
        :param dbPass: database password
        :param dbName: database name
        :param dstCollName: distination collection name for save job deatils
        return value
        0 ok
        -1 can't get last page
        -2 job list page error: 400 page not found
        -3 job list page error: not 200 or 400
        -4 job detail page error: 400 page not found
        -5 job detail page error: not 200 or 400
        """
        
        from bs4 import BeautifulSoup
        import re       # library for regex in python
        import requests
        import io       # for write html to file
        import os       # for fire path
        import random   # for random test fetch data (only for test)
        import time     # for delay
        import json     # for convert jobRequireArr to json
        from connectMongo import get_database
        from datetime import datetime

        # connect to db
        CONNECTION_STRING = "mongodb://"+dbUsr+":"+dbPass+"@t2u-th.com/"+dbName
        from pymongo import MongoClient
        client = MongoClient(CONNECTION_STRING)
        db = client[dbName]
        dbCollection = db[dstCollName]

        # global variable
        isDebugMode = False
        jobIdArr = []
        jobUrlArr = []
        companyUrlArr = []
        page = 1 #random.randint(1,76)
        currJobId       = 0
        countNewAdded   = 0
        jobTitle        = "jobTitle tag not found"
        companyName     = "companyName tag not found"
        location        = "location tag not found"       
        salary          = "salary tag not found"        
        jobNum          = "jobNum tag not found"
        jobDetail       = "jobDetail tag not found"
        jobRequire      = "jobRequire tag not found"
        jobRequireArr   = []

        preJobUrl = "https://www.jobthai.com/th/job/"
        preCompanyUrl = "https://www.jobthai.com/th/company/job/"

        startPage = 1
        lastPage = self.getJobThaiLastPage()
        if lastPage == -1:
            # can't get last page tag
            return -1
        for x in range(lastPage):
            page = x+startPage
            #page = random.randint(1,76)
            url = "https://www.jobthai.com/%E0%B8%AB%E0%B8%B2%E0%B8%87%E0%B8%B2%E0%B8%99/%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%AD%E0%B8%A1%E0%B8%9E%E0%B8%B4%E0%B8%A7%E0%B9%80%E0%B8%95%E0%B8%AD%E0%B8%A3%E0%B9%8C-it-%E0%B9%82%E0%B8%9B%E0%B8%A3%E0%B9%81%E0%B8%81%E0%B8%A3%E0%B8%A1%E0%B9%80%E0%B8%A1%E0%B8%AD%E0%B8%A3%E0%B9%8C/"
            url = url + str(page)

            print(url, end =" " )
            res = requests.get(url)
            res.encoding = "utf-8"
            if res.status_code == 200:
                print("Successful")
            elif res.status_code == 404:
                print("Error 404 page not found")
                return -2
            else:
                print("Not both 200 and 404")
                return -3
            if res.status_code == 200:
                # get job list page
                soup = BeautifulSoup(res.content, "html.parser")
                result_by_class=soup.find_all("a", id=re.compile('^job-'))
                # extarct job-id in page
                for count, value in enumerate(result_by_class):
                    m = re.search("job-(.+?)\"", str(value))
                    if m:
                        currJobId = m.group(1)
                        if currJobId.isnumeric():
                            currJobUrl = preJobUrl + currJobId
                            currComUrl = preCompanyUrl + currJobId
                            # generate company link and job detail link
                            jobIdArr.append(currJobId)          # job id
                            jobUrlArr.append(currJobUrl)        # job detail url
                            companyUrlArr.append(currComUrl)    # company detail url
                # access each job detail url
                print("page ",page, " has ", len(jobUrlArr), " jobs")
                for countJob, valJobUrl in enumerate(jobUrlArr):
                    print(countJob,valJobUrl, end =" ")    

                    # check existing data in db first
                    if dbCollection.count_documents({"jobId":str(jobIdArr[countJob])})>0:
                        # skip existing data
                        print("jobId : ",str(jobIdArr[countJob])," exist. Go next job id")
                        continue

                    #jobUrl = url
                    resJob = requests.get(valJobUrl)
                    resJob.encoding = "utf-8"
                    if resJob.status_code == 200:
                        print(resJob," Successful")
                    elif resJob.status_code == 404:
                        print(resJob," Error 404 page not found")
                        return -4
                    else:
                        print(resJob,"Not both 200 and 404")
                        return -5
                    if resJob.status_code == 200:
                        # get job detail paage
                        soupJob = BeautifulSoup(resJob.content, "html.parser")

                        # extract data
                        if not(soupJob.find("h2") is None):
                            companyName = soupJob.find("h2").string
                        if not(soupJob.find("h1") is None):
                            jobTitle = soupJob.find("h1").string 

                        # find locatio, salary ,number of position
                        locSalPosNumTagAll = soupJob.find_all("div",  {"class":"ant-col sc-1048v4y-2 fTmuAP ant-col-xs-24 ant-col-sm-24 ant-col-md-24 ant-col-lg-24 ant-col-xl-18"})
                        for countLocSalPos, valueLocSalPos in enumerate(locSalPosNumTagAll):
                            if countLocSalPos == 0:
                                location = str(valueLocSalPos.text)
                            elif countLocSalPos == 1:
                                salary = str(valueLocSalPos.text)
                            else:
                                jobNum = str(valueLocSalPos.text)

                        # find job details
                        posDetTagAll = soupJob.find_all("span", style="white-space:pre-line")
                        for countDet, valueDet in enumerate(posDetTagAll):
                            if countDet==0:
                                jobDetail = str(valueDet.text)

                        # find jor requirment
                        posReqTagAll = soupJob.find("div", {"class":"jltwsh-0 gkuvRx"})
                        if not(posReqTagAll is None): # avoid no tag found
                            liTagAll = posReqTagAll.find_all('li')
                            if not(liTagAll is None): # avoid no tag found
                                for valLi in liTagAll:
                                    jobRequireArr.append(str(valLi.text))

                        # verify data before add to db
                        isHasAllData = True
                        if jobTitle         == "jobTitle tag not found":
                            isHasAllData = False
                            print(" ", jobTitle),
                        if companyName      == "companyName tag not found":
                            isHasAllData = False
                            print(" ", companyName),
                        if location         == "location tag not found":  
                            isHasAllData = False    
                            print(" ", location),
                        if salary           == "salary tag not found":    
                            isHasAllData = False    
                            print(" ", salary),
                        if jobNum           == "jobNum tag not found":
                            isHasAllData = False
                            print(" ", jobNum),
                        if jobDetail        == "jobDetail tag not found":
                            isHasAllData = False
                            print(" ", jobDetail),
                        if len(jobRequireArr)       == 0:
                            isHasAllData = False
                            print(" ", jobRequire),
                        
                        if isHasAllData == True:
                            # save to db
                            jobDetail2Db = {
                                'dataOwner'     : 'jobThai',
                                "jobId"         : str(jobIdArr[countJob]),
                                "jobUrl"        : str(jobUrlArr[countJob]),
                                "companyUrl"    : str(companyUrlArr[countJob]),
                                "jobTitle"      : str(jobTitle),
                                "companyName"   : str(companyName),
                                "location"      : str(location),
                                "salary"        : str(salary),
                                "jobNum"        : str(jobNum),
                                "jobDetail"     : str(jobDetail),
                                "jobRequire"    : json.loads(json.dumps(jobRequireArr)),
                                'lastAct'       : 'newAdded',
                                "updateDate"    : datetime.today().replace(microsecond=0),
                                "createDate"    : datetime.today().replace(microsecond=0)
                            }
                            dbCollection.insert_one(jobDetail2Db)
                            countNewAdded = countNewAdded+1

                            # delay before fetch new job detail
                            delayBetweenJob = random.randint(10,30)
                            print("job added (delay ", delayBetweenJob, " sec)")
                            time.sleep(delayBetweenJob)
                            
                            if isDebugMode == True:
                                # print test
                                print("\n")
                                print("Extracted data page = "  ,page)
                                print("jobTitle = "             ,jobTitle) 
                                print("companyName = "          ,companyName)
                                print("location = "             ,location)
                                print("salary = "               ,salary)
                                print("jobNum = "               ,jobNum)
                                print("jobDetail = "            ,jobDetail)
                                print("jobRequire = ")
                                print(*jobRequireArr, sep='\n')   
                        else:
                            print(" some data missing, skip this job")
                            # save job detail page by jobId as html file
                            fileName = "p" + str(page) + "_n" + str(((countJob+1)+(page-1)*20)) + "_jobId" + jobIdArr[countJob] + ".html"
                            fileName = "\\jobDetail4debug\\" + fileName
                            fileName = os.getcwd()+fileName
                            with io.open(fileName, "w", encoding="utf-8") as f:
                                f.write(soupJob.prettify())

                        if isDebugMode == True:
                            # stop loop for test
                            if count == 1:
                                break
                    # end job fetch loop
                # clear array
                jobIdArr.clear()
                jobUrlArr.clear()
                companyUrlArr.clear()
                jobRequireArr.clear()
            if countNewAdded == 0:
                # no new job added in this page so add some delay
                delayNoNewJob = random.randint(10,30)
                print("No new job found (delay ", delayNoNewJob, " sec)")
                time.sleep(delayNoNewJob)
            print("page ", page, " / add new ", countNewAdded, " jobs")
            countNewAdded = 0

            # stop loop if last page reached
            if page == lastPage:
                break
        # get job complete
        print("----- Get jobThai Done -----")
        return 0

    def getJobThaiLastPage(self):
        import requests
        from bs4 import BeautifulSoup
        import io       # for write html to file
        import os       # for fire path
        url = "https://www.jobthai.com/%E0%B8%AB%E0%B8%B2%E0%B8%87%E0%B8%B2%E0%B8%99/%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%AD%E0%B8%A1%E0%B8%9E%E0%B8%B4%E0%B8%A7%E0%B9%80%E0%B8%95%E0%B8%AD%E0%B8%A3%E0%B9%8C-it-%E0%B9%82%E0%B8%9B%E0%B8%A3%E0%B9%81%E0%B8%81%E0%B8%A3%E0%B8%A1%E0%B9%80%E0%B8%A1%E0%B8%AD%E0%B8%A3%E0%B9%8C/"

        print(url, end =" " )
        res = requests.get(url)
        res.encoding = "utf-8"
        if res.status_code == 200:
            print("Successful")
        elif res.status_code == 404:
            print("Error 404 page not found")
        else:
            print("Not both 200 and 404")
        if res.status_code == 200:
            # get job list page
            soup = BeautifulSoup(res.content, "html.parser")
            a = soup.find("a", {"id": "last-button"})
            if not(a is None):
                size = len(a['href'])
                pageNumList = [a['href'][size-1]]
                curIndex = size-2
                curCh = a['href'][curIndex]
                while curCh != '=' and curIndex>=0:
                    pageNumList.append(curCh)
                    curIndex = curIndex-1
                    curCh = a['href'][curIndex]
                reverseP = pageNumList[::-1]
                page = ""
                return int(page.join(reverseP))
            
                # save job detail page by jobId as html file
                # fileName = "p1.html"
                # fileName = "\\jobDetail4debug\\" + fileName
                # fileName = os.getcwd()+fileName
                # with io.open(fileName, "w", encoding="utf-8") as f:
                #     f.write(soup.prettify())
            else:
                print("Last page tag not found")
                return -1