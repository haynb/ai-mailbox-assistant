import configparser


class ConfigApp :
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("conf/config.ini")
        self.email_account = config.get("email", "account")
        self.email_password = config.get("email", "password")
        self.email_imap_server = config.get("email", "imapServer")
        self.email_imap_port = config.getint("email", "imapPort")
        self.email_smtp_server = config.get("email", "smtpServer")
        self.email_smtp_port = config.getint("email", "smtpPort")
        self.openai_key = config.get("openai", "openai_key")
        self.openai_default_model = config.get("openai", "openai_default_model")
        self.openai_base_url = config.get("openai", "openai_base_url")
        self.content_file_path = config.get("common", "content_file_path")


# 实例化 configApp 类
app_config = ConfigApp()