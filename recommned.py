from prep_matrix import PrepMatrix
from operator import itemgetter
import os
import dbhandler
from terminaltables import SingleTable


class bcolors:
    CYAN = '\033[96m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Recommend:
    def __init__(self, db, uid):
        self.uid = uid
        self.mat_data = PrepMatrix(db)
        self.similarity = self.get_sim_list(self.uid)
        self.rec_prob = self.get_rec_probs(self.uid)

    def get_sim_list(self, uid):
        all_users = self.mat_data.data.all_users
        all_probs = self.mat_data.data.all_probs
        matrix = self.mat_data.mat
        ret = []
        for user in all_users:
            sxu = 0
            dxu = 0
            if user == uid:
                continue
            for prob in all_probs[:50]:
                if matrix[user, prob] == matrix[uid, prob] and matrix[uid, prob] != 0:
                    sxu += 1
                elif matrix[user, prob] != 0 or matrix[uid, prob] != 0:
                    dxu += 1
            # print user, prob, ":", sxu, dxu
            # ads = raw_input()
            try:
                s = sxu * 1.0 / dxu
            except Exception as e:
                s = 0
            temp = dict()
            temp["user"] = user
            temp["sim"] = s
            ret.append(temp)
        ret = sorted(ret, key=itemgetter('sim'), reverse=True)
        return ret

    def get_rec_probs(self, uid):
        all_probs = self.mat_data.data.all_probs
        matrix = self.mat_data.mat
        ret = []
        for p in all_probs:
            pscore = 0
            if matrix[uid, p] >= 3:
                continue
            for s in self.similarity[:3]:
                tm = matrix[s["user"], p]
                if tm < 3:
                    tm = 0
                else:
                    tm = 1
                pscore += s["sim"] * tm
            temp = dict()
            temp["pid"] = p
            temp["pscore"] = pscore
            ret.append(temp)
        ret = sorted(ret, key=itemgetter('pscore'), reverse=True)
        # print ret[:3]
        return ret[:3]


def main():
    db = dbhandler.connect_db_judged(
        "127.0.0.1", "root", "sustcse", "uva_crawler")
    os.system("clear")
    print bcolors.BOLD + bcolors.HEADER + "                  Problem Recomendation system for SourceCode" + bcolors.ENDC + "\n"
    while True:
        p = raw_input("Type user_id or exit : ")
        # os.system("clear")
        print "\n"
        if p == "exit":
            break
        obj = Recommend(db, int(p))
        data = [[bcolors.WARNING+"pid"+bcolors.ENDC,bcolors.WARNING+"Title"+bcolors.ENDC]]
        for p in obj.rec_prob:
            query = "SELECT name FROM problems WHERE pid=" + str(p["pid"])
            pname = dbhandler.parse_db(db, query)
            temp = [p["pid"],pname[0][0]]
            data.append(temp)
        table = SingleTable(data)
        table.inner_row_border = True
        table.justify_columns={1:"center"}
        print bcolors.CYAN + "Recommended problems : " + bcolors.ENDC
        print table.table
        print "\n"
    dbhandler.disconnect_db_judge(db)


if __name__ == '__main__':
    main()
