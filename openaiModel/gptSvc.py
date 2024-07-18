import common.writeFile
from conf.conf import app_config
from .tools import tools
import openai
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class GptSvc:
    client = None
    tools = None
    messages = None

    def __init__(self, mailSvc):
        self.client = openai.OpenAI(base_url=app_config.openai_base_url, api_key=app_config.openai_key)
        self.tools = tools
        self.messages = [
            {"role": "system",
             "content": "You are a personal mailbox management assistant, helping users manage their mailboxes. You "
                        "have many tools to use. Don't make assumptions about what values to plug into functions. Ask "
                        "for clarification if a user request is ambiguous. If no suitable function is found, "
                        "returns null."}
        ]
        self.mailSvc = mailSvc
        pass

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def call_function(self, name: str, func):
        response = self.client.chat.completions.create(
            model=app_config.openai_default_model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto"
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            tool_function_name = tool_calls[0].function.name
            arguments = tool_calls[0].function.arguments.replace('false', 'False').replace('true', 'True')
            params = eval(arguments)
            if tool_function_name == name:
                return func(**params)
            else:
                return None

    def summarize_email(self, **params):
        if params['urgency']:
            self.notify_users()
            pass
        origin_data = self.mailSvc.get_email_info(params['email_id'].encode('utf-8'))
        common.writeFile.write_email_to_file(subject=origin_data[0], sender=origin_data[1], date=origin_data[2],
                                             summary=params['summarize'], file_path=app_config.content_file_path)
        print(params)
        if params['scheduled']:
            run_time = datetime.fromisoformat(params['time'])
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.scheduled_task, 'date', run_date=run_time)
            scheduler.start()

    def notify_users(self):
        # todo 写入文件以及根据Urgency决定后续处理方式
        pass

    def scheduled_task(self):
        print("任务执行了！")
        # 定时提醒用户
        self.notify_users()

