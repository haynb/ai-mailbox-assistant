from conf.conf import app_config
# from tools import tools as my_tools
import tools
import openai


class GptSvc:
    client = None
    tools = None
    messages = None

    def __init__(self):
        self.client = openai.OpenAI(base_url=app_config.openai_base_url, api_key=app_config.openai_key)
        self.tools = tools
        self.messages = [
            {"role": "system", "content": "You are a personal mailbox management assistant, helping users manage their mailboxes. You have many tools to use. Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous. If no suitable function is found, returns null."}
        ]
        pass



