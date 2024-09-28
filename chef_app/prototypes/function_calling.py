from openai import OpenAI
import random
import json

class ChefClient:
    def __init__(self, client):
        self.functions = []
        self.client = client

        function_defs = [
            {
                "function": self.random_number,
                "description": "Generate a random number between 1 and 100",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
                "return_type": "int",
            },
            {
                "function": self.convert_names,
                "description": "Converts human names to codewords. If the codeword is unknown, tell the user that it's unknown.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the person",
                        }
                    },
                    "required": ["name"],
                    "additionalProperties": False,
                },
                "return_type": "string",
            }
        ]


        for function_def in function_defs:
            self.functions.append(
                {
                    "type": "function",
                    "function": {
                        "name": function_def["function"].__name__,
                        "description": function_def["description"],
                        "parameters": function_def["parameters"],
                        "return_type": function_def["return_type"],
                    }
                }
            )
        
        self.messages = [
            {"role": "system", "content": "You\'re an assistant that has an ability to interact with websites"},
        ]

    def random_number(self) -> int:
        return random.randint(1, 100)

    def convert_names(self, name: str) -> str:
        d = {
            "Janek": "apple",
            "Piotrek": "banana",
            "Adam": "citroen"
        }

        if name in d:
            return d[name]
        else:
            return "unknown"
    
    def handle_function(self, function):
        if function.name == "random_number":
            return self.random_number()
        elif function.name == "convert_names":
            print(function)
            arguments = json.loads(function.arguments)
            return self.convert_names(**arguments)

        return None
    
    def query(self):
        return self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-3.5-turbo",
            tools=self.functions,
        )

br = False

openai_client = OpenAI()
client = ChefClient(openai_client)

while not br:
    user_input = input("> ")
    
    if user_input.lower() == "exit":
        break

    client.messages.append({"role": "user", "content": user_input})

    chat_completion = client.query()
    
    client.messages.append(chat_completion.choices[0].message)

    tool_calls = chat_completion.choices[0].message.tool_calls
    if (tool_calls is not None):
        for i in range(len(tool_calls)):
            function = tool_calls[i].function

            client.messages.append({
                "role": "tool",
                "content": json.dumps(client.handle_function(function)),
                "tool_call_id": tool_calls[i].id
            })

        chat_completion = client.query()

        client.messages.append(chat_completion.choices[0].message)
        print(chat_completion.choices[0].message.content)
    else:
        print(chat_completion.choices[0].message.content)

