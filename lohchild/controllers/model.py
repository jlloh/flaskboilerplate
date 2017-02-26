import bcrypt
from flask import g,current_app
import sqlite3
from collections import OrderedDict

class User:
    """
    initialize User class with username, and database to see if user exists?
    """
    def __init__(self,username,database):
        """
        assumption that username is a unicode, and equivalent to the user_id field 
        that flask-login requires
        """
        self.database=database
        self.username=username

        self.is_active0=True
        self.is_authenticated0=False

        con=sqlite3.connect(self.database)
        userid=None
        for row in con.execute('SELECT id, hashed, role from users where username = ?'
                              ,[str(self.username)]):
            print row
            userid, hashed, role=row
        con.close()

        if userid:
            self.is_anonymous0=False
            self.userid = userid
            self.role = role
        else:
            self.is_anonymous0=True
            self.userid = None
            self.role = None



    def authenticate(self,password):
        """
        authenticate user and set is_authenticated0 flag
        self.is_authenticated0 boolean is the parameter that is used to determine 
        if session should be logged in
        """

        hashed=None

        con=sqlite3.connect(self.database)
        for row in con.execute('SELECT hashed from users where username=?'
                              ,[str(self.username)]):
            hashed,=row
        con.close()


        if hashed==None:
            self.is_anonymous0=True
        else:
            hashedresult=bcrypt.hashpw(password.encode('utf-8'),hashed.encode('utf-8'))
            if hashedresult==str(hashed):
                self.is_authenticated0=True
            else:
                self.is_authenticated0=False
    def is_authenticated(self):
        """
        fudging misleading. this isn't whether the user password has been logged in, 
        but rather any valid user. I guess you disable this if you want to lock 
        somebody out.
        """
        
        return True
    def is_active(self):
        return self.is_active0
    def is_anonymous(self):
        return self.is_anonymous0


    def get_id(self):
        if self.is_anonymous()==False:
            return unicode(self.username)
        return None

    def get_userid(self):
        if self.is_anonymous()==False:
            return unicode(self.userid)
        return None

    def get_userrole(self):
        if self.is_anonymous()==False:
            return self.role
        return None


#Function to connect to database
