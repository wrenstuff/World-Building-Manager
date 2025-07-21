from models import db
from flask import Flask, render_template, request, redirect, url_for, session
import os

from helpers import handle_create, handle_view, handle_delete, handle_edit
from utils import clean_filename

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
    return handle_create(Events,{
        'name': 'name',
        'description': 'description',
        'date': 'date',
        'notes': 'notes'
    }, 'create/create-event.html', 'event')

@app.route('/delete-event/<int:event_id>', methods=['GET','POST'])
def delete_event(event_id):
    return handle_delete(Events, event_id)

@app.route('/view-event/<int:event_id>', methods=['GET','POST'])
def view_event(event_id):
    return handle_view(Events, event_id, 'view/view-event.html')

@app.route('/edit-event/<int:event_id>', methods=['GET','POST'])
def edit_event(event_id):
    return handle_edit(Events, event_id, {
        'name': 'name',
        'description': 'description',
        'date': 'date',
        'notes': 'notes'
    }, 'edit/edit-event.html')


# Races
@app.route('/create-race', methods=['GET','POST'])
def create_race():
    return handle_create(Races, {
        'name': 'name',
        'description': 'description',
        'traits': 'traits',
        'notes': 'notes'}, 'create/create-race.html', 'race')

@app.route('/delete-race/<int:race_id>', methods=['GET','POST'])
def delete_race(race_id):
    return handle_delete(Races, race_id)

@app.route('/view-race/<int:race_id>', methods=['GET','POST'])
def view_race(race_id):
    return handle_view(race_id, 'view/view-race.html')

@app.route('/edit-race/<int:race_id>', methods=['GET','POST'])
def edit_race(race_id):
    return handle_edit(Races, race_id, {
        'name': 'name',
        'description': 'description',
        'traits': 'traits',
        'notes': 'notes'
    }, 'edit/edit-race.html')


# Religions
@app.route('/create-religion', methods=['GET','POST'])
def create_religion():
    return handle_create(Religions, {
        'name': 'name',
        'description': 'description',
        'beliefs': 'beliefs',
        'notes': 'notes'}, 'create/create-religion.html', 'religion')

@app.route('/delete-religion/<int:religion_id>', methods=['GET','POST'])
def delete_religion(religion_id):
    return handle_delete(Religions, religion_id)

@app.route('/view-religion/<int:religion_id>', methods=['GET','POST'])
def view_religion(religion_id):
    return handle_view(Religions, religion_id, 'view/view-religion.html')

@app.route('/edit-religion/<int:religion_id>', methods=['GET','POST'])
def edit_religion(religion_id):
    return handle_edit(Religions, religion_id, {
        'name': 'name',
        'description': 'description',
        'beliefs': 'beliefs',
        'notes': 'notes'
    }, 'edit/edit-religion.html')


# Settlements
@app.route('/create-settlement', methods=['GET','POST'])
def create_settlement():
    return handle_create(Settlements, {
        'name': 'name',
        'description': 'description',
        'notes': 'notes'}, 'create/create-settlement.html', 'settlement')

@app.route('/delete-settlement/<int:settlement_id>', methods=['GET','POST'])
def delete_settlement(settlement_id):
    return handle_delete(Settlements, settlement_id)

@app.route('/view-settlement/<int:settlement_id>', methods=['GET','POST'])
def view_settlement(settlement_id):
    return handle_view(Settlements, settlement_id, 'view/view-settlement.html')

@app.route('/edit-settlement/<int:settlement_id>', methods=['GET','POST'])
def edit_settlement(settlement_id):
    return handle_edit(Settlements, settlement_id, {
        'name': 'name',
        'description': 'description',
        'notes': 'notes'
    }, 'edit/edit-settlement.html')


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

    notes_content = ''
    if world and world.notes and os.path.exists(world.notes):
        with open(world.notes, 'r', encoding='utf-8') as notes_file:
            notes_content = notes_file.read()
    else:
        notes_content = "No notes available for this world."

    if not world:
        return "World not found", 404
    return render_template('view/view-world.html', world=world, notes_content=notes_content)

@app.route('/edit-world/<int:world_id>', methods=['GET','POST'])
def edit_world(world_id):
    world = Worlds.query.get(world_id)

    notes_content = ''
    if world and world.notes and os.path.exists(world.notes):
        with open(world.notes, 'r', encoding='utf-8') as notes_file:
            notes_content = notes_file.read()
    else:
        notes_content = ""

    if not world:
        return "World not found", 404

    if request.method == 'POST':
        world.name = request.form['world_name']
        world.description = request.form.get('world_description', '')
        world.notes = request.form.get('world_notes', '')
        
        db.session.commit()
        return redirect(url_for('DB_Status'))

    return render_template('edit/edit-world.html', world=world, notes_content=notes_content)


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