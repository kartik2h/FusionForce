from flask import Flask, url_for, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd  # Correct way to import pandas
import psycopg2
from flask import Flask, url_for, render_template, request, redirect, session, make_response, jsonify
from sqlalchemy import and_

app = Flask(__name__, static_folder='templates/theme/assets')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/Featherstill'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5433/csvfile'

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

class Module1(db.Model):
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

class Module2(db.Model):
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

class Module3(db.Model):
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

class Module4(db.Model):
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
        return "No file part", 400

    file = request.files['file']
    selected_modules = request.form.getlist('modules')

    if file.filename == '':
        return "No selected file", 400

    if file:
        try:
            df = pd.read_csv(file)

            for index, row in df.iterrows():
                # Create a record for CSVData
                csv_data = CSVData(
                    Iteration=row['Iteration'],
                    CPUTime=round(row['CPUTime'], 6),
                    PhysTime=round(row['PhysTime'], 6),
                    Travels=round(row['Travels'], 6),
                    Value=round(row['Value'], 6),
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

                # Add data to selected modules
                for module in selected_modules:
                    module_class = get_module_class(module)
                    if module_class:
                        module_record = module_class(**row.to_dict())
                        db.session.add(module_record)

            db.session.commit()
            return redirect(url_for('landing_page'))
        except Exception as e:
            return f"Error importing and saving data: {str(e)}"

    flash("Invalid file format", "error")
    return redirect(url_for('landing_page'))

def get_module_class(module_name):
    module_mapping = {
        'module1': Module1,
        'module2': Module2,
        'module3': Module3,
        'module4': Module4,
    }
    return module_mapping.get(module_name)


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
        return render_template('theme/edited_analytics.html')
    else:
        return redirect(url_for('home_page'))
    

@app.route('/home_page', methods=['GET', 'POST'])
def home_page():
    return render_template('theme/home_page.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('manage_users'))  # Assuming this redirects to the 'sign-in.html' page
        except:
            return render_template('theme/manage_users.html', message="User Already Exists")
    else:
        return render_template('theme/manage_users.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    global data
    if request.method == 'GET':
        return render_template('theme/sign-in.html')
    else:
        u = request.form['username']
        p = request.form['password']
        try:
            data = User.query.filter_by(username=u, password=p).first()
        except Exception as e:
            print("Error!!")
        if data is not None:
            session['logged_in'] = True
            # return redirect(url_for('home'))
            return redirect(url_for('analytics'))
        return render_template('theme/sign-in.html', message="Incorrect Details")
    


@app.route('/view_data', methods=['GET'])
def view_data():
    selected_filters = request.args.getlist('filter')

    # Default to displaying all fields if no checkboxes are selected
    if not selected_filters:
        selected_filters = ['Iteration', 'CPUTime', 'PhysTime', 'Travels', 'Value', 'AvValue', 'MinValue', 'MaxValue', 'Delta', 'Criteria', 'PrevAvRefValue', 'Progress', 'CriteriaType', 'CriteriaVarType', 'CriteriaPercentage']

    # Start with all records
    all_data = CSVData.query
    min_value = request.args.get('minValue', type=float)
    max_value = request.args.get('maxValue', type=float)

    # Apply dynamic range filters based on selected filters
    filter_conditions = []
    for filter_col in selected_filters:
        if min_value is not None and max_value is not None:
            filter_conditions.append(getattr(CSVData, filter_col).between(min_value, max_value))

    if filter_conditions:
        all_data = all_data.filter(and_(*filter_conditions))

    # Execute the query and retrieve data
    all_data = all_data.all()
    print(all_data)
    # Filter and format the data based on selected columns
    filtered_data = []
    for data in all_data:
        data_dict = data.__dict__
        filtered_record = {key: data_dict[key] for key in selected_filters if key in data_dict}
        filtered_data.append(filtered_record)

    session['selected_filters'] = selected_filters
    return render_template('theme/view_data.html', records=filtered_data, selected_filters=selected_filters)

@app.route('/edit_index', methods=['GET'])
def landing_page():
    module1_records = Module1.query.count()
    module2_records = Module2.query.count()
    module3_records = Module3.query.count()
    module4_records = Module4.query.count()

    return render_template('theme/edit_index.html', 
                           module1_records=module1_records,
                           module2_records=module2_records,
                           module3_records=module3_records,
                           module4_records=module4_records)

@app.route('/edited_analytics', methods=['GET'])
def analytics():
    return render_template('theme/edited_analytics.html')



@app.route('/manage_users', methods=['GET'])
def manage_users():
    users = User.query.all()  # Fetch all users
    users_count = len(users)  # Get the count of users
    return render_template('theme/manage_users.html', users=users, users_count=users_count)

@app.route('/delete_selected_users', methods=['POST'])
def delete_selected_users():
    try:
        user_ids = request.form.getlist('user_ids')  # Get list of selected user IDs
        for user_id in user_ids:
            user = User.query.get(int(user_id))
            if user:
                db.session.delete(user)
        db.session.commit()
        return redirect(url_for('delete_user', message="Users deleted successfully"))
    except Exception as e:
        return str(e)

@app.route('/export', methods=['GET'])
def export_data():
    try:
        # Retrieve filters from the session, default to None if not set
        selected_filters = session.get('selected_filters', [])

        # If no filters are selected or it's None, select all columns
        if not selected_filters:
            selected_filters = ['Iteration', 'CPUTime', 'PhysTime', 'Travels', 'Value', 'AvValue', 'MinValue',
                                'MaxValue', 'Delta', 'Criteria', 'PrevAvRefValue', 'Progress', 'CriteriaType',
                                'CriteriaVarType', 'CriteriaPercentage']

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


if (__name__ == '__main__'):
    with app.app_context():
        db.create_all()
    app.secret_key = "ThisIsNotASecret:p"

    app.run()


