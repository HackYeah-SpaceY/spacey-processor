# A Flask app here

# /new_cshat(url, id)
# /send_message(id, message) 
import uuid
from flask import Flask, jsonify
from flask import request
from openai import OpenAI
import json
from flask_cors import CORS
from chef_client import ChefClient
import asyncio
import cloudinary.uploader
import os

def create_app():
    app = Flask(__name__)
    state = {}
    openai_client = OpenAI()
    cloudinary.config( 
        cloud_name = "dqqmqkz28", 
        api_key = os.environ['CLOUDINARY_API_KEY'],
        api_secret = os.environ['CLOUDINARY_API_SECRET'], # Click 'View API Keys' above to copy your API secret
        secure=True
    )
    loop = asyncio.get_event_loop()

    # Url and id in query
    @app.route("/new_chat", methods=['POST'])
    def new_chat():
        data = request.json
        url = data.get("url")
        id = data.get("id")
        if not url or not id:
            return jsonify({"status": "error", "error": "Missing url or id"}), 400
        

        client = loop.run_until_complete(ChefClient(openai_client, url).__aenter__())

        state[id] = client

        return jsonify({"status": "ok", "response": f"Chat created with url: {url} and id: {id}"}), 200

    @app.route("/message", methods=['POST'])
    def send_message():
        data = request.json
        id = data.get("id")
        message = data.get("message")
        if not message or not id:
            return jsonify({"status": "error", "error": "Missing id or message"}), 400

        if id not in state:
            return jsonify({"status": "error", "error": "Chat not found"}), 404
        
        current_state = state[id]

        current_state.messages.append({"role": "user", "content": message})

        chat_completion = loop.run_until_complete(current_state.query())
        
        current_state.messages.append(chat_completion.choices[0].message)

        tool_calls = chat_completion.choices[0].message.tool_calls
        if (tool_calls is not None):
            for i in range(len(tool_calls)):
                function = tool_calls[i].function

                current_state.messages.append({
                    "role": "tool",
                    "content": json.dumps(loop.run_until_complete(current_state.handle_function(function))),
                    "tool_call_id": tool_calls[i].id
                })

            chat_completion = loop.run_until_complete(current_state.query())

            current_state.messages.append(chat_completion.choices[0].message)
            print(chat_completion.choices[0].message.content)
        else:
            print(chat_completion.choices[0].message.content)

        loop.run_until_complete(current_state.save_screenshot())

        upload_result = cloudinary.uploader.upload("screenshot.jpg", 
            asset_folder = "pets",
            # Random uuid 
            public_id = f"{uuid.uuid4()}",
            overwrite = True, 
            resource_type = "image")
        print(upload_result["secure_url"])
        
        state[id] = current_state
        return jsonify(
            {"status": "ok", "response": chat_completion.choices[0].message.content, "screenshot": upload_result["secure_url"]}
        ), 200
    
    return app

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000, threaded=True)
