from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    print("running")
    app.run(debug=True, host='0.0.0.0', port=2224, url_prefix='/market')
