from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from flask_datatables import get_row_id, DataTables


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['DATATABLES_ROW_ID'] = 'DT_RowId'
datatables = DataTables(app)


# Define the test data for the dropdown lists
org_data = ['FDA', 'CDISC', 'HL7', 'PHUSE']
std_data = ['FDA Rules', 'SDTM', 'ADaM', 'SEND']
ver_data = ['v1.0', 'v2.0', 'v3.1', 'v3.2', 'v3.3', 'v3.4']
dom_data = [ 'DM', 'AE', 'LB', 'CV', 'DS', 'EC', 'FA']
rule_data = ['CG0001', 'CG0002','CG0150','etc']
var_data = {'StudyID','SubjID'}
opt_data = {'equal to', 'greater than', 'less than'}

# Build the rule string
# rule_str = f"{name} {operator} {value}"


@app.route('/')
def index():
    org_data = ['FDA', 'CDISC', 'HL7', 'ABC']
    return render_template('index.html', organizations=org_data,
                           standards=std_data,
                           versions=ver_data,
                           domains=dom_data,
                           rules=rule_data,
                           variables=var_data,
                           operators=opt_data
                           )

@app.route('/', methods=['POST'])
def submit():
    organization = request.form.get('organization')
    standard = request.form.get('standard')
    version = request.form.get('version')
    domain = request.form.get('domain')
    rule = request.form.get('rule')
    name = request.form.get('name')
    operator = request.form.get('operator')
    value = request.form.get('value')
    
    # Build the rule string
    rule_str = f"{name} {operator} {value}"
   
    # Render the results template with the selected values
    return render_template('results.html',
                           organization=org_data,
                           standard=std_data,
                           version=ver_data,
                           domain=dom_data,
                           rule=rule_data,
                           rule_str=rule_str)


@app.route('/data')
def data():
    data = [
        {'name': 'John', 'age': 30, 'gender': 'Male'},
        {'name': 'Sarah', 'age': 25, 'gender': 'Female'},
        {'name': 'Michael', 'age': 40, 'gender': 'Male'},
        {'name': 'Jessica', 'age': 35, 'gender': 'Female'}
    ]
    return jsonify(data)


@app.route('/data')
def data():
    data = [
        {'name': 'John', 'age': 30, 'gender': 'Male'},
        {'name': 'Sarah', 'age': 25, 'gender': 'Female'},
        {'name': 'Michael', 'age': 40, 'gender': 'Male'},
        {'name': 'Jessica', 'age': 35, 'gender': 'Female'}
    ]
    return jsonify(data)


@app.route('/data2')
def data():
    data2 = [
        {'name': 'John', 'age': 30, 'gender': 'Male'},
        {'name': 'Sarah', 'age': 25, 'gender': 'Female'},
        {'name': 'Michael', 'age': 40, 'gender': 'Male'},
        {'name': 'Jessica', 'age': 35, 'gender': 'Female'}
    ]
    return jsonify(data2)

if __name__ == '__main__':
    app.run(debug=True)
