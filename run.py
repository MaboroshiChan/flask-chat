from flask import Flask, request, jsonify
import json
import logging as log
import gpt
import detector

app = Flask(__name__)

@app.route('/api/gpt3', methods=['POST'])
def gpt3():

    body = request.get_json()

    messages = body['messages']
    chat_id = body['chat_id']

    print(f"Chat ID: {chat_id}\n")
    print(f"Received messages: \n{messages}")

    det = detector.Detector()
    if det.detect_list([x['text'] for x in messages]):
        log.info("Detected keywords, not sending to GPT-3")
        return jsonify({
            "chat_id": chat_id,
            "message": [{
                "sender": "System",
                "text": "Detected keywords, not sending to GPT-3"
            }]
        })
    message: str = gpt.prepare_data(messages)
    
    sender_text = gpt.askAI(message)

    print("Answer: \n" + str(sender_text))

    resp = {
        "chat_id": chat_id,
        "message": [sender_text]
    }

    log.info("Answer: \n" + str(resp))
    return jsonify(resp)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    log.info("Starting server")
    app.run(host='localhost', port=8000, debug=True)
