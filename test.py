from emailSvc.emailServer import MailSvc
from openaiModel.gptSvc import GptSvc

mailSvc = MailSvc()
msg = mailSvc.get_email_message_list(unread_only=False)
msgList = mailSvc.get_email_info(msg,5)
# for items in msgList:
#     print(items[3])
#     pass
# print(mailSvc.send_email("heanyang@sailvan.com","测试邮件，勿回","test\n"))

# mailSvc.mark_emails_as_read()

gptSvc = GptSvc()
gptSvc.add_message("user","Could you summarize this email for me? The subject and the content is :" + msgList[4][1] + msgList[4][4])
response = gptSvc.call_function("summarize_email",gptSvc.summarize_email)
