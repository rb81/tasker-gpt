from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from .main import process_objective
import logging
import os

# Suppress httpx logs
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

app = Flask(__name__)

# Detect if running with Gunicorn or Python -m
if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
    # Use eventlet for Gunicorn
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
else:
    # Use threading for Python -m
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Custom logging handler to emit logs to SocketIO
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit('log', {'message': log_entry})

# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add the SocketIOHandler to the root logger
logger.addHandler(SocketIOHandler())

# Add a StreamHandler to the root logger for console output
logger.addHandler(logging.StreamHandler())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        objective = request.json['objective']
        result = process_objective(objective, logger)  # Pass the logger to process_objective
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error processing objective: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the objective'}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
