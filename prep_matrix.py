from prep_data import PrepData


class PrepMatrix:
    def __init__(self, db):
        self.u1 = 0
        self.u2 = 0
        self.p1 = 0
        self.p2 = 0
        self.data = PrepData(db)
        self.mat = self.get_final_matrix()

    def get_final_matrix(self):
        ret = dict()
        for user in self.data.all_users:
            for prob in self.data.all_probs:
                try:
                    p = self.data.profile[user, prob]
                    pp = self.data.prob_profile[prob]
                    try:
                        # try case : everybody solved the problem
                        th1 = int(pp["tnsp"] / pp["nsp"])
                    except:
                        th1 = 0
                    try:
                        # try case : nobody solved the problem
                        th2 = int(pp["tsp"] / pp["sp"])
                    except:
                        th2 = 0

                    if p["solved"] == 0 and p["tried"] >= th1:
                        ret[user, prob] = 1
                    elif p["solved"] == 0 and p["tried"] < th1:
                        ret[user, prob] = 2
                    elif p["solved"] == 1 and p["tried"] >= th2:
                        ret[user, prob] = 3
                        self.u1 += 1
                        self.p1 += 1
                    elif p["solved"] == 1 and p["tried"] < th2:
                        ret[user, prob] = 4
                        self.u2 += 1
                        self.p2 += 1
                except Exception as e:
                    ret[user, prob] = 0
                # print user, prob, ret[user, prob]

        for user in self.data.all_users:
            for prob in self.data.all_probs:
                if ret[user, prob] == 3:
                    if self.p2 >= 2 * self.p1 and self.u2 >= self.u1:
                        ret[user, prob] = 4
                elif ret[user, prob] == 4:
                    if self.p1 >= 2 * self.p2 and self.u1 >= self.u2:
                        ret[user, prob] = 3

        # for user in self.data.all_users:
        #     for prob in self.data.all_probs[:50]:
        #         print ret[user, prob],
        #     print "\n"
        return ret
