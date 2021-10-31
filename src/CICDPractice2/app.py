from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/foo")
def foo():
    return "1000000"

@app.route("/bar")
def bar():
    return "Bar"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
