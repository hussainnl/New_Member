import sqlite3
import os
import logging
from fetch_sheet_data import Fetch_Sheet_Data
from dotenv import load_dotenv

sheet_data = Fetch_Sheet_Data()
load_dotenv()
DB = os.getenv('DB')
con = sqlite3.connect(DB)
cur = con.cursor()

class Member_Info:

    def __init__(self):
        self.con = con
        self.cur = cur
        self.sheet_data = sheet_data
        self.taple = self.make_new_table()
        self.value =  self.make_member_id() + 2 

    def make_new_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS  member_info(member_id, name, hours, role, email ,join_time, sheet_id)")
        logging.info('make_new_table() executed')
        print('make_new_table() executed')
        self.con.commit()

        
    def new_member(self,member_data):
        """To add a new member"""
        
        print('add_new_member() executed')
        
        
        member_id = self.make_member_id() + 1
        name = member_data[0][2] +" " + member_data[0][3]
        hours = member_data[0][9]
        role = member_data[0][4]
        email = member_data[0][1]
        sheet_id = member_data[0][1]
        print(role)
        join_time = member_data[0][0][9:20]
        self.cur.execute("""
            INSERT OR IGNORE INTO member_info (member_id, name, hours, role, email, join_time, sheet_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (member_id, name, hours, role, email, join_time,sheet_id))
        self.con.commit()

    def make_member_id(self):
        res = self.cur.execute("SELECT member_id FROM member_info")
        len_of_taple =  len(res.fetchall())
        return len_of_taple
    
    def git_member_sheet_id(self,member_id):
        res = cur.execute("SELECT name,email FROM member_info WHERE member_id = ?",(member_id,)).fetchall()
    def  add_new_member (self):
        try:    
            while True:
                member_data = self.sheet_data.get_values("1Xrve4ABSNuJfVpgZMrMVyyUzkoTgFQhTZHm2omuVzK4", f"A{self.value}:J{self.value}")['values']
                self.new_member(member_data)
                self.value += 1
        except:
            print("done")





class Member_State:

    def __init__(self):
        self.con = con
        self.cur = cur
           
    

    def make_new_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS member_state(id, name, score, is_passed)")
        logging.info('make_new_table() executed')
        print('make_new_table() executed')
        self.con.commit()

    # def fetch_member_data(self):
    #     res = cur.execute("SELECT member_id,name FROM member_info")
    #     members =res.fetchall()

    #     for member in range(len(members)):
    #         id_member=members[member][0]
    #         name= members[member][1]

    #         self.cur.execute("""
    #         INSERT OR IGNORE INTO member_info (member_id, name, score, is_passed)
    #         VALUES (?, ?, ?, ?, ?, ?)
    #         """, (id_member, name, score, is_passed))
    #         self.con.commit()
    def member_score(self):
         res = self.cur.execute("SELECT sheet_id FROM member_info")

