from models import db
from flask import Flask, render_template, request, redirect, url_for, session
import os
import re

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

if not os.path.exists('static/notes'):
    os.makedirs('static/notes')

def clean_filename(filename):
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)

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
        last_event_id = Events.query.order_by(Events.id.desc()).first()
        event_id = last_event_id.id + 1 if last_event_id else 1
        event_notes_file_name = str(world_id) + '-' + str(event_id) + '-event-' + clean_filename(event_name) + '-notes.md'
        event_notes_link = f'static/notes/{event_notes_file_name}'
        
        if not world_id or not event_name:
            return "World ID and Name are required", 400
        
        if event_name in [e.name for e in Events.query.filter_by(world_id=world_id).all()]:
            return "Event with this name already exists in the selected world", 400
        else:
            new_event = Events(world_id=world_id, 
                            name=event_name, 
                            description=event_description, 
                            date=event_date, 
                            notes=event_notes_link)
            
            notes_dir = os.path.dirname(event_notes_link)
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)

            with open(event_notes_link, 'w', encoding='utf-8') as notes_file:
                notes_file.write(event_notes)

            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('DB_Status'))
    return render_template('create/create-event.html')

@app.route('/delete-event/<int:event_id>', methods=['GET','POST'])
def delete_event(event_id):
    event = Events.query.get(event_id)

    if event and event.notes:
        notes_file_path = os.path.join('static', event.notes)
        if os.path.exists(event.notes):
            os.remove(event.notes)

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
        last_race_id = Races.query.order_by(Races.id.desc()).first()
        race_id = last_race_id.id + 1 if last_race_id else 1
        race_notes_file_name = str(world_id) + '-' + str(race_name) + '-race-' + clean_filename(race_name) + '-notes.md'
        race_notes_link = f'static/notes/{race_notes_file_name}'

        if not world_id or not race_name:
            return "World ID and Name are required", 400
        
        if race_name in [r.name for r in Races.query.filter_by(world_id=world_id).all()]:
            return "Race with this name already exists in the selected world", 400
        else:        
            new_race = Races(world_id=world_id,
                            name=race_name,
                            description=race_description,
                            traits=race_traits,
                            notes=race_notes_link)
            
            notes_dir = os.path.dirname(race_notes_link)
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)
            
            with open(race_notes_link, 'w', encoding='utf-8') as notes_file:
                notes_file.write(race_notes)

            db.session.add(new_race)
            db.session.commit()
            return redirect(url_for('DB_Status'))
    return render_template('create/create-race.html')

@app.route('/delete-race/<int:race_id>', methods=['GET','POST'])
def delete_race(race_id):
    race = Races.query.get(race_id)

    if race and race.notes:
        notes_file_path = os.path.join('static', race.notes)
        if os.path.exists(race.notes):
            os.remove(race.notes)

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
        last_religion_id = Religions.query.order_by(Religions.id.desc()).first()
        religion_id = last_religion_id.id + 1 if last_religion_id else 1
        religion_notes_file_name = str(world_id) + '-' + str(religion_id) + '-religion-' + clean_filename(religion_name) + '-notes.md'
        religion_notes_link = f'static/notes/{religion_notes_file_name}'

        if not world_id or not religion_name:
            return "World ID and Name are required", 400
        
        if religion_name in [r.name for r in Religions.query.filter_by(world_id=world_id).all()]:
            return "Religion with this name already exists in the selected world", 400
        else:
        
            new_religion = Religions(world_id=world_id,
                                    name=religion_name,
                                    description=religion_description,
                                    beliefs=religion_beliefs,
                                    notes=religion_notes_link)
            db.session.add(new_religion)
            db.session.commit()
        
            notes_dir = os.path.dirname(religion_notes_link)
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)

            with open(religion_notes_link, 'w', encoding='utf-8') as notes_file:
                notes_file.write(religion_notes)


            return redirect(url_for('DB_Status'))
    return render_template('create/create-religion.html')

@app.route('/delete-religion/<int:religion_id>', methods=['GET','POST'])
def delete_religion(religion_id):
    religion = Religions.query.get(religion_id)

    if religion and religion.notes:
        notes_file_path = os.path.join('static', religion.notes)
        if os.path.exists(religion.notes):
            os.remove(religion.notes)

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
        last_settlement_id = Settlements.query.order_by(Settlements.id.desc()).first()
        settlement_id = last_settlement_id.id + 1 if last_settlement_id else 1
        settlement_notes_file_name = str(world_id) + '-' + str(settlement_id) + '-settlement-' + clean_filename(settlement_name) + '-notes.md'
        settlement_notes_link = f'static/notes/{settlement_notes_file_name}'

        if not world_id or not settlement_name:
            return "World ID and Name are required", 400
        
        if settlement_name in [s.name for s in Settlements.query.filter_by(world_id=world_id).all()]:
            return "Settlement with this name already exists in the selected world", 400
        else:
            new_settlement = Settlements(world_id=world_id,
                                        name=settlement_name,
                                        description=settlement_description,
                                        notes=settlement_notes_link)
            db.session.add(new_settlement)
            db.session.commit()

            notes_dir = os.path.dirname(settlement_notes_link)
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)

            with open(settlement_notes_link, 'w', encoding='utf-8') as notes_file:
                notes_file.write(settlement_notes)

            return redirect(url_for('DB_Status'))
    return render_template('create/create-settlement.html')

@app.route('/delete-settlement/<int:settlement_id>', methods=['GET','POST'])
def delete_settlement(settlement_id):
    settlement = Settlements.query.get(settlement_id)

    if settlement and settlement.notes:
        notes_file_path = os.path.join('static', settlement.notes)
        if os.path.exists(settlement.notes):
            os.remove(settlement.notes)

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
        last_world_id = Worlds.query.order_by(Worlds.id.desc()).first()
        world_id = last_world_id.id + 1 if last_world_id else 1
        world_notes_file_name = str(world_id) + '-world-' + clean_filename(world_name) + '-notes.md'
        world_notes_link = f'static/notes/{world_notes_file_name}'

        if not world_name:
            return "World name is required", 400
        
        if world_name in [w.name for w in Worlds.query.all()]:
            return "World with this name already exists", 400
        else:
            new_world = Worlds(name=world_name, 
                            description=world_description, 
                            notes=world_notes_link)
            db.session.add(new_world)
            db.session.commit()

            notes_dir = os.path.dirname(world_notes_link)
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)
            with open(world_notes_link, 'w', encoding='utf-8') as notes_file:
                notes_file.write(world_notes)

            return redirect(url_for('DB_Status'))
    return render_template('create/create-world.html')

@app.route('/delete-world/<int:world_id>', methods=['GET','POST'])
def delete_world(world_id):
    world = Worlds.query.get(world_id)

    if world and world.notes:
        notes_file_path = os.path.join('static', world.notes)
        if os.path.exists(world.notes):
            os.remove(world.notes)

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


# Select World to reference in other entries
@app.route('/select-world/<int:world_id>', methods=['GET','POST'])
def select_world_id(world_id):
    if not Worlds.query.get(world_id):
        return "World not found", 404
    session['selected_world_id'] = world_id
    return redirect(url_for('DB_Status'))

@app.route('/clear-selected-world', methods=['GET','POST'])
def clear_selected_world():
    session.pop('selected_world_id', None)
    return redirect(url_for('DB_Status'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)