import json
import requests
import dbhandler


class PrepData:
    def __init__(self, db):
        self.db = db
        self.all_probs = self.get_all_probs()
        self.all_users = []
        self.profile = self.create_profile()
        self.prob_profile = self.create_prob_profile()

    def get_all_probs(self):
        query = "SELECT pid FROM problems WHERE 1"
        probs = dbhandler.parse_db(self.db, query)
        ret = []
        for p in probs:
            ret.append(int(p[0]))
        return ret

    def create_profile(self):
        query = "SELECT * FROM submissions WHERE 1"
        subs = dbhandler.parse_db(self.db, query)
        ret = dict()
        for s in subs:
            userid = int(s[1])

            if not userid in self.all_users:
                self.all_users.append(userid)

            problemid = int(s[3])
            verdict = int(s[5])
            try:
                temp = ret[userid, problemid]
            except:
                temp = dict()
                temp["solved"] = 0
                temp["tried"] = 0

            temp["tried"] += 1
            if verdict == 1:
                temp["solved"] = 1

            ret[userid, problemid] = temp
        return ret

    def create_prob_profile(self):
        ret = dict()
        for user in self.all_users:
            for prob in self.all_probs:

                try:
                    temp = ret[prob]
                except:
                    temp = dict()
                    temp["sp"] = 0
                    temp["nsp"] = 0
                    temp["tsp"] = 0
                    temp["tnsp"] = 0

                try:
                    prof = self.profile[user, prob]
                except:
                    prof = dict()
                    prof["solved"] = 0
                    prof["tried"] = 0

                if prof["solved"] == 1:
                    temp["sp"] += 1
                    temp["tsp"] += prof["tried"]
                elif prof["tried"] != 0:
                    temp["nsp"] += 1
                    temp["tnsp"] += prof["tried"]
                ret[prob] = temp
        return ret
