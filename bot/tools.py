import paramiko
import os,dotenv
import psycopg2
import logging
from psycopg2 import Error
import re

logging.basicConfig(
    filename='logfile.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, encoding="utf-8"
)

dotenv.load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')

def exec_command_ssh(command):
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    username = os.getenv('USER')
    password = os.getenv('PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port) 
    stdin, stdout, stderr = client.exec_command(command) 
    data = stdout.read() + stderr.read() 
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    return data 

def get_row_from_table(table_name):
    connection = None
    msg = ""
    try:
        connection = psycopg2.connect(user=DB_USER,
                                        password=DB_PASSWORD,
                                        host=DB_HOST,
                                        port=DB_PORT, 
                                        database=DB_NAME)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM %s;" % (table_name))
        data = cursor.fetchall()
        for row in data:
            msg += f"{row[0]}. {row[1]}\n"

        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    return msg


def insert_to_table_info(table_name, column,data):
    connection = None
    status = False
    try:
        connection = psycopg2.connect(user=DB_USER,
                                        password=DB_PASSWORD,
                                        host=DB_HOST,
                                        port=DB_PORT, 
                                        database=DB_NAME)

        cursor = connection.cursor()

        cursor.execute("INSERT INTO %s (%s) VALUES ('%s')" % (table_name,column, data))
        connection.commit()
        status = True
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    return status

def check_to_exists_table(table_name,column,string):
    connection = None
    status = False
    try:
        connection = psycopg2.connect(user=DB_USER,
                                        password=DB_PASSWORD,
                                        host=DB_HOST,
                                        port=DB_PORT, 
                                        database=DB_NAME)

        cursor = connection.cursor()

        cursor.execute("SELECT exists (SELECT 1 FROM %s WHERE %s = '%s' LIMIT 1);" % (table_name,column,string))
        data = cursor.fetchall()
        status = data[0][0]
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    return status

def find_email_in_text(text):
    emailRegex = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}')

    emailList = emailRegex.findall(text)

    emails = [] # список (id,email)

    for i in range(len(emailList)):
        emails.append((i+1, emailList[i]))
    
    return emails

def find_phone_in_text(text):
    phoneNumRegex = re.compile(r"((8|\+7)[\- ]?\(?\d{3}\)?[\- ]?[\d\- ]{7,10}(?<!-))")

    phoneNumberList = phoneNumRegex.findall(text)

    phoneNumbers = []
    count_number = 0 
    for i in range(len(phoneNumberList)):
        if len("".join(re.split(r'[()\-\+ ]',phoneNumberList[i][0]))) == 11:
            count_number += 1
            phoneNumbers.append((count_number,phoneNumberList[i][0]))
    return phoneNumbers