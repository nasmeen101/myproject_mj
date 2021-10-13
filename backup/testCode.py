from datetime import datetime

def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"
    # mongodb://jouThaiUsr01:jobpass@t2u-th.com:27017/?authSource=jobThai&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false
    CONNECTION_STRING = "mongodb://jouThaiUsr01:jobpass@t2u-th.com/jobThai"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['jobThai']

# connect db
dbname = get_database()
collectionJobList = dbname["jobList"]
# collectionJobList.update_many({},{'$rename':{"timeStamp":"createDate"}})
collectionJobList.update_many({},{ '$set': {'lastAct':'seg_jobDetail'}}) 
# collectionJobList.update_many({},{ '$set': {'updateDate':datetime.today().replace(microsecond=0)}})
# jobPerLoop  = 3  
# jobs = collectionJobList.find(
#         {"$or": [   {'lastAct' : 'newAdded'}, 
#                     {'lastAct' : 'seg_jobTitle'},
#                     {'lastAct' : "seg_jobDetail"}
#                 ]},  
#         {'jobId':1,'jobRequire':1,'jobTitle':1, '_id':0},
#         0,
#         jobPerLoop)
# for job in jobs:
#     print('r ',isinstance( job['jobRequire'], list))
#     print('t ',isinstance( job['jobTitle'], list))
#     # for r in job['jobRequire']:
#     #     print(r)

# collectionJobTitleWord = dbname["jobTitleWord"]
# collectionJobTitleWord.update_many({},{'$rename':{"timestamp":"createDate"}})
# collectionJobTitleWord.update_many({},{ '$set': {'updateDate':datetime.today().replace(microsecond=0)}}) 

# dbname = get_database()
# collectionJobList = dbname["jobTitleWord"]
# tWlist = collectionJobList.distinct('jobId')
# print(len( list(tWlist) ))

# update(
#   {},
#    },
#   false,
#   true
# )

# collectionJobList.update(
#   {},
#   { '$set': {'lastestAction':'N/S'} },
#   false,
#   true
# )

# collectionJobList.insert_many({'lastestAction':'N/S'})
# jobId = collectionJobList.distinct('jobId')
# print("jobId ",len(jobId))