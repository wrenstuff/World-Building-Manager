from models import db
from flask import Flask, render_template, request, redirect, url_for

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

# Routes for creating, viewing, editing, and deleting entries
# Put new templates in the respective folders located under 'templates/'
# And enter the routes alphabetically

# Events
@app.route('/create-event', methods=['GET','POST'])
def create_event():
    if request.method == 'POST':
        world_id = request.form['world_id']
        event_name = request.form['event_name']
        event_description = request.form.get('event_description', '')
        event_date = request.form.get('event_date', '')
        event_notes = request.form.get('event_notes', '')
        
        if not world_id or not event_name:
            return "World ID and Name are required", 400
        
        new_event = Events(world_id=world_id, 
                           name=event_name, 
                           description=event_description, 
                           date=event_date, 
                           notes=event_notes)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('DB_Status'))
    return render_template('create/create-event.html')

@app.route('/delete-event/<int:event_id>', methods=['GET','POST'])
def delete_event(event_id):
    event = Events.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('DB_Status'))

@app.route('/view-event/<int:event_id>', methods=['GET','POST'])
def view_event(event_id):
    event = Events.query.get(event_id)
    if not event:
        return "Event not found", 404
    return render_template('view/view-event.html', event=event)

@app.route('/edit-event/<int:event_id>', methods=['GET','POST'])
def edit_event(event_id):
    event = Events.query.get(event_id)
    if not event:
        return "Event not found", 404
    
    if request.method == 'POST':
        event.name = request.form['event_name']
        event.description = request.form.get('event_description', '')
        event.date = request.form.get('event_date', '')
        event.notes = request.form.get('event_notes', '')

        db.session.commit()
        return redirect(url_for('DB_Status'))
    
    return render_template('edit/edit-event.html', event=event)


# Races
@app.route('/create-race', methods=['GET','POST'])
def create_race():
    if request.method == 'POST':
        world_id = request.form['world_id']
        race_name = request.form['race_name']
        race_description = request.form.get('race_description', '')
        race_traits = request.form.get('race_traits', '')
        race_notes = request.form.get('race_notes', '')

        if not world_id or not race_name:
            return "World ID and Name are required", 400
        
        new_race = Races(world_id=world_id,
                         name=race_name,
                         description=race_description,
                         traits=race_traits,
                         notes=race_notes)
        db.session.add(new_race)
        db.session.commit()
        return redirect(url_for('DB_Status'))
    return render_template('create/create-race.html')

@app.route('/delete-race/<int:race_id>', methods=['GET','POST'])
def delete_race(race_id):
    race = Races.query.get(race_id)
    if race:
        db.session.delete(race)
        db.session.commit()
    return redirect(url_for('DB_Status'))

@app.route('/view-race/<int:race_id>', methods=['GET','POST'])
def view_race(race_id):
    race = Races.query.get(race_id)
    if not race:
        return "Race not found", 404
    return render_template('view/view-race.html', race=race)

@app.route('/edit-race/<int:race_id>', methods=['GET','POST'])
def edit_race(race_id):
    race = Races.query.get(race_id)
    if not race:
        return "Race not found", 404
    
    if request.method == 'POST':
        race.name = request.form['race_name']
        race.description = request.form.get('race_description', '')
        race.traits = request.form.get('race.traits', '')
        race.notes = request.form.get('race_notes', '')

        db.session.commit()
        return redirect(url_for('DB_Status'))
    
    return render_template('edit/edit-race.html', race=race)


# Religions
@app.route('/create-religion', methods=['GET','POST'])
def create_religion():
    if request.method == 'POST':
        world_id = request.form['world_id']
        religion_name = request.form['religion_name']
        religion_description = request.form.get('religion_description', '')
        religion_beliefs = request.form.get('religion_beliefs', '')
        religion_notes = request.form.get('religion_notes', '')

        if not world_id or not religion_name:
            return "World ID and Name are required", 400
        
        new_religion = Religions(world_id=world_id,
                                 name=religion_name,
                                 description=religion_description,
                                 beliefs=religion_beliefs,
                                 notes=religion_notes)
        db.session.add(new_religion)
        db.session.commit()
        return redirect(url_for('DB_Status'))
    return render_template('create/create-religion.html')

