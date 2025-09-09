from data_base_manager import Member_Info ,Member_State
from prepare_member_sheet import Prepare_Member_Sheet
import os
from dotenv import load_dotenv


load_dotenv()
ORIGINAL_FILE_ID = os.getenv('ORIGINAL_FILE_ID')
Member_Info().add_new_member()
name , email = Member_State().member_score()[0]

new_id, new_link = Prepare_Member_Sheet().copy_and_share_sheet(ORIGINAL_FILE_ID,name,email)
Prepare_Member_Sheet().send_custom_email(email,name,name,new_link)