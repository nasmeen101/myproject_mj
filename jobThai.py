from bs4 import BeautifulSoup
import re # library for regex in python
import requests
import io   # for write html to file
import os   # for fire path
import random   # for random test fetch data (only for test)

# global variable
jobIdArr = []
jobUrlArr = []
companyUrlArr = []
page = random.randint(1,76)
currJobId       = 0
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

url = "https://www.jobthai.com/%E0%B8%AB%E0%B8%B2%E0%B8%87%E0%B8%B2%E0%B8%99/%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%AD%E0%B8%A1%E0%B8%9E%E0%B8%B4%E0%B8%A7%E0%B9%80%E0%B8%95%E0%B8%AD%E0%B8%A3%E0%B9%8C-it-%E0%B9%82%E0%B8%9B%E0%B8%A3%E0%B9%81%E0%B8%81%E0%B8%A3%E0%B8%A1%E0%B9%80%E0%B8%A1%E0%B8%AD%E0%B8%A3%E0%B9%8C/"
url = url + str(page)

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
    for count, url in enumerate(jobUrlArr):
        print(count,url),    
        jobUrl = url
        resJob = requests.get(jobUrl)
        resJob.encoding = "utf-8"
        if resJob.status_code == 200:
            print(resJob," Successful")
        elif resJob.status_code == 404:
            print(resJob," Error 404 page not found")
        else:
            print(resJob,"Not both 200 and 404")
        if resJob.status_code == 200:
            # get job detail paage
            soupJob = BeautifulSoup(resJob.content, "html.parser")
            # save job detail page by jobId as html file
            fileName = "p" + str(page) + "_n" + str(((count+1)+(page-1)*20)) + "_jobId" + jobIdArr[count] + ".html"
            fileName = "\\jobDetail\\" + fileName
            fileName = os.getcwd()+fileName
            with io.open(fileName, "w", encoding="utf-8") as f:
                f.write(soupJob.prettify())

            # extract data
            if len(soupJob.find("h2"))>0:
                companyName = soupJob.find("h2").string
            if len(soupJob.find("h1"))>0:
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
            for valLi in posReqTagAll.find_all('li'):
                jobRequireArr.append(str(valLi.text))
            # print
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

            # stop loop for test
            if count == 0:
                break

    jobIdArr.clear()
    jobUrlArr.clear()
    companyUrlArr.clear()
    jobRequireArr.clear()

    
    