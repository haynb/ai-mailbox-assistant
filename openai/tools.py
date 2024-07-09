tools = [
    {
        "type": "function",
        "function": {
            "name": "get_email_info",
            "description": "Get the email information including subject, sender, and date",
            "parameters": {
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "description": "List of email message identifiers",
                    },
                    "num": {
                        "type": "integer",
                        "description": "Number of recent emails to fetch information for",
                    },
                },
                "required": ["messages", "num"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_email_message_list",
            "description": "Retrieve a list of all email messages from the inbox",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a specified recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient's email address",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject of the email",
                    },
                    "body": {
                        "type": "string",
                        "description": "Body content of the email",
                    },
                },
                "required": ["to_email", "subject", "body"]
            },
        }
    }
]