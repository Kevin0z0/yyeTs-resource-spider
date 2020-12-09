import pymongo
import sys
class DB:
    def __init__(self, data):
        account = "{}:{}@".format(data['username'], data['password']) if len(data['username']) > 0 else ""
        try:
            self.db = pymongo.MongoClient("mongodb://{}{}:{}".format(account, data["host"], data["port"]))
            mydb = self.db[data["dbname"]]
            self.mycol = mydb[data["table"]]
        except Exception as e:
            print(e)
            sys.exit(0)
    def insert(self, result):
        self.mycol.insert_one(result)

    def __exit__(self):
        self.db.close()