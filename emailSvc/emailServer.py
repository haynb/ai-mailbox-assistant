import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from conf.conf import app_config
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class mailSvc:
    imapSvc = None
    stmpSvc = None
    action = None

    def __init__(self):
        self.initImap()
        self.initSmtp()
        pass

    def initImap(self):
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


    def initSmtp(self):
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

    def get_email_info(self,messages,num: int):
        """
        Get the email information: subject, from, date
        :param： messages, num
        :return: subject, from, date
        """
        email_info_list = []
        for i in messages[-num:]:
            status,message = self.imapSvc.fetch(i, '(RFC822)')
            msg = email.message_from_bytes(message[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            from_ = msg.get("From")
            date_ = msg.get("Date")
            date_ = parsedate_to_datetime(date_)
            email_info_list.append((subject, from_, date_))
        return email_info_list

    def get_email_message_list(self):
        """
        Get the email message
        :param mail: mailSvc
        :return: mailList
        """
        self.imapSvc.select('INBOX')
        status, messages = self.imapSvc.search(None, 'ALL')
        mailList = messages[0].split()
        return mailList

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