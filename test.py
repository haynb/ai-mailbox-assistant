from emailSvc.emailServer import MailSvc

mailSvc = MailSvc()
msg = mailSvc.get_email_message_list(unread_only=True)
msgList = mailSvc.get_email_info(msg,5)
for items in msgList:
    print(items[1])
    pass
# print(mailSvc.send_email("heanyang@sailvan.com","测试邮件，勿回","test\n"))

# mailSvc.mark_emails_as_read()

