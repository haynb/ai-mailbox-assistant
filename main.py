import schedule
import time
from emailSvc.emailServer import MailSvc
from openaiModel.gptSvc import GptSvc
from datetime import datetime

mailSvc = MailSvc()
gptSvc = GptSvc(mailSvc)

def start():
    msgs = mailSvc.get_email_message_list(unread_only=True)
    for msg in msgs:
        result = mailSvc.get_email_info(msg)
        today_date = datetime.now().strftime("%Y-%m-%d")
        message = (
            "Could you summarize this email for me? "
            + "Today's date is " + today_date + ". The email_id and subject and the content is: "
            + msg.decode('utf-8') + "\n"
            + result[1] + "\n"
            + result[3]
        )
        gptSvc.add_message("user", message)
        gptSvc.call_function("summarize_email", gptSvc.summarize_email)

# 每小时执行一次 summarize_emails 函数
schedule.every(1).hours.do(start)

# 无限循环，保持程序运行并执行定时任务
while True:
    schedule.run_pending()
    time.sleep(1)