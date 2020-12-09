import pymysql
import sys
from time import sleep
class DB:
    def __init__(self, data):
        try:
            self.db = pymysql.connect(data["host"], data["username"], data["password"], data["dbname"])
            self.cursor = self.db.cursor()
            self.__tableName = data["table"]
            self.__table_exists()
        except Exception as e:
            print(e)
            sys.exit(0)

    def __detect_tables(self, name):
        query = "show tables;"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        for i in tables:
            if name == i[0]:
                return False
        return True

    def __table_exists(self):
        if self.__detect_tables(self.__tableName):
            self.createTable()
            print("已创建数据表")

    def __execute(self,query):
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(query)
            self.db.commit()
        except Exception as e:
            if "PRIMARY" in str(e):
                return
            sleep(2)
            self.__execute(query)

    def createTable(self):
        query = f"""
        CREATE TABLE {self.__tableName}(
            level char(3),
            region varchar(10),
            title varchar(50) not null,
            dramaType varchar(10),
            type varchar(30),
            company varchar(40),
            imgurl varchar(150),
            rank int,
            url varchar(100) not null primary key,
            score varchar(4),
            introduction text,
            translator varchar(100),
            actors varchar(1000),
            formerName varchar(100),
            alias varchar(100),
            screenwriter varchar(500),
            imdb varchar(100),
            premiereDate int,
            language varchar(20),
            directors varchar(300)
        )
        """
        self.cursor.execute(query)

    def insert(self, val):
        args = []
        result = []
        for i in val:
            v = val[i]
            if not v: continue
            args.append(i)
            result.append(str(v) if isinstance(v, int) else "'{}'".format(str(v).replace("'","''").replace("\\","\\\\")))
        query = f"INSERT INTO {self.__tableName} ({','.join(args)}) VALUES ({','.join(result)})"
        # print(query)
        self.__execute(query)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()