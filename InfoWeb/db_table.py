import mysql.connector

'''
    Basic Wrapper of MySQL Database
'''

class db_table:
    def __init__(self, serverName = "localhost", dbUserName = "root", pwd = "********", dbName = "TrojanTech"):
        self.serverName = serverName
        self.dbUserName = dbUserName
        self.pwd = pwd
        self.dbName = dbName
        self.db = mysql.connector.connect(
            host = self.serverName, 
            user = self.dbUserName, 
            password = self.pwd,
            database = self.dbName
        )

    def connect(self):
        self.db = mysql.connector.connect(
            host = self.serverName, 
            user = self.dbUserName, 
            password = self.pwd,
            database = self.dbName
        )
    
    def create(self, sql):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            print("Table Create Successfully!")
        except:
            print("Table Create Unsuccessfully!")

    def insert(self, sql):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
            print("Insert Successfully!")
        except:
            self.db.rollback()

    def select(self, sql):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except:
            print("Error: unable to fetch data")
    
    def close(self):
        self.db.close()

def main():
    db = db_table()
    create_Employee_Table = """
    CREATE TABLE EMPLOYEE (
        EID INT AUTO_INCREMENT PRIMARY KEY,
        ENAME VARCHAR(64) NOT NULL,
        MAC VARCHAR(32),
        IP VARCHAR(32) NOT NULL,
        DEVICE VARCHAR(32) NOT NULL
    )
    """
    db.create(create_Employee_Table)
    create_Record_Table = """
    CREATE TABLE CLOCKRECORDS (
        RID INT AUTO_INCREMENT PRIMARY KEY,
        EID INT NOT NULL,
        CHECKPOINT INT NOT NULL,
        RDATE DATE NOT NULL,
        STATUS INT NOT NULL,
        FOREIGN KEY (EID) REFERENCES EMPLOYEE (EID) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """
    db.create(create_Record_Table)
    db.close()


if __name__ == "__main__":
    main()