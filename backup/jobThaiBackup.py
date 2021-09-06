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
currJobId = 0
positionName    = "positionName tag not found"
companyName     = "companyName tag not found"
location        = "location tag not found"       # location-text
salary          = "salary tag not found"         # id="salary-text"
positionNum     = "positionNum tag not found"
positionDetail  = "positionDetail tag not found"
positionRequired = "positionRequired tag not found"
positionRequiredArr = []

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
    # soup = BeautifulSoup(res.text)
    #soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup.prettify())
    soup = BeautifulSoup(res.content, "html.parser")
    #result_by_class=soup.find_all("div", {"class": "ant-row msklqa-8 hQCzHL"})
    #work 
    #result_by_class=soup.find_all("div", class_="ant-row msklqa-8 hQCzHL")
    result_by_class=soup.find_all("a", id=re.compile('^job-'))
    for count, value in enumerate(result_by_class):
        m = re.search("job-(.+?)\"", str(value))
        #found = "0"
        if m:
            currJobId = m.group(1)
            #print("id found=",found,sep='\n')
            if currJobId.isnumeric():
                currJobUrl = preJobUrl + currJobId
                currComUrl = preCompanyUrl + currJobId
                jobIdArr.append(currJobId)
                jobUrlArr.append(currJobUrl)
                companyUrlArr.append(currComUrl)

        #print(count, value,sep='\n\n\n')
    jobLen = len(jobUrlArr)
    print("jobLen = ",jobLen,"\n")
    for count, url in enumerate(jobUrlArr):
        # count start with 0
        print(count,url)    
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
            soupJob = BeautifulSoup(resJob.content, "html.parser")
            # save jobdetail page by jobId as html file
            fileName = "p" + str(page) + "_n" + str(((count+1)+(page-1)*20)) + "_jobId" + jobIdArr[count] + ".html"
            fileName = "\\jobDetail\\" + fileName
            fileName = os.getcwd()+fileName
            with io.open(fileName, "w", encoding="utf-8") as f:
                f.write(soupJob.prettify())

            # extract data
            #result_by_h2=soup.find_all("h2", id="company-name-label")
            # result_by_h2=soup.find_all("a", id=re.compile('^job-')) "p", class_="strikeout body"
            # result_by_aJobId=soup.find_all("a", id="job-"+str(currJobId))
            if len(soupJob.find("h2"))>0:
                companyName = soupJob.find("h2").string
            if len(soupJob.find("h1"))>0:
                positionName = soupJob.find("h1").string 
            # work but use class more easier
            # if len(soupJob.find("h3",id="location-text"))>0:
            #     location = soupJob.find("h3",id="location-text").string
            # find salary
            # work but use class more easier
            # listJobSalary = soupJob.find_all("img", alt="number of positions icon")
            # for countJobSal, valueJobSal in enumerate(listJobSalary):
            #     print(countJobSal, valueJobSal.text)

            # work but not sure for len
            # listJobSalary = re.findall('<img alt="salary icon" height="20px" src="/static/images/salary-no-margin.png"/>(.+?)</div>', str(soupJob))
            # if len(listJobSalary)>=1:
            #     salary = listJobSalary[1]

            # find number of position
            #posTagAll = soupJob.find_all("img", alt="number of positions icon")
            locSalPosNumTagAll = soupJob.find_all("div",  {"class":"ant-col sc-1048v4y-2 fTmuAP ant-col-xs-24 ant-col-sm-24 ant-col-md-24 ant-col-lg-24 ant-col-xl-18"})
            for countLocSalPos, valueLocSalPos in enumerate(locSalPosNumTagAll):
                #print(countPos, valuePos.text)
                if countLocSalPos == 0:
                    location = str(valueLocSalPos.text)
                elif countLocSalPos == 1:
                    salary = str(valueLocSalPos.text)
                else:
                    positionNum = str(valueLocSalPos.text)
                # if countPos==1:
                #     positionNum = str(valuePos.text)
            # posAll = soupJob.find_all("img", alt="number of positions icon") # found but can't access data
            # ---- work but not sure for check len
            # posTagAll = re.findall('<img alt="number of positions icon" src="/static/images/user-no-margin.png"/>(.+?)</div>', str(soupJob))
            # if len(posTagAll)>=1:
            #     positionNum = posTagAll[1]

            # find position details
            # posDetTagAll = re.findall('<span style="white-space:pre-line">(.+?)</span>', str(soupJob)) # can't catch multiple line
            posDetTagAll = soupJob.find_all("span", style="white-space:pre-line")
            for countDet, valueDet in enumerate(posDetTagAll):
                if countDet==0:
                    positionDetail = str(valueDet.text)

            # find jor requirment
            posReqTagAll = soupJob.find("div", {"class":"jltwsh-0 gkuvRx"})
            for valLi in posReqTagAll.find_all('li'):
                # print(valLi.text)
                positionRequiredArr.append(str(valLi.text))
            # for countPosReq, valuePosReq in enumerate(posReqTagAll):
            #     if countPosReq==0:
            #         positionRequired = str(valuePosReq.text)
            
            # print
            print("\n")
            print("Extracted data page = "  ,page)
            print("positionName = "         ,positionName) 
            print("companyName = "          ,companyName)
            print("location = "             ,location)
            print("salary = "               ,salary)
            print("positionNum = "          ,positionNum)
            print("positionDetail = "       ,positionDetail)
            print("positionRequired = ")
            print(*positionRequiredArr, sep='\n')   

            # result_by_aJobId=soup.find("a", id="job-"+str(jobIdArr[count]))
            # result_by_h2 = result_by_aJobId.find_all("h2")
            # for countH2, valueH2 in enumerate(result_by_h2):
            #     print(countH2, valueH2.string,sep='\n\n\n')
            #print(soup.prettify())



            # stop loop for test
            if count == 0:
                break


    jobUrlArr.clear();
    companyUrlArr.clear();

    #print(result_by_class)
    #for id_link_info, value_link_info in enumerate(result_by_class):
        #print(f"#{id_link_info}\t{value_link_info}")

    #bs = BeautifulSoup(res.content, "html.parser")
    #print(bs.prettify())
    #result_by_class=bs.select("a[class*=DvvsL]")
    
    