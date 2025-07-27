from models import db
from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from sqlalchemy.orm import joinedload
import os

from helpers import handle_create, handle_view, handle_delete, handle_edit
from utils import clean_filename

from models import Event
from models import Race, Religion
from models import Settlement, Subrace
from models import World

app = Flask(__name__)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'secret_key'

db.init_app(app)
with app.app_context():
    db.create_all()

if not os.path.exists('static/notes'):
    os.makedirs('static/notes')

@app.route('/')
def DB_Status():
    event = Event.query.all()
    race = Race.query.all()
    religion = Religion.query.all()
    settlement = Settlement.query.all()
    subrace = Subrace.query.options(joinedload(Subrace.race)).all()
    world = World.query.all()

    return render_template('db-status.html', 
                           event=event, 
                           race=race, 
                           religion=religion, 
                           settlement=settlement, 
                           subrace=subrace,
                           world=world)

# Error Routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Routes for creating, viewing, editing, and deleting entries
# Put new templates in the respective folders located under 'templates/'
# And enter the routes alphabetically

# Events
@app.route('/create-event', methods=['GET','POST'])
def create_event():
    return handle_create(Event,{
        'name': 'name',
        'description': 'description',
        'date': 'date',
        'notes': 'notes'
    }, 'create/create-event.html', 'event')

@app.route('/delete-event/<int:event_id>', methods=['GET','POST'])
def delete_event(event_id):
    return handle_delete(Event, event_id)

@app.route('/view-event/<int:event_id>', methods=['GET','POST'])
def view_event(event_id):
    return handle_view(Event, event_id, 'view/view-event.html')

@app.route('/edit-event/<int:event_id>', methods=['GET','POST'])
def edit_event(event_id):
    return handle_edit(Event, event_id, {
        'name': 'name',
        'description': 'description',
        'date': 'date',
        'notes': 'notes'
    }, 'edit/edit-event.html')


# Races
@app.route('/create-race', methods=['GET','POST'])
def create_race():
    return handle_create(Race, {
        'name': 'name',
        'description': 'description',
        'traits': 'traits',
        'notes': 'notes'}, 'create/create-race.html', 'race')

@app.route('/delete-race/<int:race_id>', methods=['GET','POST'])
def delete_race(race_id):
    return handle_delete(Race, race_id)

@app.route('/view-race/<int:race_id>', methods=['GET','POST'])
def view_race(race_id):
    
    return handle_view(Race, race_id, 'view/view-race.html')

@app.route('/edit-race/<int:race_id>', methods=['GET','POST'])
def edit_race(race_id):
    return handle_edit(Race, race_id, {
        'name': 'name',
        'description': 'description',
        'traits': 'traits',
        'notes': 'notes'
    }, 'edit/edit-race.html')


# Religions
@app.route('/create-religion', methods=['GET','POST'])
def create_religion():
    return handle_create(Religion, {
        'name': 'name',
        'description': 'description',
        'beliefs': 'beliefs',
        'notes': 'notes'}, 'create/create-religion.html', 'religion')

@app.route('/delete-religion/<int:religion_id>', methods=['GET','POST'])
def delete_religion(religion_id):
    return handle_delete(Religion, religion_id)

@app.route('/view-religion/<int:religion_id>', methods=['GET','POST'])
def view_religion(religion_id):
    return handle_view(Religion, religion_id, 'view/view-religion.html')

@app.route('/edit-religion/<int:religion_id>', methods=['GET','POST'])
def edit_religion(religion_id):
    return handle_edit(Religion, religion_id, {
        'name': 'name',
        'description': 'description',
        'beliefs': 'beliefs',
        'notes': 'notes'
    }, 'edit/edit-religion.html')


# Settlements
@app.route('/create-settlement', methods=['GET','POST'])
def create_settlement():
    return handle_create(Settlement, {
        'name': 'name',
        'description': 'description',
        'notes': 'notes'}, 'create/create-settlement.html', 'settlement')

@app.route('/delete-settlement/<int:settlement_id>', methods=['GET','POST'])
def delete_settlement(settlement_id):
    return handle_delete(Settlement, settlement_id)

