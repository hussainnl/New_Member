import base64
import os
import asyncio
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from final_html_body import EMAIL_HTML_BODY , PASS_HTML_BODY, NOT_PASS_HTML_BODY
from config import Configuration
from get_invite_link import get_invite_link
from dotenv import load_dotenv
import logging

load_dotenv()
SUPPORT_ASKING_LINK = os.getenv('SUPPORT_ASKING_LINK')
TASKS_LINK = os.getenv('TASK_LINK')
APPLY_AGAIN_LINK = os.getenv('APPLY_AGAIN_LINK')
GROUP_ID = os.getenv('GROUP_ID')


class Prepare_Member_Sheet :
    
    def __init__(self):
        self.credentials = Configuration().authenticate_google()
        self.support_asking_link = SUPPORT_ASKING_LINK
        self.tasks_link = TASKS_LINK
        self.apply_again_link = APPLY_AGAIN_LINK
        
    def copy_and_share_sheet(self,origin_file_id, new_name, email):
        """
        تنسخ الملف وتشاركه (بدون إرسال إشعار)، وتعيد ID ورابط الملف الجديد.
        """
        try:
            new_name = f"نسخة تقيم {new_name}"
            drive_service = build('drive', 'v3', credentials=self.credentials)
            logging.info(f"جاري إنشاء نسخة من الملف بالاسم: '{new_name}'...")
            file_metadata = {'name': new_name}
            # نطلب ID والرابط معاً
            copied_file = drive_service.files().copy(
                fileId=origin_file_id,
                body=file_metadata,
                fields='id, webViewLink'
            ).execute()
            new_file_id = copied_file.get('id')
            new_file_link = copied_file.get('webViewLink')

            if not new_file_id:
                logging.info("خطأ: فشلت عملية النسخ.")
                return None, None
            logging.info(f"تم إنشاء النسخة بنجاح! ID: {new_file_id}")

            logging.info(f"جاري منح صلاحية 'محرر' للمستخدم: '{email}'...")
            user_permission = {'type': 'user', 'role': 'writer', 'emailAddress': email}
            drive_service.permissions().create(
                fileId=new_file_id,
                body=user_permission,
                sendNotificationEmail=False  # --- مهم: لن نرسل الإشعار من هنا ---
            ).execute()
            logging.info("تم منح الصلاحية بنجاح.")
            logging.info(new_file_link)
            return new_file_id, new_file_link
        except HttpError as error:
            logging.info(f'حدث خطأ في Google Drive API: {error}')
            return None, None
        
    def htnl_member_sheet(self,name,file_name,file_link,support_asking_link,tasks_link):
        
        final_html_body = EMAIL_HTML_BODY.format(name =name ,file_name=file_name, file_link= file_link,
                                                 support_asking_link = support_asking_link ,tasks_link = tasks_link)
        return final_html_body
    def send_member_sheet(self, to_email, name,file_link):
        """
        تستخدم Gmail API لإرسال بريد إلكتروني مخصص بتنسيق HTML.
        """
        try:
            support_asking_link = self.support_asking_link
            tasks_link = self.tasks_link
            subject = f"مرحباً بك يا{name} في مشروع 'نواة'"
            file_name = f"نسخة تقيم {name}"
            gmail_service = build('gmail', 'v1', credentials=self.credentials)
            logging.info(f"جاري إرسال بريد إلكتروني مخصص إلى: {to_email}...")
        
            message = MIMEText(self.htnl_member_sheet(name, file_name, file_link, support_asking_link, tasks_link), 'html')
            message['to'] = to_email
            message['subject'] = subject
        
            # 'me' تشير إلى حساب المستخدم الذي قام بالمصادقة
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body = {'raw': raw_message}
        
            gmail_service.users().messages().send(userId='me', body=body).execute()
            logging.info("تم إرسال البريد الإلكتروني بنجاح!")
        except HttpError as error:
            logging.info(f'حدث خطأ في Gmail API: {error}')



    def htnl_pass_state(self,name,pass_state_link,pass_state):
        if pass_state == 1 :
            final_html_body = PASS_HTML_BODY.format(name =name ,pass_state_link = pass_state_link)
        else:
            final_html_body = NOT_PASS_HTML_BODY.format(name =name ,pass_state_link = pass_state_link)
        return final_html_body
    def send_pass_state(self, to_email, name,pass_state):
        """
        تستخدم Gmail API لإرسال بريد إلكتروني مخصص بتنسيق HTML.
        """
        try:
            
            if pass_state == 1 :
                
                pass_state_link =  asyncio.run(get_invite_link(GROUP_ID))
                
            else:
                pass_state_link = self.apply_again_link           
  
            subject = f"مرحباً بك يا{name} في مشروع 'نواة'"
            gmail_service = build('gmail', 'v1', credentials=self.credentials)
            logging.info(f"جاري إرسال بريد إلكتروني مخصص إلى: {to_email}...")
        
            message = MIMEText(self.htnl_pass_state(name,pass_state_link,pass_state), 'html')
            message['to'] = to_email
            message['subject'] = subject
        
            # 'me' تشير إلى حساب المستخدم الذي قام بالمصادقة
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body = {'raw': raw_message}
        
            gmail_service.users().messages().send(userId='me', body=body).execute()
            logging.info("تم إرسال البريد الإلكتروني بنجاح!")
        except HttpError as error:
            logging.info(f'حدث خطأ في Gmail API: {error}')


