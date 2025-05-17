from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Note {self.id} - {self.title}>"

@app.route('/')
def index():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/note/new', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form.get('tags', '')
        note = Note(title=title, content=content, tags=tags)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_note.html')

@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.tags = request.form.get('tags', '')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_note.html', note=note)

@app.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