@app.route('/delete-religion/<int:religion_id>', methods=['GET','POST'])
def delete_religion(religion_id):
    religion = Religions.query.get(religion_id)
    if religion:
        db.session.delete(religion)
        db.session.commit()
    return redirect(url_for('DB_Status'))

@app.route('/view-religion/<int:religion_id>', methods=['GET','POST'])
def view_religion(religion_id):
    religion = Religions.query.get(religion_id)
    if not religion:
        return "Religion not found", 404
    return render_template('view/view-religion.html', religion=religion)

@app.route('/edit-religion/<int:religion_id>', methods=['GET','POST'])
def edit_religion(religion_id):
    religion = Religions.query.get(religion_id)
    if not religion:
        return "Religion not found", 404

    if request.method == 'POST':
        religion.name = request.form['religion_name']
        religion.description = request.form.get('religion_description', '')
        religion.beliefs = request.form.get('religion_beliefs', '')
        religion.notes = request.form.get('religion_notes', '')
        
        db.session.commit()
        return redirect(url_for('DB_Status'))

    return render_template('edit/edit-religion.html', religion=religion)


# Settlements
@app.route('/create-settlement', methods=['GET','POST'])
def create_settlement():
    if request.method == 'POST':
        world_id = request.form['world_id']
        settlement_name = request.form['settlement_name']
        settlement_description = request.form.get('settlement_description', '')
        settlement_notes = request.form.get('settlement_notes', '')

        if not world_id or not settlement_name:
            return "World ID and Name are required", 400
        
        new_settlement = Settlements(world_id=world_id,
                                     name=settlement_name,
                                     description=settlement_description,
                                     notes=settlement_notes)
        db.session.add(new_settlement)
        db.session.commit()
        return redirect(url_for('DB_Status'))
    return render_template('create/create-settlement.html')

@app.route('/delete-settlement/<int:settlement_id>', methods=['GET','POST'])
def delete_settlement(settlement_id):
    settlement = Settlements.query.get(settlement_id)
    if settlement:
        db.session.delete(settlement)
        db.session.commit()
    return redirect(url_for('DB_Status'))

@app.route('/view-settlement/<int:settlement_id>', methods=['GET','POST'])
def view_settlement(settlement_id):
    settlement = Settlements.query.get(settlement_id)
    if not settlement:
        return "Settlement not found", 404
    return render_template('view/view-settlement.html', settlement=settlement)

@app.route('/edit-settlement/<int:settlement_id>', methods=['GET','POST'])
def edit_settlement(settlement_id):
    settlement = Settlements.query.get(settlement_id)
    if not settlement:
        return "Settlement not found", 404

    if request.method == 'POST':
        settlement.name = request.form['settlement_name']
        settlement.description = request.form.get('settlement_description', '')
        settlement.notes = request.form.get('settlement_notes', '')
        
        db.session.commit()
        return redirect(url_for('DB_Status'))

    return render_template('edit/edit-settlement.html', settlement=settlement)


# Worlds
@app.route('/create-world', methods=['GET','POST'])
def create_world():
    if request.method == 'POST':
        world_name = request.form['world_name']
        world_description = request.form.get('world_description', '')
        world_notes = request.form.get('world_notes', '')

        if not world_name:
            return "World name is required", 400

        new_world = Worlds(name=world_name, 
                           description=world_description, 
                           notes=world_notes)
        db.session.add(new_world)
        db.session.commit()
        return redirect(url_for('DB_Status'))
    return render_template('create/create-world.html')

@app.route('/delete-world/<int:world_id>', methods=['GET','POST'])
def delete_world(world_id):
    world = Worlds.query.get(world_id)
    if world:
        db.session.delete(world)
        db.session.commit()
    return redirect(url_for('DB_Status'))

@app.route('/view-world/<int:world_id>', methods=['GET','POST'])
def view_world(world_id):
    world = Worlds.query.get(world_id)
    if not world:
        return "World not found", 404
    return render_template('view/view-world.html', world=world)

@app.route('/edit-world/<int:world_id>', methods=['GET','POST'])
def edit_world(world_id):
    world = Worlds.query.get(world_id)
    if not world:
        return "World not found", 404

    if request.method == 'POST':
        world.name = request.form['world_name']
        world.description = request.form.get('world_description', '')
        world.notes = request.form.get('world_notes', '')
        
        db.session.commit()
        return redirect(url_for('DB_Status'))

    return render_template('edit/edit-world.html', world=world)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)