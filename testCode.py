from connectMongo import get_database

# connect db
dbname = get_database()
collectionJobList = dbname["jobList"]
jobId = collectionJobList.distinct('jobId')
print("jobId ",len(jobId))