from flask import Flask, request, jsonify, stream_with_context, json
import logging as log
import gpt
import detector
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080'], supports_credentials=True) 

@app.route('/api/gpt3/stream', methods=['POST'])
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
            "warning": "Detected keywords, not sending to GPT-3"
        })
    message: str = gpt.prepare_data(messages)
    
    chunks = gpt.askAIStream(message)

    def generate():
        for chunk in chunks:
            print(f"Chunk: \n{chunk}")
            resp = {
                "chat_id": chat_id,
                "message": chunk
            }
            yield json.dumps(resp) + "\n"

    return app.response_class(stream_with_context(generate()))

@app.route('/api/gpt3', methods=['POST'])
def gpt3_single():
    
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
                "warning": "Detected keywords, not sending to GPT-3"
            })
        message: str = gpt.prepare_data(messages)
        response = gpt.askAI(message)

        log.info("Response: \n" + response)
        return jsonify({
            "chat_id": chat_id,
            "message": response
        })

@app.route('/ping', methods=['GET'])
def ping():
    pong = gpt.ping()
    return jsonify(pong)

@app.route('/ping/stream', methods=['GET'])
def ping_stream():
    pong = gpt.ping_stream()
    def generate():
        for chunk in pong:
            resp = {
                "chat_id": "ping",
                "message": chunk
            }
            yield json.dumps(resp) + "\n"
    return app.response_class(stream_with_context(generate()))



if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    log.info("Starting server")
    app.run(host='localhost', port=8000, debug=True)