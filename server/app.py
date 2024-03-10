import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from parser.parser import Parser
from environment.ast import Ast
from environment.environment import Environment
from environment.execute import root_executer

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/ping')
def ping():
    return jsonify({'message': 'pong!'})


@app.route('/interpreter', methods=['POST'])
def interpreter():
    input_data = request.json.get('input')
    env = Environment(None, 'GLOBAL')
    ast = Ast()
    parser = Parser(ast)
    instructions = parser.interpretar(input_data)
    root_executer(instructions, ast, env)
    return jsonify({
        'output': ast.get_console(),
        'errors': ast.get_errors(),
        'symbolTable': []
    })


port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(debug=True, port=port)
