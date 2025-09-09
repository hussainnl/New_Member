import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from final_html_body import EMAIL_HTML_BODY
from config import Configuration
from final_html_body import EMAIL_HTML_BODY
import os
from dotenv import load_dotenv


load_dotenv()
SOCIAL_MEDIA = os.getenv('SOCIAL_MEDIA')


class Prepare_Member_Sheet :
    
    def __init__(self):
        self.credentials = Configuration().authenticate_google()
        self.social_media = SOCIAL_MEDIA
        
    def copy_and_share_sheet(self,origin_file_id, new_name, email):
        """
        تنسخ الملف وتشاركه (بدون إرسال إشعار)، وتعيد ID ورابط الملف الجديد.
        """
        try:
            new_name = f"نسخة تقيم {new_name}"
            drive_service = build('drive', 'v3', credentials=self.credentials)
            print(f"جاري إنشاء نسخة من الملف بالاسم: '{new_name}'...")
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
                print("خطأ: فشلت عملية النسخ.")
                return None, None
            print(f"تم إنشاء النسخة بنجاح! ID: {new_file_id}")

            print(f"جاري منح صلاحية 'محرر' للمستخدم: '{email}'...")
            user_permission = {'type': 'user', 'role': 'writer', 'emailAddress': email}
            drive_service.permissions().create(
                fileId=new_file_id,
                body=user_permission,
                sendNotificationEmail=False  # --- مهم: لن نرسل الإشعار من هنا ---
            ).execute()
            print("تم منح الصلاحية بنجاح.")
            print(new_file_link)
            return new_file_id, new_file_link
        except HttpError as error:
            print(f'حدث خطأ في Google Drive API: {error}')
            return None, None
        
    def htnl_body_prepare(self,name,file_name,file_link,social_media):
        
        final_html_body = EMAIL_HTML_BODY.format(name =name ,file_name=file_name, file_link= file_link,social_media = social_media)
        return final_html_body
    def send_custom_email(self, to_email, name,file_name,file_link):
        """
        تستخدم Gmail API لإرسال بريد إلكتروني مخصص بتنسيق HTML.
        """
        try:
            social_media = self.social_media
            subject = f"مرحباً بك يا{name} في مشروع 'نواة'"
            file_name = f"نسخة تقيم {name}"
            gmail_service = build('gmail', 'v1', credentials=self.credentials)
            print(f"جاري إرسال بريد إلكتروني مخصص إلى: {to_email}...")
        
            message = MIMEText(self.htnl_body_prepare(name,file_name,file_link,social_media), 'html')
            message['to'] = to_email
            message['subject'] = subject
        
            # 'me' تشير إلى حساب المستخدم الذي قام بالمصادقة
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body = {'raw': raw_message}
        
            gmail_service.users().messages().send(userId='me', body=body).execute()
            print("تم إرسال البريد الإلكتروني بنجاح!")
        except HttpError as error:
            print(f'حدث خطأ في Gmail API: {error}')





# if Prepare_Member_Sheet().credentials:
#             # 2. نسخ ومشاركة الملف باستخدام Drive API
#             new_id, new_link = copy_and_share_sheet(
#                 credentials, 
#                 ORIGINAL_FILE_ID, 
#                 NEW_FILE_NAME, 
#                 EMAIL_TO_SHARE_WITH
#             )
            
#             # 3. إذا نجحت الخطوة السابقة، قم بإرسال الإيميل المخصص
#             if new_id and new_link:
#                 # تعبئة المتغيرات في رسالة الـ HTML
#                 final_html_body = EMAIL_HTML_BODY.format(file_name=NEW_FILE_NAME, file_link= new_link)
                
#                 send_custom_email(
#                     credentials,
#                     EMAIL_TO_SHARE_WITH,
#                     EMAIL_SUBJECT,
#                     final_html_body
#                 )
                
#                 print("\n" + "="*50)
#                 print("✨ اكتملت العملية بالكامل بنجاح! ✨")
#                 print(f"ID الملف الجديد هو:\n{new_id}")
#                 print("="*50)


