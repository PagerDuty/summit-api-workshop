from os import environ as ENV
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/hello-world', methods=['GET'])
def hello_world_route():
    return f"Hello, World. {ENV.get('TEST_KEY')}"

if __name__ == "__main__":
    app.run(debug=True)
