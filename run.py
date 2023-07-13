from flask import Flask, request, jsonify, stream_with_context, json, render_template
import logging as log
import gpt
import detector
from flask_cors import CORS
from flask_socketio import SocketIO, emit


app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:8000', ' http://127.0.0.1:8081','http://localhost:8081'], supports_credentials=True, methods=['GET', 'POST']) 
socketio = SocketIO(engineio_logger=True)
socketio.init_app(app, cors_allowed_origins="*", async_mode='threading',transports=['websocket'])

def process_messages(chat_id: str, messages: list[dict[str, str]]):
    det = detector.Detector()
    if det.detect_list([x['text'] for x in messages]):
        log.info("Detected keywords, not sending to GPT-3")
        return jsonify({
            "chat_id": 'System',
            "warning": "Detected keywords, not sending to GPT-3"
        })
    message: str = gpt.prepare_data(messages)
    chunks = gpt.askAIStream(message)
    return chunks

@app.route('/')
def index():
    print("Sucessfully connected to server")
    return 'hello world'

@app.route('/api/gpt3/stream', methods=['POST'])
def gpt3():

    body = request.get_json()

    messages = body['messages']
    chat_id = body['chat_id']

    print(f"Chat ID: {chat_id}\n")
    print(f"Received messages: \n{messages}")

    chunks = process_messages(chat_id, messages)

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
        response: dict[str, str] = gpt.askAI(message)

        log.info("Response: \n" + str(response))
        return jsonify({
            "chat_id": chat_id,
            "message": response
        })

@app.route('/api/feedback', methods=['POST'])
def feedback():
    body = request.get_json()
    message = body['message']
    chat_id = body['chat_id']
    usr_id = body['usr_id']
    log.info("Feedback received from user {usr_id} in chat {chat_id}: \n{message}"
             .format(usr_id=usr_id, chat_id=chat_id, message=message))

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

# websocket
@socketio.on('connect', namespace='/websocket')
def connect(data):
    usr_id = data['usr_id']
    log.info("Client connected: {usr_id}".format(usr_id=usr_id))
    emit('response', {'data': 'Connected', 'count': 0})

# websocket
@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    # feed data to GPT-3
    messages = data['messages']
    chat_id = data['chat_id']

    chunks = process_messages(chat_id, messages)
    # send data to client
    for chunk in chunks:
        resp = {
            "chat_id": chat_id,
            "response": chunk
        }
        emit('message', resp, broadcast=True)

# websocket
@socketio.on('disconnect')
def disconnect():
    log.info("Client disconnected")


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    log.info("Starting server")
    app.run(host='localhost', port=8000, debug=True)
    #socketio.run(app, host='127.0.0.1', port=9000, debug=True)