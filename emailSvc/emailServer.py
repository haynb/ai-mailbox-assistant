import email
from email.utils import parsedate_to_datetime
from conf.conf import app_config
import imaplib
import smtplib
from imapclient import imap_utf7
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

class MailSvc:
    imapSvc = None
    stmpSvc = None
    # 缓存未读邮件
    unread_emails_cache = {}

    def __init__(self):
        self.init_imap()
        self.init_smtp()
        pass

    def init_imap(self):
        """
        Initialize the IMAP service
        :return:
        """
        # 邮箱的IMAP地址和端口
        imap_server = app_config.email_imap_server
        imap_port = app_config.email_imap_port

        # 创建一个IMAP4的SSL实例
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)

        # 登录邮箱
        your_email = app_config.email_account
        your_password = app_config.email_password
        mail.login(your_email, your_password)
        self.imapSvc = mail


    def init_smtp(self):
        """
        Initialize the SMTP service
        :return:
        """
        # 邮箱的SMTP地址和端口
        smtp_server = app_config.email_smtp_server
        smtp_port = app_config.email_smtp_port

        # 创建一个SMTP实例
        mail = smtplib.SMTP(smtp_server, smtp_port)
        mail.starttls()  # 启用TLS
        # 登录邮箱
        your_email = app_config.email_account
        your_password = app_config.email_password
        mail.login(your_email, your_password)
        self.smtpSvc = mail

    def get_email_info(self, messages, num: int):
        """
        获取邮件信息：主题、发件人、日期及内容
        :param: messages: 邮件列表，num: 要提取的邮件数量
        :return: 包含(邮件ID, 主题, 发件人, 日期, 内容)的元组列表
        """
        email_info_list = []
        for i in messages[-num:]:
            status, message = self.imapSvc.fetch(i, '(RFC822)')
            msg = email.message_from_bytes(message[0][1])

            # 获取主题
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            # 获取发件人
            from_ = msg.get("From")

            # 获取日期
            date_ = msg.get("Date")
            try:
                date_ = parsedate_to_datetime(date_)
            except Exception as e:
                date_ = None  # 或者设置为一个默认值

            # 获取邮件内容，只提取第一部分
            content = ""
            if msg.is_multipart():
                first_part = msg.get_payload(0)
                if first_part.get_content_type() == "text/plain":
                    content = first_part.get_payload(decode=True).decode(first_part.get_content_charset() or 'utf-8')
            else:
                content = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

            email_info_list.append((i, subject, from_, date_, content))

        return email_info_list

    def get_email_message_list(self, unread_only=False):
        """
        Get the email message list, optionally only unread messages
        """
        self.imapSvc.select('INBOX')
        criteria = 'UNSEEN' if unread_only else 'ALL'
        status, messages = self.imapSvc.search(None, criteria)
        mailList = messages[0].split()
        return mailList

    def check_and_update_unread_emails(self):
        """
        Check for new unread emails, update the cache, and summarize them using AI.
        """
        # 获取所有未读邮件
        unread_email_ids = self.get_email_message_list(unread_only=True)
        new_unread_emails = [email_id for email_id in unread_email_ids if email_id not in self.unread_emails_cache]

        # 获取新未读邮件的信息
        if new_unread_emails:
            new_unread_emails_info = self.get_email_info(new_unread_emails, len(new_unread_emails))
            for info in new_unread_emails_info:
                id,subject, from_, date_ = info
                # 假设有一个AI模型来总结邮件，这里用伪代码表示
                # todo: 实现ai_summarize_email函数
                # summary = ai_summarize_email(subject, from_, date_)  # 需要实现此函数
                self.unread_emails_cache[id] = {""}

    def mark_emails_as_read(self):
        """
        Mark all unread emails as read at a fixed time each day.
        """
        self.check_and_update_unread_emails()
        # 根据缓存中的未读邮件ID，将其标记为已读
        for email_id in self.unread_emails_cache:
            self.imapSvc.store(email_id, '+FLAGS', '\\Seen')
        print("All unread emails have been marked")

    def send_email(self, to_email, subject, body):
        """
        Send an email
        :param to_email: Recipient email address
        :param subject: Email subject
        :param body: Email body
        """
        msg = MIMEMultipart()
        msg['From'] = app_config.email_account
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        try:
            self.smtpSvc.send_message(msg)
            return "Email sent successfully"
        except Exception as e:
            return f"Failed to send email: {e}"

