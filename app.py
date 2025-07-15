from models import db
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'secret_key'

db.init_app(app)

@app.route('/')
def index():
    return "Welcome to the World Building Manager!"

if __name__ == '__main__':
    app.run(debug=True)