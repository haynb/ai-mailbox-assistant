import openai

client = openai.OpenAI(base_url='https://cfcus02.opapi.win/v1/', api_key='sk-hHXZ8sOTBc442d016471T3BlbKFJ13617D3C756a4e678C59')

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the user's location.",
                    },
                },
                "required": ["location", "format"],
            },
        }
    }
]


messages = [
    {"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.If no suitable function is found, returns null."},
    {"role": "user", "content": "What's the weather like today in Beijing?"}
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
def call_function_weather_api(function_name, **params):
    # 假设这是一个调用天气 API 的函数
    return f"Weather Info: 72°F and sunny in {params['location']}"

response_message = response.choices[0].message

tool_calls = response_message.tool_calls
if tool_calls:
    tool_call_id = tool_calls[0].id
    tool_function_name = tool_calls[0].function.name
    tool_query_string = eval(tool_calls[0].function.arguments)
    print(tool_call_id, tool_function_name, tool_query_string)
    if tool_function_name == "get_current_weather":
        weather_response = call_function_weather_api(tool_function_name, **tool_query_string)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_function_name,
            "content": weather_response
        })
        print(weather_response)







