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

class Check_Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    
    def __init__(self, username):
        self.username = username

# Outside the import_data function
def update_record(record, row_data):
    for key, value in row_data.items():
        if hasattr(record, key):
            setattr(record, key, round(value, 6) if isinstance(value, float) else value)
        flash("Upload successful!", "success")
        db.session.commit()



def create_csv_data(row):
    return CSVData(
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

@app.route('/extended_data_analysis')
def extended_data_analysis():
    data = CSVData.query.all()

    # Convert data to DataFrame
    df = pd.DataFrame([vars(d) for d in data])
    df.drop('_sa_instance_state', axis=1, inplace=True)  # Remove unnecessary column

    # Analysis for sum and count
    analysis = {
        'sum': df.sum().to_dict(),      # Sum of each column
        'count': df.count().to_dict()   # Count of non-null records in each column
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
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form['admin']

        try:
            new_user = User(username=username, password=password)
            db.session.add(new_user)

            # Add to Check_Admin table if is_admin is True
            if int(is_admin):
                db.session.add(Check_Admin(username=username))

            db.session.commit()
            return redirect(url_for('manage_users'))  # Redirect to manage users page
        except Exception as e:
            print(e)  # For debugging purposes
            return redirect(url_for('manage_users'))
    else:
        return redirect(url_for('manage_users'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
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
            session['username'] = data.username  # Store the username in the session
            return redirect(url_for('analytics'))
        return render_template('theme/sign-in.html', message="Incorrect Details")
    


@app.route('/view_data', methods=['GET'])
def view_data():
    selected_filters = request.args.getlist('filter')
    selected_modules = request.args.getlist('module')

    # Determine which model to use based on the selected module
    model = CSVData  # Default model
    if 'module1' in selected_modules:
        model = Module1
    elif 'module2' in selected_modules:
        model = Module2
    elif 'module3' in selected_modules:
        model = Module3
    elif 'module4' in selected_modules:
        model = Module4

    # Default to displaying all fields if no checkboxes are selected
    if not selected_filters:
        selected_filters = [column.name for column in model.__table__.columns]

    # Start with all records from the selected model
    all_data = model.query
    min_value = request.args.get('minValue', type=float)
    max_value = request.args.get('maxValue', type=float)

    # Apply dynamic range filters based on selected filters
    filter_conditions = []
    for filter_col in selected_filters:
        if min_value is not None and max_value is not None:
            filter_conditions.append(getattr(model, filter_col).between(min_value, max_value))

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
    
@app.route('/delete_selected_users', methods=['POST'])
def delete_selected_users():
    try:
        user_usernames = request.form.getlist('user_usernames')  # Get list of selected user usernames
        for user_username in user_usernames:
            # Query for the user in the User model
            user = User.query.filter_by(username=user_username).first()
            if user:
                # Query for the user in the Check_Admin model
                admin_user = Check_Admin.query.filter_by(username=user_username).first()
                if admin_user:
                    db.session.delete(admin_user)  # Delete from Check_Admin if exists
                db.session.delete(user)  # Delete from User model

        db.session.commit()
        return redirect(url_for('manage_users', message="Users deleted successfully"))
    except Exception as e:
        return str(e)


@app.route('/manage_users', methods=['GET'])
def manage_users():
    # Check if a user is logged in
    if session.get('logged_in'):
        current_user_username = session.get('username')
        admin_user = Check_Admin.query.filter_by(username=current_user_username).first()

        if admin_user:
            # The user is an admin
            users = User.query.all()  # Fetch all users
            users_count = len(users)  # Get the count of users
            return render_template('theme/manage_users.html', users=users, users_count=users_count)
        else:
            # The user is not an admin
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('restricted'))  # Redirect to a restricted access page

    flash("Please log in to access this page.", "error")
    return redirect(url_for('login_page'))  # Redirect to login page
    
@app.route('/restricted', methods=['GET'])
def restricted():
    return render_template('theme/restrict.html')

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


