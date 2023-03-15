from flask import Flask, render_template, request

app = Flask(__name__)

# Define the test data for the dropdown lists
org_data = ['FDA', 'CDISC', 'HL7', 'PHUSE']
std_data = {'FDA': ['FDA Rules', 'FDA Guidelines'],
            'CDISC': ['SDTM', 'ADaM', 'SEND'],
            'HL7': ['HL7 v2', 'HL7 v3']}
ver_data = {'FDA Rules': ['v1.0', 'v2.0'],
            'FDA Guidelines': ['v1.0', 'v1.1'],
            'SDTM': ['v3.1.2', 'v3.2'],
            'ADaM': ['v2.1.1', 'v2.2'],
            'SEND': ['v3.0.1', 'v3.1.0'],
            'HL7 v2': ['v2.1', 'v2.2'],
            'HL7 v3': ['v3.0', 'v3.1']}
dom_data = {'v1.0': ['Demographics', 'Concomitant Medications'],
            'v1.1': ['Demographics', 'Concomitant Medications', 'Adverse Events'],
            'v2.0': ['Demographics', 'Concomitant Medications', 'Adverse Events', 'Vital Signs'],
            'v3.1.2': ['DM', 'AE'],
            'v3.2': ['DM', 'AE', 'LB'],
            'v2.1.1': ['ADSL', 'ADaM-DM', 'ADaM-MA'],
            'v2.2': ['ADSL', 'ADaM-DM', 'ADaM-MA', 'ADAeM'],
            'v3.0.1': ['CV', 'DS', 'EC', 'FA'],
            'v3.1.0': ['CV', 'DS', 'EC', 'FA', 'LB'],
            'v2.1': ['ADT', 'ORM', 'ORU'],
            'v2.2': ['ADT', 'ORM', 'ORU', 'MFN'],
            'v3.0': ['ADT', 'ORM', 'ORU', 'MFN', 'MDM'],
            'v3.1': ['ADT', 'ORM', 'ORU', 'MFN', 'MDM', 'MFD']}
rule_data = {'Demographics': ['Age >= 18', 'Gender in {Male, Female}', 'Race in {White, Black, Asian}'],
             'Concomitant Medications': ['Start Date >= 01/01/2022', 'End Date <= 06/30/2022'],
             'Adverse Events': ['Severity in {Mild, Moderate, Severe}', 'Related To in {Drug, Device}'],
             'Vital Signs': ['Systolic BP >= 120', 'Diastolic BP <= 80'],
             'DM': ['Study ID not null', 'Age >= 18'],
             'AE': ['Severity in {Mild, Moderate, Severe}', 'Related To in {Drug, Device}'],
             'LB': ['Visit Name not null', 'Test Name in {Hematology, Chemistry}'],
             'ADSL': ['Pool ID in {P001, P002, P003}', 'Sex in {M, F}'],
             'ADaM-DM': ['Subject ID in {001, 002, 003}', 'Visit Name in {Screening, Baseline}'],
             'ADaM-MA': ['Subject ID in {AB1, AB2, AB3}', 'Visit Name in {Screening, Baseline}'],
             }
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

if __name__ == '__main__':
    app.run(debug=True)
