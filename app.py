from models import db
from flask import Flask, render_template

from models import Events
from models import Races
from models import Religions
from models import Settlements
from models import Worlds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'secret_key'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def DB_Status():
    events = Events.query.all()
    races = Races.query.all()
    religions = Religions.query.all()
    settlements = Settlements.query.all()
    worlds = Worlds.query.all()

    return render_template('db-status.html', 
                           events=events, 
                           races=races, 
                           religions=religions, 
                           settlements=settlements, 
                           worlds=worlds)

if __name__ == '__main__':
    app.run(debug=True)