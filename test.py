from emailSvc.emailServer import MailSvc
from openaiModel.gptSvc import GptSvc
from datetime import datetime

mailSvc = MailSvc()
msg = mailSvc.get_email_message_list(unread_only=False)
result = mailSvc.get_email_info(msg[-3])
# for items in msgList:
#     print(items[3])
#     pass
# print(mailSvc.send_email("heanyang@sailvan.com","测试邮件，勿回","test\n"))

# mailSvc.mark_emails_as_read()


gptSvc = GptSvc(mailSvc)
# 获取今天的日期并格式化为字符串
today_date = datetime.now().strftime("%Y-%m-%d")
message = (
    "Could you summarize this email for me? "
    + "Today's date is " + today_date + ". The email_id and subject and the content is: "
    + msg[-3].decode('utf-8') + "\n"
    + result[1] + "\n"
    + result[3]
)
gptSvc.add_message("user",message)
response = gptSvc.call_function("summarize_email",gptSvc.summarize_email)

