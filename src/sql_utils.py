#!/usr/bin/python
import sqlite3
import os, platform
from encrypt_utils import EncryptUtils

FILE_PROTOCOL="file://"
FILE_NAME='/pdfViewer.db'
CONFIG_FOLDER_NAME='/.dange-pdf'

if (platform.system() == 'Linux' or platform.system() == 'Darwin'):
    if not os.path.exists(os.path.expanduser('~')+ CONFIG_FOLDER_NAME):
        os.makedirs(os.path.expanduser('~')+ CONFIG_FOLDER_NAME)
    databaseFile=os.path.expanduser('~')+ CONFIG_FOLDER_NAME + FILE_NAME
elif platform.system() == 'Windows':
    if not os.path.exists(os.path.expandvars(R"% HOMEPATH %")+ CONFIG_FOLDER_NAME):
        os.makedirs(os.path.expandvars(R"% HOMEPATH %")+ CONFIG_FOLDER_NAME)
    databaseFile=os.path.expandvars(R"% HOMEPATH %")+ CONFIG_FOLDER_NAME + FILE_NAME
else:
    pass

#databaseFile='.dange-pdf/test-pdfviewer.db'

class SqlUtils():

    def __init__(self):
        if os.path.exists(databaseFile):
            self.databseFile=databaseFile
            self.encrypt_utils=EncryptUtils()
        else:
            self.databseFile=databaseFile
            self.create_tables()
            self.encrypt_utils=EncryptUtils()


    def create_tables(self):
        '''Creates tables FILE and PATTERN if they dont exists in database'''

        print(self.databseFile)
        conn = sqlite3.connect(self.databseFile)

        conn.execute('''CREATE TABLE if not exists PATTERN 
                (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
                PATTERN         TEXT    NOT NULL UNIQUE,
                PASSWORD        BLOB    NOT NULL
                );''')

        conn.execute('''CREATE TABLE if not exists FILE
                (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
                FILENAME         TEXT    NOT NULL UNIQUE,
                PASSWORD        BLOB    NOT NULL
                );''')
        conn.close()


    def drop_tables(self):
        '''Drops the tables FILE and PATTERN in the Database '''

        conn = sqlite3.connect(self.databseFile)

        conn.execute('''DROP TABLE if exists PATTERN;''')
        conn.execute('''DROP TABLE if exists FILE;''')

        conn.close()

    def insert_into_file(self, filename,password):
        conn = sqlite3.connect(self.databseFile)
        password_encrypted=self.encrypt_utils.encrypt(password)
        query_string="INSERT INTO FILE (FILENAME,PASSWORD) VALUES (? , ?)"
        try:
            data_tuple = (filename, password_encrypted)
            conn.execute(query_string,data_tuple)
            conn.commit()
            print("Records inserted successfully")
            conn.close()
        except sqlite3.IntegrityError:
            print("Filename already exists in database. Ignoring")


    def get_all_files_data(self):
        conn = sqlite3.connect(self.databseFile)
        dict= {}
        cursor = conn.execute("SELECT id, FILENAME, PASSWORD from FILE")
        for row in cursor:
            dict[row[1]] = row[2]
        
        conn.close()
        return dict

    def get_all_filenames(self):
        conn = sqlite3.connect(self.databseFile)
        list= []
        cursor = conn.execute("SELECT FILENAME from FILE")
        for row in cursor:
            list.append(row[0])
        
        conn.close()
        return list


    def get_password_for_file(self,filename):
        conn = sqlite3.connect(self.databseFile)
        query_string="SELECT PASSWORD from FILE where filename ='" + filename + "\'"
    
        result = []
        cursor = conn.execute(query_string)
        for row in cursor:
            result.append(row[0])
        
        conn.close()

        if result:
            return self.encrypt_utils.decrypt(result[0])
        else:
            return None


    def insert_into_pattern(self, pattern,password):
        conn = sqlite3.connect(self.databseFile)
        password_encrypted=self.encrypt_utils.encrypt(password)
        query_string="INSERT INTO PATTERN (PATTERN,PASSWORD) VALUES (?, ?)"
        try:
            data_tuple = (pattern, password_encrypted)
            conn.execute(query_string, data_tuple)
            conn.commit()
            print("Records inserted successfully")
            conn.close()
        except sqlite3.IntegrityError:
            print("Pattern already exists in database. Ignoring")


    def get_all_patterns_data(self):
        conn = sqlite3.connect(self.databseFile)
        dict= {}
        cursor = conn.execute("SELECT id, PATTERN, PASSWORD from PATTERN")
        for row in cursor:
            dict[row[1]] = row[2]
        
        conn.close()
        return dict

    def get_all_patterns(self):
        conn = sqlite3.connect(self.databseFile)
        list= []
        cursor = conn.execute("SELECT PATTERN from PATTERN")
        for row in cursor:
            list.append(row[0])
        
        conn.close()
        return list

    def get_password_for_pattern(self,pattern):
        conn = sqlite3.connect(self.databseFile)
        query_string="SELECT PASSWORD from PATTERN where pattern ='" + pattern + "\'"
    
        result = []
        cursor = conn.execute(query_string)
        for row in cursor:
            result.append(row[0])
        
        conn.close()

        if result:
            return self.encrypt_utils.decrypt(result[0])
        else:
            return None


def test_sql_utils():
    sql_utils=SqlUtils()
    sql_utils.drop_tables()
    sql_utils.create_tables()
    sql_utils.insert_into_file('Statement_2022MTH01_140526881.pdf', 'abc123')
    print(sql_utils.get_all_files_data())
    result = sql_utils.get_password_for_file('Statement_2022MTH01_140526881.pdf')
    if result is not None:
        print(result)

    sql_utils.insert_into_pattern('Statement_*.pdf', 'abc123')
    sql_utils.insert_into_pattern('*Statement_2022MTH0*.pdf', 'abc123')
    sql_utils.insert_into_pattern('*Tanmay_Mukund_Dange_*.pdf', 'abc123')

    # Printing all Patterns in the database
    for pat in sql_utils.get_all_patterns():
        print(pat)

    # Fetching Password for a given pattern
    result = sql_utils.get_password_for_pattern('Statement_*.pdf')
    if result is not None:
        print(result)
    
if __name__ == "__main__":
    test_sql_utils()