@app.route('/view-settlement/<int:settlement_id>', methods=['GET','POST'])
def view_settlement(settlement_id):
    return handle_view(Settlement, settlement_id, 'view/view-settlement.html')

@app.route('/edit-settlement/<int:settlement_id>', methods=['GET','POST'])
def edit_settlement(settlement_id):
    return handle_edit(Settlement, settlement_id, {
        'name': 'name',
        'description': 'description',
        'notes': 'notes'
    }, 'edit/edit-settlement.html')


# Subraces
@app.route('/create-subrace', methods=['GET','POST'])
def create_subrace():
    races = Race.query.all()
    
    if request.method == 'POST':
        race_id = request.form.get('race_id')
        race = Race.query.get(race_id)
        
        if race and not race.has_subrace:
            race.has_subrace = True
            db.session.commit()
    
    return handle_create(Subrace, {
        'name': 'name',
        'description': 'description',
        'traits': 'traits',
        'notes': 'notes',
        'race_id': 'race_id'
    }, 'create/create-subrace.html', 'subrace', extra_context={'race': races})

@app.route('/delete-subrace/<int:subrace_id>', methods=['GET','POST'])
def delete_subrace(subrace_id):
    subrace = Subrace.query.get_or_404(subrace_id)
    race_id = subrace.race_id
    
    result = handle_delete(Subrace, subrace_id)
    
    remaining_subraces = Subrace.query.filter_by(race_id=race_id).count()
    if remaining_subraces == 0:
        race = Race.query.get(race_id)
        if race:
            race.has_subrace = False
            db.session.commit()
            
    return result

@app.route('/view-subrace/<int:subrace_id>', methods=['GET','POST'])
def view_subrace(subrace_id):
    return handle_view(Subrace, subrace_id, 'view/view-subrace.html', related_attr='race')

@app.route('/edit-subrace/<int:subrace_id>', methods=['GET','POST'])
def edit_subrace(subrace_id):
    
    subrace = Subrace.query.get_or_404(subrace_id)
    
    return handle_edit(Subrace, subrace_id, {
        'name': 'name',
        'description': 'description',
        'traits': 'traits',
        'notes': 'notes',
        'parent': 'race'
    }, 'edit/edit-subrace.html')


# Worlds
@app.route('/create-world', methods=['GET','POST'])
def create_world():
    if request.method == 'POST':
        world_name = request.form['name']
        world_description = request.form.get('description', '')
        world_notes = request.form.get('notes', '')
        last_world_id = World.query.order_by(World.id.desc()).first()
        world_id = last_world_id.id + 1 if last_world_id else 1
        world_notes_file_name = str(world_id) + '-world-' + clean_filename(world_name) + '-notes.md'
        world_notes_link = f'static/notes/{world_notes_file_name}'

        if not world_name:
            return "World name is required", 400
        
        if world_name in [w.name for w in World.query.all()]:
            return "World with this name already exists", 400
        else:
            new_world = World(name=world_name, 
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
    return render_template('create/create-world.html', include_world_id=False)

@app.route('/delete-world/<int:world_id>', methods=['GET','POST'])
def delete_world(world_id):
    world = World.query.get(world_id)

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
    world = World.query.get(world_id)

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
    world = World.query.get(world_id)

    notes_content = ''
    if world and world.notes and os.path.exists(world.notes):
        with open(world.notes, 'r', encoding='utf-8') as notes_file:
            notes_content = notes_file.read()
    else:
        notes_content = ""

    if not world:
        return "World not found", 404

    if request.method == 'POST':
        world.name = request.form['name']
        world.description = request.form.get('description', '')
        world.notes = request.form.get('notes', '')
        
        db.session.commit()
        return redirect(url_for('DB_Status'))

    return render_template('edit/edit-world.html', world=world, notes_content=notes_content)


# Select World to reference in other entries
@app.route('/select-world/<int:world_id>', methods=['GET','POST'])
def select_world_id(world_id):
    if not World.query.get(world_id):
        return "World not found", 404
    session['selected_world_id'] = world_id
    return redirect(url_for('DB_Status'))

# Clear selected world
@app.route('/clear-selected-world', methods=['GET','POST'])
def clear_selected_world():
    session.pop('selected_world_id', None)
    return redirect(url_for('DB_Status'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)