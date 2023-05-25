from flask import Flask, request, jsonify
import json
import logging as log
import core

app = Flask(__name__)

@app.route('/gpt3', methods=['POST'])
def gpt3():
    messages = request.form.get('messages')
    chat_id = request.form.get('chat_id')

    msg_model: dict[str, str] = json.loads(messages)

    log.info("Received messages: \n" + msg_model)

    message: str = core.gpt.prepare_data(msg_model)
    answer = core.gpt.askAI(message)

    resp = {
        "chat_id": chat_id,
        "message": answer
    }

    log.info("Answer: \n" + resp)
    return jsonify(answer)


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    log.info("Starting server")
    app.run(host='localhost', port=8000, debug=True)
