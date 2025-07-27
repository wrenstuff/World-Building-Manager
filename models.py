from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

db = SQLAlchemy()

class NotesMixin:
    @property
    def notes_content(self):
        if self.notes and os.path.exists(self.notes):
            with open(self.notes, 'r', encoding='utf-8') as f:
                return f.read()
        return 'No notes available.'

# this is where all of the models are defined for the World Building Manager app
# Add more comments when there's something else that could be added
# Sort the models alphabetically by their names

# events
class Event(db.Model, NotesMixin):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# factions
# items
# languages
# locations
# nations
# people
# races
class Race(db.Model, NotesMixin):
    __tablename__ = 'race'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    traits = db.Column(db.Text)
    notes = db.Column(db.Text)
    has_subrace = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    subraces = db.relationship('Subrace', back_populates='race')

# religions
class Religion(db.Model, NotesMixin):
    __tablename__ = 'religion'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    beliefs = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# settlements
class Settlement(db.Model, NotesMixin):
    __tablename__ = 'settlement'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# subraces
class Subrace(db.Model, NotesMixin):
    __tablename__ = 'subrace'
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    traits = db.Column(db.Text)
    notes = db.Column(db.Text)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    race = db.relationship('Race', back_populates='subraces')

# timelines
# worlds
class World(db.Model, NotesMixin):
    __tablename__ = 'world'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))