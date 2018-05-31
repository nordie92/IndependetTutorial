from flask import Flask, send_file
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    sio = StringIO()
    sio.write('print("hello world")')
    sio.seek(0)
    return send_file(sio, attachment_filename="clnt.py")

app.run(debug=True)