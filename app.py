from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd  # Correct way to import pandas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class CSVData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iteration = db.Column(db.Integer)
    cpu_time = db.Column(db.Integer)
    phys_time = db.Column(db.Integer)
    travels = db.Column(db.Integer)
    value = db.Column(db.Integer)
    av_value = db.Column(db.Integer)
    min_value = db.Column(db.Integer)
    max_value = db.Column(db.Integer)
    delta = db.Column(db.Integer)
    criteria = db.Column(db.Integer)
    prev_av_ref_value = db.Column(db.Integer)
    progress = db.Column(db.Integer)
    criteria_type = db.Column(db.Integer)
    criteria_var_type = db.Column(db.Integer)
    criteria_percentage = db.Column(db.Integer, __tablename__='CSVData')  # Set the table name to 'CSVData'
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/import', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file)

            # Create a new record for each row and save it to the database
            for index, row in df.iterrows():
                csv_data = CSVData(
                    iteration=row['Iteration'],
                    cpu_time=row['CPUTime'],
                    phys_time=row['PhysTime'],
                    travels=row['Travels'],
                    value=row['Value'],
                    av_value=row['AvValue'],
                    min_value=row['MinValue'],
                    max_value=row['MaxValue'],
                    delta=row['Delta'],
                    criteria=row['Criteria'],
                    prev_av_ref_value=row['PrevAvRefValue'],
                    progress=row['Progress'],
                    criteria_type=row['CriteriaType'],
                    criteria_var_type=row['CriteriaVarType'],
                    criteria_percentage=row['CriteriaPercentage']
                )
                #db.session.add(csv_data)
            
            db.session.commit()
            
            return "Data imported and saved successfully!"
        except Exception as e:
            return f"Error importing and saving data: {str(e)}"

    return "Invalid file format"


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))



if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
   # db.create_all()
    
    app.run()
