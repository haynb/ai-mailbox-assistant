### 项目概要

本项目使用Python语言开发，旨在通过IMAP协议接入AI大模型功能，利用大模型的Function Call实现本地函数，自动总结邮箱邮件内容并判断其紧急性。项目功能包括：

- 自动获取未读邮件并总结其内容
- 判断邮件是否紧急，紧急邮件立即通知主人
- 将非紧急邮件总结写入文件，每天定时发送给主人
- 设置日程提醒，定时任务提醒主人

### 项目依赖管理

项目依赖于以下主要库：

- `imaplib` 和 `smtplib`：用于IMAP和SMTP邮件服务
- `email`：处理邮件内容
- `openai`：调用OpenAI的GPT服务
- `schedule` 和 `apscheduler`：定时任务调度

### 项目构建和运行环境

1. 安装依赖库：

   ```
   bash
   Copy Code
   pip install imaplib smtplib email openai schedule apscheduler
   ```

2. 创建并配置`app_config`文件，包含邮箱和OpenAI API的配置信息。

3. 构建并运行项目：

   ```
   bash
   Copy Code
   python main.py
   ```

### 项目实现和功能点

1. **邮件服务初始化**：

   - IMAP和SMTP服务初始化，登录邮箱。

   ```
   pythonCopy Codedef init_imap(self):
       mail = imaplib.IMAP4_SSL(app_config.email_imap_server, app_config.email_imap_port)
       mail.login(app_config.email_account, app_config.email_password)
       self.imapSvc = mail
   
   def init_smtp(self):
       mail = smtplib.SMTP(app_config.email_smtp_server, app_config.email_smtp_port)
       mail.starttls()
       mail.login(app_config.email_account, app_config.email_password)
       self.smtpSvc = mail
   ```

2. **获取和处理邮件**：

   - 获取未读邮件列表，提取邮件信息。

   ```
   pythonCopy Codedef get_email_message_list(self, unread_only=False):
       self.imapSvc.select('INBOX')
       criteria = 'UNSEEN' if unread_only else 'ALL'
       status, messages = self.imapSvc.search(None, criteria)
       mailList = messages[0].split()
       return mailList
   
   def get_email_info(self, mail_id):
       status, message = self.imapSvc.fetch(mail_id, '(RFC822)')
       msg = email.message_from_bytes(message[0][1])
       subject, encoding = decode_header(msg["Subject"])[0]
       if isinstance(subject, bytes):
           subject = subject.decode(encoding if encoding else 'utf-8')
       from_ = msg.get("From")
       date_ = parsedate_to_datetime(msg.get("Date"))
       content = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
       return [subject, from_, date_, content]
   ```

3. **调用AI总结邮件**：

   - 调用OpenAI模型总结邮件内容，并判断紧急性。

   ```
   pythonCopy CodegptSvc = GptSvc(mailSvc)
   message = (
       "Could you summarize this email for me? Today's date is " + today_date + ". The email_id and subject and the content is: "
       + msg[-3].decode('utf-8') + "\n"
       + result[1] + "\n"
       + result[3]
   )
   gptSvc.add_message("user",message)
   response = gptSvc.call_function("summarize_email",gptSvc.summarize_email)
   ```

4. **定时任务**：

   - 使用`schedule`和`apscheduler`实现定时任务，每小时检查未读邮件并总结。

   ```
   pythonCopy Codeimport schedule
   import time
   
   def summarize_emails():
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
           response = gptSvc.call_function("summarize_email", gptSvc.summarize_email)
   
   schedule.every(1).hours.do(summarize_emails)
   
   while True:
       schedule.run_pending()
       time.sleep(1)
   ```

### 执行效果

项目启动后将自动检查邮箱中的未读邮件，使用AI大模型总结邮件内容，并根据紧急程度进行处理。非紧急邮件会被写入文件并每天发送给主人，紧急邮件则会立即通知主人。此外，用户还可以设置日程提醒，项目将通过定时任务提醒用户。

通过以上功能，项目实现了邮件管理的自动化和智能化，提高了用户处理邮件的效率。