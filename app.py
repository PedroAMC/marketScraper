from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app as your_app

app = Flask(__name__)

# Mount your Flask app under the desired URL prefix
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/myapp': your_app,
})

if __name__ == '__main__':
    app.run(debug=True, port=2224)
