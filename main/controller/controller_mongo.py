from pymongo import MongoClient
import json


class CustomMongoConnect:
    def __init__(self, dbname, collname):
        self.conn = MongoClient(host="localhost", port=27017)
        self.db = self.conn[dbname]
        self.coll = self.db[collname]

    def display_all_docs(self):
        res = [doc for doc in self.coll.find()]
        print(res)

    def show_by_coach(self, coach):
        filter = {"Coach": coach.upper()}
        cursors = self.coll.find(filter)
        res = [doc for doc in cursors]
        res = json.dumps(res, default=str)
        return {"result": json.loads(res)}, 200

    def show_by_seat(self, coach, seat):
        filter = {"Coach": coach.upper(),"Seat ":seat}
        cursors = self.coll.find_one(filter)
        if cursors:
            return {"result":json.loads(json.dumps(cursors,default=str))}, 200
        else:
            return {"result":" Invalid error"}, 401


s = CustomMongoConnect("tthelper", "T16316")
s.show_by_seat("S2", "16")
