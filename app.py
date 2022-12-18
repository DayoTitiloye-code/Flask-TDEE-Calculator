from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)

class Results(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    calculation = db.Column('calculation', db.Float)

    def __init__(self, calculation):
        self.calculation = calculation

@app.route('/')
def home():
    return render_template('base.html'), 200

@app.route('/result', methods=['POST', 'GET'])
def result():
    age = None
    weight = None
    height = None
    activity = None
    if request.method == 'POST':
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        activity = request.form['activity']
        form_data = request.form
        bmr = (11.65 * float(weight)) + (3.4 * float(height)) - (5.75 * float(age)) + 360
        calculation = None
        match activity:
            case 'sedentary':
                calculation = int(bmr * 1.2)
            case 'le':
                calculation = int(bmr * 1.375)
            case 'me':
                calculation = int(bmr * 1.55)
            case 'he': 
                calculation = int(bmr * 1.725)
            case 'athlete':
                calculation = int(bmr * 1.9)
        print(bmr)
        calc = Results(calculation)
        db.session.add(calc)
        db.session.commit()
    return render_template('result.html', form_data = form_data, calculation=calculation), 200

@app.route('/view')
def view():
    return render_template('view.html', values = Results.query.all())

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"message": f"Sorry... {err}"}), 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"message": f"It's not you, it's us"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

