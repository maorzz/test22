
from enum import unique
from flask import Flask, redirect, url_for, render_template, request, session, flash, redirect, url_for
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.sql.elements import Null


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    gorem = db.Column(db.String(20))
    desc = db.Column(db.Text(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return Table(self.name)


################################################


@ app.route("/")
def home():
    return render_template("index.html")


@ app.route("/events")
def events():
    myTable = Table.query.all()
    return render_template("events.html", myTable=myTable)


@ app.route("/monitor")
def monitor():
    return render_template("monitor.html")


@ app.route("/addevent", methods=['POST'])
def addevent():
    name = Table(request.form['name'], request.form['desc'])
    db.session.add(name)
    db.session.commit()
    return redirect(url_for('events'))


@ app.route("/update/<int:id>",  methods=["GET", "POST"])
def update(id):
    table_to_update = Table.query.get_or_404(id)

    if request.method == "POST":
        table_to_update.name = request.form['event']
        try:
            db.session.commit()

            return redirect('/events')
        except:
            return "THERE WAS A PROBLEM"
    else:
        return render_template('update.html', table_to_update=table_to_update)


@ app.route("/updatevent/<int:id>",  methods=["GET", "POST"])
def editevent(id):
    event_to_update = Table.query.get_or_404(id)

    if request.method == "POST":
        event_to_update.desc = request.form['editevent']
        try:
            db.session.commit()

            return redirect('/events')
        except:
            return "THERE WAS A PROBLEM"
    else:
        return render_template('updateevent.html', event_to_update=event_to_update)


@ app.route("/delete/<int:id>",  methods=["GET", "POST"])
def delete(id):
    delete_event = Table.query.get_or_404(id)

    try:
        db.session.delete(delete_event)
        db.session.commit()
        return redirect('/events')
    except:
        return "THERE WAS A PROBLEM"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
