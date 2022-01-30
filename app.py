from ast import Expression
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/evaluate', methods = ['POST'])
def evaluate():
    try:
        input_data = request.get_json(force=True)
        return input_data
    except:
        abort(400, description="Bad Request")