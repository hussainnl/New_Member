from apscheduler.schedulers.background import BackgroundScheduler
from data_base_manager import Member_Info ,Member_State 
from prepare_member_sheet import Prepare_Member_Sheet
import time
from member_reminder import check_pass_state
import logging


logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S"  
)


scheduler = BackgroundScheduler()
scheduler.start()


len_of_taple = Member_Info().make_member_id()
member_ids = []
for x in range(1,len_of_taple+1):
    member_ids.append(x)
member_ids
print(member_ids)
for member_id in member_ids:
    print(member_id)
    email,name,new_link = Member_Info().get_member_sheet_id(member_id)
    join_time = Member_Info().get_member_join_time(member_id)
    reminder_time = check_pass_state(scheduler,join_time, member_id, name,email)
    Member_State().update_reminder_time(reminder_time,member_id)

while True:

    Member_Info().make_new_table()
    Member_Info().check_new_members()
    Member_State().make_new_table()
    Member_State().fetch_member_data()
    members_ids = Member_State().get_members_ids()
    for member_id in members_ids:
        try:
            email,name,new_link = Member_Info().get_member_sheet_id(member_id)
            Prepare_Member_Sheet().send_member_sheet(email,name,new_link)      
            join_time = Member_Info().get_member_join_time(member_id)
            reminder_time = check_pass_state(scheduler,join_time, member_id, name,email)
            Member_State().update_reminder_time(reminder_time,member_id)
            logging.info(f"Sending successful to {name}")
        except:
            logging.info(f"Sending failed to {name}")
    logging.info("Latest updates checked")
    time.sleep(3600)
    
