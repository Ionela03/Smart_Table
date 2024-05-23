import eventlet
eventlet.monkey_patch()

import subprocess
import os
import signal
import threading
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
current_process = None
process_lock = threading.Lock()

# Define the script directory relative to the current file
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), 'Games')

@app.route('/')
def index():
    return "Welcome to the Home Page!"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def signal_handler(sig, frame):
    print('Signal received, stopping...')
    global current_process
    with process_lock:
        if current_process and current_process.poll() is None:
            current_process.kill()
            current_process.wait()
            print("Process forcefully stopped.")
        exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@socketio.on('command')
def handle_command(command):
    global current_process
    with process_lock:
        print(f'Received command: {command}')
        
        if command == 'stop':
            if current_process and current_process.poll() is None:
                print("Attempting to stop the current script...")
                current_process.kill()
                current_process.wait()
                current_process = None
                print("Script successfully stopped.")
            socketio.emit('response', 'Current script stopped.')

        elif command.startswith('run:'):
            script_name = command.split('run:')[1]
            script_path = os.path.join(SCRIPT_DIR, script_name)
            
            if os.path.exists(script_path):
                if current_process and current_process.poll() is None:
                    print("Stopping the current script before starting a new one...")
                    current_process.kill()
                    current_process.wait()
                    current_process = None
                print(f"Starting new script: {script_path}")
                current_process = subprocess.Popen(['sudo', 'python3', script_path])
                print(f"Script {script_path} started.")
                socketio.emit('response', f'Script {script_path} started.')
            else:
                print(f"Script {script_path} not found.")
                socketio.emit('response', f'Script {script_path} not found.')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
