from flask import Flask

app = Flask(__name__)

@app.route('/message', methods=['GET'])
def get_static_message():
    return "not implemented yet"

if __name__ == '__main__':
    app.run(port=5002, debug=True)
