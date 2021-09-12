# technicalWords

# job titles
itSupport   = [ "IT Support" ]
fullStack   = [ "full stack", "Full Stack", "Fullstack", "Full stack", "Full-Stack", "Full-Stacked",
                "FullStack"]
frontEnd    = [ "Frontend","Front – end", "Front-end",  "Front end" ]
backEnd     = [ "Backend" ,"Back - end",  "Back-end",   "Back end"]
programmer  = [ "Programmer", "Programmers", "โปรแกรมเมอร์"]
sysAnalyst  = [ "System Analyst", "system analyst", "วิเคราะห์ระบบ" ]
dataAnalyst = [ "Data Analyst", "Data Scientist", "data analyst", "data scientist", "วิเคราะห์ข้อมูล"]
busAnalyst  = [ "Business Analyst", "business analyst"]                
progAnalyst = [ "Programmer Analyst", "programmer analyst", "วิเคราะห์โปรแกรม", "วิเคราะห์แอปพลิเคชัน"]  
softAnalyst = [ "Software Analyst", "software analyst", "SAP Support Analyst",
                "Technical Analyst", "technical analyst", "IT Analyst"]               
secAnalyst  = [ "Security Analyst", "security analyst", "Cyber Security", "cyber security"]  

jobSet1 = itSupport + fullStack + frontEnd + backEnd + programmer
jobSet2 = sysAnalyst + dataAnalyst + busAnalyst + progAnalyst + softAnalyst +secAnalyst 
jobAll  = jobSet1 + jobSet2

# programming languages
langCpp = [ "C++", "c++" ]
langCsh = [ "C#", "c#" ]
langNet = [ ".net", ".NET", ".Net" ]
webFw   = [ "React"]
crossPf = [ "Angular", "Flutter"]
langAll = langCpp + langCsh + langNet + webFw + crossPf

customWords = jobAll + langAll
