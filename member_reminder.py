from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random




def check_pass_state(scheduler,join_time, member_id, name,email):
    """

    
    """
    
    
    func = send_pass_email
    from data_base_manager import Member_State
    current_reminder_time = Member_State().get_current_reminder_time(member_id)
    if current_reminder_time == 'not has':
        join_time = datetime.strptime(join_time, "%Y/%m/%d")
        run_time =  join_time + timedelta(days = 6)
    else:
        run_time = datetime.strptime(current_reminder_time, "%Y/%m/%d")

    run_time = run_time.replace(
    hour=10,
    minute=random.randint(0, 59),
    second=random.randint(0, 59),
    microsecond=0 )

    # Add Job
    scheduler.add_job(
        func,
        trigger="date",           # تشغيل مرة واحدة في وقت محدد
        run_date=run_time,
        args=[scheduler, member_id, name,email],         # تمرير member_id للفنكشن
        id=f"job_{member_id}",    # ID مميز لكل عضو
        replace_existing=True,    # لو العضو ليه Job قديمة تتبدل
        timezone=ZoneInfo("Africa/Cairo")
    )
    print(f"Job added for member {member_id}, scheduled at {run_time}")
    return run_time

def send_pass_email(scheduler, member_id, name,email):
    """
    
    
    """
    
    from prepare_member_sheet import Prepare_Member_Sheet
    func = Prepare_Member_Sheet().send_pass_state
    run_time =  datetime.now() + timedelta(seconds = 3)
    
    from data_base_manager import Member_info_state
    pass_state = Member_info_state(member_id).pass_state
    
    # Add Job
    scheduler.add_job(
        func,
        trigger="date",           # تشغيل مرة واحدة في وقت محدد
        run_date=run_time,
        args=[email,name,pass_state],         # تمرير member_id للفنكشن
        id=f"job_{member_id}",    # ID مميز لكل عضو
        replace_existing=True,    # لو العضو ليه Job قديمة تتبدل
        timezone=ZoneInfo("Africa/Cairo")
    )
    print(f"Job added for member {member_id}, scheduled at {run_time}")
    return run_time