import MySQLdb


def connect_db_judged(host_ip,username,password,dbName):
    try:
        if password=="null":
            password=""
        db = MySQLdb.connect(host_ip,username,password, dbName)
        return db
    except Exception as e:
        print "Exception : ", e
        return None


def disconnect_db_judge(db):
    db.close()


def parse_db(db, query):
    try:
        cursor = db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print "Exception : ", e
        return None


def update_db(db, query):
    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        return "success"
    except Exception as e:
        db.rollback()
        print "Exception : ", e
        return "failed"
