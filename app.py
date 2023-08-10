from flask import Flask, Blueprint

app = Flask(__name__)

# Define your Flask routes
@app.route('/myapp/')
def myapp_home():
    return "Hello, this is my Flask app hosted under /myapp!"

# You can define more routes here

if __name__ == '__main__':
    app.run(debug=True, port=2224)
