from flask import Flask, render_template, request, jsonify
from lark import Lark, Transformer, Token
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

grammar = r"""
    ?start: expr
    ?expr: term
         | expr "+" term   -> add
         | expr "-" term   -> sub
    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div
    ?factor: NUMBER        -> number
           | "(" expr ")"  -> parenthesis
    NUMBER: /-?\d*\.?\d+/
    %import common.WS
    %ignore WS
"""
parser = Lark(grammar, parser='lalr')

class TokenCollector:
    def __init__(self):
        self.tokens = []

    def process_token(self, value, token_type):
        if isinstance(value, (int, float)):
            tipo = "NUMERO " + ("FLOTANTE" if isinstance(value, float) or '.' in str(value) else "ENTERO")
        else:
            operators = {
                '+': 'SUMA', 
                '-': 'RESTA', 
                '*': 'MULTIPLICACIÓN', 
                '/': 'DIVISIÓN', 
                '(': 'PARÉNTESIS APERTURA',
                ')': 'PARÉNTESIS CIERRE'
            }
            tipo = f"OPERADOR {operators.get(value, '')}"
        
        self.tokens.append({
            "value": value,
            "type": tipo
        })

class TreeBuilder(Transformer):
    def __init__(self):
        self.token_collector = TokenCollector()
        super().__init__()

    def number(self, n):
        value = float(n[0].value)
        self.token_collector.process_token(value, "number")
        return {"type": "number", "value": value}

    def add(self, args):
        self.token_collector.process_token("+", "operator")
        return {"type": "add", "left": args[0], "right": args[1]}
    
    def sub(self, args):
        self.token_collector.process_token("-", "operator")
        return {"type": "sub", "left": args[0], "right": args[1]}

    def mul(self, args):
        self.token_collector.process_token("*", "operator")
        return {"type": "mul", "left": args[0], "right": args[1]}

    def div(self, args):
        self.token_collector.process_token("/", "operator")
        return {"type": "div", "left": args[0], "right": args[1]}

    def parenthesis(self, args):
        # Paréntesis no añaden nada adicional al árbol
        self.token_collector.process_token("(", "operator")
        self.token_collector.process_token(")", "operator")
        return args[0]

class Evaluator(Transformer):
    def number(self, n):
        return float(n[0].value)

    def add(self, args):
        # Asegurarse de que los argumentos son flotantes
        return float(args[0]) + float(args[1])
    
    def sub(self, args):
        return float(args[0]) - float(args[1])

    def mul(self, args):
        return float(args[0]) * float(args[1])

    def div(self, args):
        # Manejar la división con conversión explícita a flotante
        divisor = float(args[1])
        if divisor == 0:
            raise ValueError("División por cero")
        return float(args[0]) / divisor

    def parenthesis(self, args):
        # Devolver el valor dentro de los paréntesis
        return args[0]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    expression = data.get('expression')
    if not expression:
        return jsonify({'treeHTML': '', 'result': '', 'tokens': []})

    try:
        tree = parser.parse(expression)
        tree_builder = TreeBuilder()
        transformed_tree = tree_builder.transform(tree)
        
        # Render tree HTML
        tree_html = render_tree(transformed_tree)
        
        # Evaluate expression
        result = Evaluator().transform(tree)
        
        # Round result to avoid floating-point imprecision
        result = round(result, 10)
        
        return jsonify({
            'treeHTML': tree_html, 
            'result': str(result),
            'tokens': tree_builder.token_collector.tokens
        })
    except ZeroDivisionError:
        return jsonify({
            'treeHTML': '<p>Error: División por cero</p>', 
            'result': '', 
            'tokens': []
        })
    except Exception as e:
        return jsonify({
            'treeHTML': f'<p>Error: {str(e)}</p>', 
            'result': '', 
            'tokens': []
        })
        

def render_tree(node):
    if node['type'] == 'number':
        return f'''
            <div class="node-container">
                <div class="node">{node["value"]}</div>
            </div>
        '''
    
    operators = {
        'add': '+', 
        'sub': '-', 
        'mul': '×', 
        'div': '÷'
    }
    
    operator = operators.get(node['type'], '')
    left = render_tree(node['left'])
    right = render_tree(node['right'])
    
    return f'''
        <div class="node-container">
            <div class="node operator">{operator}</div>
            <div class="children">
                <div class="left">{left}</div>
                <div class="right">{right}</div>
            </div>
        </div>
    '''

if __name__ == '__main__':
    app.run(debug=True)

    
from flask import Flask, render_template, request, jsonify
from lark import Lark, Transformer, Token
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

grammar = r"""
    ?start: expr
    ?expr: term
         | expr "+" term   -> add
         | expr "-" term   -> sub
    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div
    ?factor: NUMBER        -> number
           | "(" expr ")"  -> parenthesis
    NUMBER: /-?\d*\.?\d+/
    %import common.WS
    %ignore WS
"""
parser = Lark(grammar, parser='lalr')

class TokenCollector:
    def __init__(self):
        self.tokens = []

    def process_token(self, value, token_type):
        if isinstance(value, (int, float)):
            tipo = "NUMERO " + ("FLOTANTE" if isinstance(value, float) or '.' in str(value) else "ENTERO")
        else:
            operators = {
                '+': 'SUMA', 
                '-': 'RESTA', 
                '*': 'MULTIPLICACIÓN', 
                '/': 'DIVISIÓN', 
                '(': 'PARÉNTESIS APERTURA',
                ')': 'PARÉNTESIS CIERRE'
            }
            tipo = f"OPERADOR {operators.get(value, '')}"
        
        self.tokens.append({
            "value": value,
            "type": tipo
        })

class TreeBuilder(Transformer):
    def __init__(self):
        self.token_collector = TokenCollector()
        super().__init__()

    def number(self, n):
        value = float(n[0].value)
        self.token_collector.process_token(value, "number")
        return {"type": "number", "value": value}

    def add(self, args):
        self.token_collector.process_token("+", "operator")
        return {"type": "add", "left": args[0], "right": args[1]}
    
    def sub(self, args):
        self.token_collector.process_token("-", "operator")
        return {"type": "sub", "left": args[0], "right": args[1]}

    def mul(self, args):
        self.token_collector.process_token("*", "operator")
        return {"type": "mul", "left": args[0], "right": args[1]}

    def div(self, args):
        self.token_collector.process_token("/", "operator")
        return {"type": "div", "left": args[0], "right": args[1]}

    def parenthesis(self, args):
        # Paréntesis no añaden nada adicional al árbol
        self.token_collector.process_token("(", "operator")
        self.token_collector.process_token(")", "operator")
        return args[0]

class Evaluator(Transformer):
    def number(self, n):
        return float(n[0].value)

    def add(self, args):
        return args[0] + args[1]
    
    def sub(self, args):
        return args[0] - args[1]

    def mul(self, args):
        return args[0] * args[1]

    def div(self, args):
        return args[0] / args[1]

    # El método de paréntesis ya está implícito en la evaluación
    # por la estructura recursiva del árbol