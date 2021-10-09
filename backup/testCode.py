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
# collectionJobList.update_many({},{'$rename':{"timeStamp":"timestamp"}})
collectionJobList.update_many({},{ '$set': {'lastAct':'newAdded'}}) 

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