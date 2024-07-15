from conf.conf import app_config
from .tools import tools
import openai


class GptSvc:
    client = None
    tools = None
    messages = None

    def __init__(self):
        self.client = openai.OpenAI(base_url=app_config.openai_base_url, api_key=app_config.openai_key)
        self.tools = tools
        self.messages = [
            {"role": "system",
             "content": "You are a personal mailbox management assistant, helping users manage their mailboxes. You "
                        "have many tools to use. Don't make assumptions about what values to plug into functions. Ask "
                        "for clarification if a user request is ambiguous. If no suitable function is found, "
                        "returns null."}
        ]
        pass

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def call_function(self):
        response = self.client.chat.completions.create(
            model=app_config.openai_default_model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto"
        )
        response_message = response.choices[0].message
        return response_message

    def summarize_email(self, **params):
        print( f"Summarize: {params['summarize']} \n, Importance: {params['importance']} \n, Urgency: {params['urgency']} \n")
