from emailSvc.emailServer import mailSvc

mailSvc = mailSvc()
msg = mailSvc.get_email_message_list()
msgList = mailSvc.get_email_info(msg,10)
for items in msgList:
    print(items[0])
    pass
print(mailSvc.send_email("heanyang@sailvan.com","静态检查芭芭拉","test"))
