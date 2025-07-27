import os
from flask import render_template, redirect, url_for, request
from models import db
from utils import clean_filename

def handle_create(model, fields, template_path, file_prefix, extra_context=None):
    
    context = {'fields': fields}
    if extra_context:
        context.update(extra_context)
        
    if request.method == 'POST':
        world_id = request.form.get('world_id')
        name = request.form.get(fields['name'])
        notes_text = str(request.form.get(fields['notes']))
        
        existing = model.query.filter_by(world_id=world_id, name=name).all()
        if name in [e.name for e in existing]:
            return f"{model.__name__} with this name already exists in the world.", 400
        
        last_item = model.query.filter_by(world_id=world_id).order_by(model.id.desc()).first()
        item_id = last_item.id + 1 if last_item else 1
        notes_filename = f"{world_id}-{item_id}-{file_prefix}-{clean_filename(name)}.md"
        notes_link = f"static/notes/{notes_filename}"

        os.makedirs(os.path.dirname(notes_link), exist_ok=True)
        with open(notes_link, 'w', encoding='utf-8') as notes_file:
            notes_file.write(notes_text)

        kwargs = {
            fields['name']: name,
            fields['description']: request.form.get(fields['description'], ''),
            fields['notes']: notes_link
        }

        optional_fields = [
            'date', 'traits', 'beliefs', 'race_id'
        ]

        for f in optional_fields:
            fkey = fields.get(f)
            if fkey is not None:
                kwargs[fkey] = request.form.get(f, '')

        new_entry = model(world_id=world_id, **kwargs)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('DB_Status'))
    
    return render_template(template_path, include_world_id=True, **context)


def handle_view(model, id, template_path, related_attr=None):
    
    item = model.query.get(id)
    if not item:
        return f"{model.__name__} not found.", 404
        
    related = getattr(item, related_attr) if related_attr else None
        
    return render_template(template_path,
                           **{
                                 model.__name__.lower(): item,
                                 'related': related,
                           })


def handle_delete(model, id):
    item = model.query.get(id)
    if item and item.notes and os.path.exists(item.notes):
        os.remove(item.notes)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('DB_Status'))


def handle_edit(model, id, fields, template_path):
    item = model.query.get(id)
    if not item:
        return f"{model.__name__} not found.", 404

    if request.method == 'POST':
        for key in fields:
            if key == 'parent':
                continue
            elif key == 'notes':
                notes_text = request.form.get(fields[key], '')
                notes_path = getattr(item, fields[key], '')
                if notes_path:
                    with open(notes_path, 'w', encoding='utf-8') as f:
                        f.write(notes_text)
            else:
                setattr(item, fields[key], request.form.get(fields[key], ''))
        
        db.session.commit()
        return redirect(url_for('DB_Status'))

    context = {
        model.__name__.lower(): item,
    }

    for key in fields:
        if key == 'notes':
            notes_path = getattr(item, fields[key], '')
            if os.path.exists(notes_path):
                with open(notes_path, 'r', encoding='utf-8') as f:
                    context[key] = f.read()
            else:
                context[key] = ''
        elif key != 'parent':
            context[key] = getattr(item, fields[key], '')
            
    if 'parent' in fields:
        context['parent'] = getattr(item, fields['parent'], None)
        
    return render_template(template_path, **context)