import sqlite3
import os
import re
import logging
from fetch_sheet_data import Fetch_Sheet_Data
from dotenv import load_dotenv
import logging

load_dotenv()

HOURS_IDS = os.getenv("HOURS_IDS").split(",\n")
ORIGINAL_FILE_ID = os.getenv('ORIGINAL_FILE_ID')
DB = os.getenv('DB')
REGASTER_FILE_ID = os.getenv('REGASTER_FILE_ID')
sheet_data = Fetch_Sheet_Data()


class Member_Info:

    def __init__(self):
        self.con =  sqlite3.connect(DB, check_same_thread=False)
        self.cur = self.con.cursor()
        self.sheet_data = sheet_data
        self.value =  self.make_member_id() + 2
        

    def make_new_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS  member_info(member_id, name, hours, role, email ,join_time, sheet_id)")
        logging.info('Member_Info().make_new_table() executed')
        
        self.con.commit()

        
    def new_member(self,member_data):
        """To add a new member"""
             
        member_id = self.make_member_id() + 1
        name = member_data[0][2] +" " + member_data[0][3]
        hours = member_data[0][9]
        role = member_data[0][4]
        email = member_data[0][1]
        sheet_id = 'not has'
        logging.info(name)
        join_date = member_data[0][0]
        match= re.search(r"\d{4}/\d{2}/\d{2}", join_date)
        join_time = match.group()
        self.cur.execute("""
            INSERT OR IGNORE INTO member_info (member_id, name, hours, role, email, join_time, sheet_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (member_id, name, hours, role, email, join_time,sheet_id))
        self.con.commit()

    def make_member_id(self):
        try:
            res = self.cur.execute("SELECT member_id FROM member_info")
            len_of_taple =  len(res.fetchall())
            return len_of_taple
        except:
            len_of_taple =  0
            return len_of_taple
    
    def get_member_sheet_id(self,member_id):

        currint_sheet_id = self.cur.execute("SELECT sheet_id FROM member_info WHERE member_id = ? ",(member_id,)).fetchone()[0]
        from prepare_member_sheet import Prepare_Member_Sheet
        name , email =Member_State().required_data(member_id)
        if currint_sheet_id == 'not has':
            origin_sheet = self.get_origin_id(member_id)
            sheet_id, sheet_link = Prepare_Member_Sheet().copy_and_share_sheet(origin_sheet,name,email)
            currint_sheet_id = self.updata_member_sheet_id(sheet_id,member_id)
            Member_State().update_s_sent(member_id)
            logging.info('sheet_link')
            return email,name,sheet_link
        else:
            currint_sheet_link = 'https://docs.google.com/spreadsheets/d/'+ currint_sheet_id +'/edit?usp=drivesdk'
            logging.info('currint_sheet_link',currint_sheet_link)
            return email,name,currint_sheet_link

            
        
    
    def get_origin_id(self,member_id):

        member_hours =  [self.get_member_hours(member_id) - 1,]
        origin_id = HOURS_IDS[member_hours[0]]     
        return origin_id        


    def updata_member_sheet_id(self,sheet_id,member_id):
        
        self.cur.execute("""
            UPDATE member_info
            SET sheet_id = ? 
            where member_id =?
            """, (sheet_id,member_id))
        self.con.commit()

        
    def get_member_join_time(self,member_id):

        member_join_time = self.cur.execute("SELECT join_time FROM member_info WHERE member_id = ? ",(member_id,)).fetchone()[0]
        return member_join_time
    def get_member_hours(self,member_id):

        member_hours = self.cur.execute("SELECT hours FROM member_info WHERE member_id = ? ",(member_id,)).fetchone()[0]
        return int(member_hours)


    def  check_new_members (self):

        try:    
            while True:
                member_data = self.sheet_data.get_values(REGASTER_FILE_ID, f"A{self.value}:J{self.value}")['values']
                
                self.new_member(member_data)
                self.value += 1
        except Exception :
            pass




class Member_State:

    def __init__(self):
        self.con = sqlite3.connect(DB, check_same_thread=False)
        self.cur = self.con.cursor()
        self.sheet_data = sheet_data
        
    def make_new_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS member_state(member_id, name, score, reminder_time, is_sheet_sent, is_passed)")
        logging.info('Member_State.make_new_table() executed')
        self.con.commit()

    def fetch_member_data(self):
        """To fertch and insert the data from member_info taple into member_state"""
        res = self.cur.execute("SELECT member_id,name FROM member_info")
        members =res.fetchall()
        members_ids = self.cur.execute("SELECT member_id,name FROM member_state").fetchall()
        
        for member in range(len(members)):
            member_id=members[member][0]
            name= members[member][1]
            score = 0
            reminder_time = 'not has'
            is_sheet_sent = 0
            is_passed = 0
            
            if  members_ids == []:
                self.cur.execute("""
                INSERT OR IGNORE INTO member_state (member_id, name, score, reminder_time, is_sheet_sent, is_passed)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (member_id, name, score, reminder_time, is_sheet_sent, is_passed))
                self.con.commit()
            elif member_id not in members_ids[member] :
                self.cur.execute("""
                INSERT OR IGNORE INTO member_state (member_id, name, score, reminder_time, is_sheet_sent, is_passed)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (member_id, name, score, reminder_time, is_sheet_sent, is_passed))
                self.con.commit()
            else:
                continue
        
    def required_data(self,member_id):

        res = self.cur.execute("SELECT name,email FROM member_info WHERE member_id = ?",(member_id,)).fetchall()[0]
        return res
    



    def get_sheet_score (self,member_id):
        """To get member score from the member sheet"""
        try:
            sheet_id = self.cur.execute("SELECT sheet_id FROM member_info WHERE member_id = ?",(member_id,)).fetchone()[0]
            logging.info(sheet_id)
            score = self.sheet_data.get_values(sheet_id, f"C26")['values'][0][0]
            return score
        except Exception as e:
            logging.info('member not has sheet id')
            logging.error(f"Error details: {e}")
    
    def update_score(self,member_id):
        score = self.get_sheet_score(member_id)
        self.cur.execute("""
        UPDATE member_state
        SET score = ? 
        WHERE 
        member_id = ?
        """, (score,member_id))
        self.con.commit()

    def get_score(self,member_id):
        """To get member score from the data base"""
        member_score = self.cur.execute("SELECT score FROM member_state WHERE member_id = ?",(member_id,)).fetchone()[0]

        member_score = member_score.replace("%", "")

        member_score = member_score.replace("٫", ".")

        member_score = float(member_score)

        return member_score

    def update_pass_state(self,member_id):

        member_score = self.get_score(member_id)
        logging.info(member_score,"member_score")
        required_score = 51.00
        if member_score >= required_score :
            self.cur.execute("""
            UPDATE member_state
            SET is_passed = ? 
            WHERE 
            member_id = ?
            """, (1,member_id))
            self.con.commit()
            
        else:
            self.cur.execute("""
            UPDATE member_state
            SET is_passed = ? 
            WHERE 
            member_id = ?
            """, (0,member_id))
            self.con.commit()
            
    def get_pass_state(self,member_id):

        pass_state = self.cur.execute("SELECT is_passed FROM member_state WHERE member_id = ?",(member_id,)).fetchone()[0]
        return pass_state

    def update_s_sent (self,member_id):

        sheet_id = self.cur.execute("SELECT sheet_id FROM member_info WHERE member_id = ?",(member_id,)).fetchone()[0]
        if sheet_id != 'not has':
            self.cur.execute("""
            UPDATE member_state
            SET is_sheet_sent = ? 
            WHERE 
            member_id = ?
            """, (1,member_id))
            self.con.commit()

    def update_reminder_time(self,reminder_time,member_id):

        reminder_state = self.cur.execute("SELECT reminder_time FROM member_state WHERE member_id = ?",(member_id,)).fetchone()[0]
        reminder_time = str(reminder_time)
        reminder_time = reminder_time.replace("-", "/")
        match= re.search(r"\d{4}/\d{2}/\d{2}", reminder_time)
        new_reminder_time = match.group()
        if reminder_state == 'not has':
            self.cur.execute("""
            UPDATE member_state
            SET reminder_time = ? 
            WHERE 
            member_id = ?
            """, (new_reminder_time,member_id))
            self.con.commit()

    def get_current_reminder_time(self,member_id):
        
       current_reminder_time = self.cur.execute("SELECT reminder_time FROM member_state WHERE member_id = ?",(member_id,)).fetchone()[0]
       return current_reminder_time


    def get_members_ids(self):
        
        members = self.cur.execute("SELECT member_id FROM member_state WHERE is_sheet_sent = 0").fetchall()
        members_ids = [member[0] for member in members]
        return members_ids



class Member_info_state(Member_State):

    def __init__(self,member_id):
        super().__init__()
        self.update_score(member_id)
        self.update_pass_state(member_id)
        self.pass_state = self.get_pass_state(member_id)    
