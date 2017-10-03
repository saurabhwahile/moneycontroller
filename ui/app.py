from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit


app = Flask(__name__, template_folder='.')
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)