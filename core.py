""" Core File
    this file was made to contain Different things related to the core
    used mostly in main app.py"""

#Import Libs for using in functions
#socket for checking if server is up
import socket
import configparser
#official MySQL connector for python
import mysql.connector as mdb


#Used for Getting Admin Login Information
config = configparser.ConfigParser()
config.read('config.ini')
database=config['database']
""" Host is Up Function.
    Used for checking a UCS server"""
def isup(host,port):
    #makes a socekt
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #makes port Int if it is already not
        port=int(port)
        #connects to the host
        s.connect((host, port))
        #disconnects from host
        s.shutdown(2)
        #if no error accure and the connection is successfull,Returns True
        return True
    except:
        """ error may accure like error while connecting to host or ...
            in this case, False is Returned """
        return False

#function is used to connecting to database
def connect_mdb(host=database["host"], user=database["user"], password=database["pass"], database=database["database"]):
    con = mdb.connect(host=host,user=user,password=password,database=database)
    #con.set_character_set('utf8')
    return con