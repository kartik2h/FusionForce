from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd  # Correct way to import pandas
import psycopg2
from flask import Flask, url_for, render_template, request, redirect, session, make_response, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/Featherstill'


db = SQLAlchemy(app)

class CSVData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Iteration = db.Column(db.Float)
    CPUTime = db.Column(db.Float)
    PhysTime = db.Column(db.Float)
    Travels = db.Column(db.Float)
    Value = db.Column(db.Float)
    AvValue = db.Column(db.Float)
    MinValue = db.Column(db.Float)
    MaxValue = db.Column(db.Float)
    Delta = db.Column(db.Float)
    Criteria = db.Column(db.Float)
    PrevAvRefValue = db.Column(db.Float)
    Progress = db.Column(db.Float)
    CriteriaType = db.Column(db.Float)
    CriteriaVarType = db.Column(db.Float)
    CriteriaPercentage = db.Column(db.Float)



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
                    Iteration=row['Iteration'],
                    CPUTime=round(row['CPUTime'], 6),
                    PhysTime=round(row['PhysTime'], 6),
                    Travels=round(row['Travels'], 6),
                    Value=round(row['Value'],6),
                    AvValue=round(row['AvValue']),
                    MinValue=round(row['MinValue'], 6),
                    MaxValue=round(row['MaxValue'], 6),
                    Delta=round(row['Delta'], 6),
                    Criteria=round(row['Criteria'], 6),
                    PrevAvRefValue=round(row['PrevAvRefValue'], 6),
                    Progress=round(row['Progress'], 6),
                    CriteriaType=round(row['CriteriaType'], 6),
                    CriteriaVarType=round(row['CriteriaVarType'], 6),
                    CriteriaPercentage=row['CriteriaPercentage']
                )
                db.session.add(csv_data)
            
            db.session.commit()
            
            return "Data imported and saved successfully!"
        except Exception as e:
            return f"Error importing and saving data: {str(e)}"

    return "Invalid file format"


@app.route('/data_analysis')
def data_analysis():
    data = CSVData.query.all()
    
    # Convert data to DataFrame
    df = pd.DataFrame([vars(d) for d in data])
    df.drop('_sa_instance_state', axis=1, inplace=True)  # Remove unnecessary column

    # Example analysis - replace with your own analysis logic
    analysis = {
        'mean': df.mean().to_dict(),
        'median': df.median().to_dict(),
        'max': df.max().to_dict(),
        'min': df.min().to_dict(),
    }

    return jsonify(analysis)

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        selected_filters = request.args.getlist('filter')  # Collects selected checkboxes
        session['selected_filters'] = selected_filters
        all_data = CSVData.query.all()
        filtered_data = []
        for data in all_data:
            data_dict = data.__dict__
            filtered_record = {key: data_dict[key] for key in selected_filters}
            filtered_data.append(filtered_record)
        return render_template('LandingPage.html', records=filtered_data, selected_filters=selected_filters)
    else:
        return render_template('login.html', message="Hello!")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('login.html', message="User Already Exists")
    else:
        return render_template('login.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            #return redirect(url_for('home'))
            return render_template('LandingPage.html')
        return render_template('login.html', message="Incorrect Details")


@app.route('/export', methods=['GET'])
def export_data():
    try:
        # Retrieve filters from the session, default to None if not set
        selected_filters = session.get('selected_filters', [])

        # If no filters are selected or it's None, select all columns
        if not selected_filters:
            selected_filters = ['Iteration', 'CPUTime', 'PhysTime', 'Travels', 'Value', 'AvValue', 'MinValue', 'MaxValue', 'Delta', 'Criteria', 'PrevAvRefValue', 'Progress', 'CriteriaType', 'CriteriaVarType', 'CriteriaPercentage']

        # Query all CSVData from the database
        data = CSVData.query.all()

        # Process and filter the data
        filtered_data = []
        for d in data:
            data_dict = d.__dict__
            filtered_record = {key: data_dict[key] for key in selected_filters}
            filtered_data.append(filtered_record)

        # Convert the filtered data to a pandas DataFrame
        df = pd.DataFrame(filtered_data, columns=selected_filters)

        # Convert the DataFrame to CSV format
        csv_data = df.to_csv(index=False)

        # Create a response with the CSV data
        response = make_response(csv_data)
        response.headers['Content-Disposition'] = 'attachment; filename=filtered_data.csv'
        response.headers['Content-Type'] = 'text/csv'

        return response
    except Exception as e:
        return f"Error exporting data: {str(e)}"



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))




if(__name__ == '__main__'):
    with app.app_context():
        db.create_all()
    app.secret_key = "ThisIsNotASecret:p"
    
    
    app.run()
