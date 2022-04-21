#!/usr/bin/python
import sqlite3
import os

from encrypt_utils import decode_key_from_json, decrypt, encrypt, load_settings_from_json

FILE_PROTOCOL="file://"
FILE_NAME='/pdfViewer.db'
databseFile=FILE_PROTOCOL+os.path.expanduser('~')+ FILE_NAME
databseFile='test-pdfviewer.db'


def create_tables():
    '''Creates tables FILE and PATTERN if they dont exists in database'''

    conn = sqlite3.connect(databseFile)

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


def drop_tables():
    '''Drops the tables FILE and PATTERN in the Database '''

    conn = sqlite3.connect(databseFile)

    conn.execute('''DROP TABLE if exists PATTERN;''')
    conn.execute('''DROP TABLE if exists FILE;''')

    conn.close()

def insert_into_file(filename,password):
    conn = sqlite3.connect(databseFile)
    password_encrypted=encrypt_password(password)
    query_string="INSERT INTO FILE (FILENAME,PASSWORD) VALUES (? , ?)"
    try:
        data_tuple = (filename, password_encrypted)
        conn.execute(query_string,data_tuple)
        conn.commit()
        print("Records inserted successfully")
        conn.close()
    except sqlite3.IntegrityError:
        print("Filename already exists in database. Ignoring")


def get_all_files_data():
    conn = sqlite3.connect(databseFile)
    dict= {}
    cursor = conn.execute("SELECT id, FILENAME, PASSWORD from FILE")
    for row in cursor:
        dict[row[1]] = row[2]
     
    conn.close()
    return dict

def get_all_filenames():
    conn = sqlite3.connect(databseFile)
    list= []
    cursor = conn.execute("SELECT FILENAME from FILE")
    for row in cursor:
        list.append(row[0])
     
    conn.close()
    return list


def get_password_for_file(filename):
    conn = sqlite3.connect(databseFile)
    query_string="SELECT PASSWORD from FILE where filename ='" + filename + "\'"
 
    result = []
    cursor = conn.execute(query_string)
    for row in cursor:
        result.append(row[0])
    
    conn.close()

    if result:
        return decrypt_password(result[0])
    else:
        return None


def encrypt_password(plaintext_password):
    settings = load_settings_from_json()
    key = decode_key_from_json(settings["key"])
    iv = settings["iv"]
    return encrypt(plaintext_password,key,iv)

def decrypt_password(ciphertext_password):
    settings = load_settings_from_json()
    key = decode_key_from_json(settings["key"])
    iv = settings["iv"]
    return decrypt(ciphertext_password,key,iv)


def insert_into_pattern(pattern,password):
    conn = sqlite3.connect(databseFile)
    password_encrypted=encrypt_password(password)
    query_string="INSERT INTO PATTERN (PATTERN,PASSWORD) VALUES (?, ?)"
    try:
        data_tuple = (pattern, password_encrypted)
        conn.execute(query_string, data_tuple)
        conn.commit()
        print("Records inserted successfully")
        conn.close()
    except sqlite3.IntegrityError:
        print("Pattern already exists in database. Ignoring")


def get_all_patterns_data():
    conn = sqlite3.connect(databseFile)
    dict= {}
    cursor = conn.execute("SELECT id, PATTERN, PASSWORD from PATTERN")
    for row in cursor:
        dict[row[1]] = row[2]
     
    conn.close()
    return dict

def get_all_patterns():
    conn = sqlite3.connect(databseFile)
    list= []
    cursor = conn.execute("SELECT PATTERN from PATTERN")
    for row in cursor:
        list.append(row[0])
     
    conn.close()
    return list

def get_password_for_pattern(pattern):
    conn = sqlite3.connect(databseFile)
    query_string="SELECT PASSWORD from PATTERN where pattern ='" + pattern + "\'"
 
    result = []
    cursor = conn.execute(query_string)
    for row in cursor:
        result.append(row[0])
    
    conn.close()

    if result:
        return decrypt_password(result[0])
    else:
        return None


def main():
    drop_tables()
    create_tables()
    insert_into_file('Statement_2022MTH01_140526881.pdf', 'abc123')
    print(get_all_files_data())
    result = get_password_for_file('Statement_2022MTH01_140526881.pdf')
    if result is not None:
        print(result)

    insert_into_pattern('Statement_*.pdf', 'abc123')
    insert_into_pattern('*Statement_2022MTH0*.pdf', 'abc123')
    insert_into_pattern('*Tanmay_Mukund_Dange_*.pdf', 'abc123')

    # Printing all Patterns in the database
    for pat in get_all_patterns():
        print(pat)

    # Fetching Password for a given pattern
    result = get_password_for_pattern('Statement_*.pdf')
    if result is not None:
        print(result)
    
if __name__ == "__main__":
    main()