tools = [
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
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_email",
            "description": "Summarizes the content of an email and provides additional context about its importance "
                           "and urgency. This function helps users quickly understand the essence of an email and "
                           "prioritize their responses effectively.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summarize": {
                        "type": "string",
                        "description": "A concise summary of the email content, highlighting the main points, "
                                       "purpose, and any key actions or information contained within the email.The "
                                       "second part is your suggestion on this email, such as how to handle it or how "
                                       "to reply to it. (If it is not necessary to handle it, do not add this part)"
                    },
                    "importance": {
                        "type": "string",
                        "description": "An assessment of the email's importance on a scale from 1 to 10, where 1 "
                                       "indicates low importance and 10 indicates high importance. This helps "
                                       "recipients gauge the priority level of the email."
                    },
                    "urgency": {
                        "type": "boolean",
                        "description": "True or False.A boolean value indicating whether the email requires immediate "
                                       "attention or action. If set to true, it signifies that the email is urgent "
                                       "and should be addressed as soon as possible."
                    }
                },
                "required": ["summarize", "importance", "urgency"]
            }
        }
    }
]