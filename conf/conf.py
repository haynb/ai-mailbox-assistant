import configparser


class configApp :
    email_account = ""
    email_password = ""
    email_server = ""
    email_port = 0

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("conf/config.ini")
        self.email_account = config.get("email", "account")
        self.email_password = config.get("email", "password")
        self.email_imap_server = config.get("email", "imapServer")
        self.email_imap_port = config.getint("email", "imapPort")
        self.email_smtp_server = config.get("email", "smtpServer")
        self.email_smtp_port = config.getint("email", "smtpPort")


# 实例化 configApp 类
app_config = configApp()