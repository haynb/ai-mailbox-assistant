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
response_message = gptSvc.call_function()
tool_calls = response_message.tool_calls
if tool_calls:
    tool_call_id = tool_calls[0].id
    tool_function_name = tool_calls[0].function.name
    arguments = tool_calls[0].function.arguments.replace('false', 'False').replace('true', 'True')
    params = eval(arguments)
    if tool_function_name == "summarize_email":
        gptSvc.summarize_email(**params)
