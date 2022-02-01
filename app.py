from ast import Expression
from flask import Flask, request, abort
from ParallelCalculator import ParallelCalculator


app = Flask(__name__)


@app.route('/evaluate', methods = ['POST'])
def evaluate():
    try:
        input_data = request.get_json(force=True)
        calc = ParallelCalculator()
        res = calc.count_value_from_string(input_data['expression'])
        return {"result":str(res)}
    except:
        abort(400, description="Bad Request")