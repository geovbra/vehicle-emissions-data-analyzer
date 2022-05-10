import json
from flask import Flask, request, jsonify, send_file
import jobs
import csv
import redis
import sys
app = Flask(__name__)


rd = redis.StrictRedis(host=sys.argv[1], port=6379, db=0)
jd = redis.StrictRedis(host=sys.argv[1], port=6379, db=2)


data = {}


@app.route('/', methods=['GET'])
def how_to():

    """
    Shows how to use the app to get the results you want.
    Returns:
        string: all of the possible inputs that the server is looking for.
    """




    return '\n\n----------------------------------------\nHow to use our Vehicle Emissions Analyzer\n----------------------------------------\n\nStep 1:\nReset the data in the kubernetes database by running a curl request with endpoint /reset -X POST\n\nStep 2:\nEvery part of CRUD is available. For instructions on how to use each route, use:\n    /create\n    /read\n    /update\n    /delete\n\n'

@app.route('/reset', methods=['POST'])
def read_data_from_file_into_dict():
    
    """
    Used to read in the data for later use with other functions. (Updates the list of data dictionaries)
    Returns:
        string: informing the user that the data is now available for use.
    """

    global data

    data['vehicle_emissions'] = []
    
    with open('uk_gov_data_dense_preproc.csv' , 'r', encoding = "ISO-8859-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['vehicle_emissions'].append(dict(row))

    rd.set('vehicle_emissions', json.dumps(data))

    return f'Data has been read from file\n'

# now emissions_data will be accessible to other functions

@app.route('/read', methods=['GET'])
def read_how_to():

    """
    Shows how to use the read route to get the desired data output.
    Returns:
        string: all of the possible inputs that the server is looking for.
    """




    return '\nHow to use /read:\n\nSyntax:\n/read/KEY?start=VALUE with the capital words being user inputs\n\n\nWhat the inputs can be:\n\nKEY:\n    all - returns all of the stored data\n    car_id - returns all data with specified car_id\n    manufacturer - returns all data with specified manufacturer\n    model - returns all data with specified model\n    description - returns all data with specified description\n    transmission - returns all data with specified transmission\n    transmission_type - returns all data with specified transmission_type\n    engine_size_cm3 - returns all data with specified engine_size_cm3\n    fuel - returns all data with specified fuel\n    powertrain - returns all data with specified powertrain\n    powertrain_ps - returns all data with specified powertrain_ps\n    co2_emissions_gPERkm - returns all data with specified co2_emissions_gPERkm\n\n\nVALUE:\n    Using the read/all route, find a value for your field that you would like to evaluate (IE: read/manufacturer?start=MERCEDES-BENZ)\n\n'

@app.route('/read/<string:key>', methods=['GET'])
def read(key:str):

    temp_data = []

    key = f'{key}'

    if key == "all":
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            temp_data.append(row)
    
    elif key == "car_id":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['car_id'] == start:
                temp_data.append(row)

    elif key == "manufacturer":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['manufacturer'] == start:
                temp_data.append(row)

    elif key == "model":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['model'] == start:
                temp_data.append(row)

    elif key == "description":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['description'] == start:
                temp_data.append(row)
  
    elif key == "transmission":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['transmission'] == start:
                temp_data.append(row)

    elif key == "transmission_type":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['transmission_type'] == start:
                temp_data.append(row)

    elif key == "engine_size_cm3":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['engine_size_cm3'] == start:
                temp_data.append(row)

    elif key == "fuel":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['fuel'] == start:
                temp_data.append(row)

    elif key == "powertrain":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['powertrain'] == start:
                temp_data.append(row)

    elif key == "power_ps":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['power_ps'] == start:
                temp_data.append(row)

    elif key == "co2_emissions_gPERkm":
        start = request.args.get('start')
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['co2_emissions_gPERkm'] == start:
                temp_data.append(row)

    return jsonify(temp_data)

@app.route('/update', methods=['GET'])
def update_how_to():

    """
    Shows how to use the update route to get the desired data input.
    Returns:
        string: all of the possible inputs that the server is looking for.
    """




    return '\nHow to use /update:\n\nSyntax:\n/update/CAR_ID  -X POST -H "Content-Type: application/json" -d \'{"field": "FIELD", "value": "VALUE"}\' with the capital words (other than POST) being user inputs\n\n\nWhat the inputs can be:\n\nCAR_ID:\n    Insert the car_id of the dataset that you wish to update\n\nFIELD:\n    manufacturer,\n    model,\n    description,\n    transmission,\n    transmission_type,\n    engine_size_cm3,\n    fuel,\n    powertrain,\n    power_ps,\n    co2_emissions_gPERkm\n\nVALUE:\n    Enter a new value for the field that you are updating (IE: /update/500  -X POST -H "content-Type: application/json" -d \'{"field": "manufacturer", "value": "me"}\') to set "me" as the value of manufacturer for car number 500'


@app.route('/update/<string:ID>', methods=['POST'])
def update_data(ID:str):

    ID = int(float(ID))

    temp_data = json.loads(rd.get('vehicle_emissions'))

    try:
        params = request.get_json(force=True)
    except Exception as e:
        return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})

    try:
        field = params['field']
        value = params['value']
    except Exception as e:
        return "Please provide a JSON dictionary with keys \"field\" and \"value\""

    if field == 'car_id':
        return 'You cannot alter the car_id!'
    if field != 'manufacturer' and field != 'model' and field != 'description' and field != 'transmission' and field != 'trasnmission_type' and field != 'engine_size_cm3' and field != 'fuel' and field != 'powertrain' and field != 'power_ps' and field != 'co2_emissions_gPERkm':
        return 'please enter a valid string for field.'
    updated_entry = {}  
 
    for row in temp_data['vehicle_emissions']:
        if int(float(row['car_id'])) == ID:
            row[field] = value
            updated_entry = row

    rd.set('vehicle_emissions', json.dumps(temp_data))

    return jsonify(updated_entry)

@app.route('/create', methods=['GET'])
def create_how_to():

    """
    Shows how to use the create route to get the desired data input.
    Returns:
        string: all of the possible inputs that the server is looking for.
    """




    return '\nHow to use /create\n\nSyntax:\n/create/new_entry -X POST -H "Content-Type: application/json" -d \'{"manufacturer": "VALUE", "model": "VALUE", "description": "VALUE", "transmission": "VALUE", "transmission_type": "VALUE", "engine_size_cm3": "VALUE", "fuel": "VALUE", "powertrain": "VALUE", "power_ps": "VALUE", "co2_emissions_gPERkm": "VALUE"}\' with the capital words (other than POST) being user inputs\n\n\nWhat the inputs can be:\n\nVALUE:\n    Enter the desired value for each field for each spot the says "VALUE"\n\nThe value of car_id will automatically be set to the next number in the list of current cars and appended to the end of that list\n\nExample:\ncreate/new_entry -X POST -H "Content-Type: application/json" -d \'{"manufacturer": "1", "model": "1", "description": "1", "transmission": "1", "transmission_type": "1", "engine_size_cm3": "1", "fuel": "1", "powertrain": "1", "power_ps": "1", "co2_emissions_gPERkm": "1"}\'\nThis will create a new car entry and append it to the end of the list with the next available car_id, and it will have a value of "1" for every field'

@app.route('/create/new_entry', methods=['POST'])
def create_data():
    
    temp_data = json.loads(rd.get('vehicle_emissions'))

    try:
        params = request.get_json(force=True)
    except Exception as e:
        return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
    try:
        manufacturer = params['manufacturer']
        model = params['model']
        description = params['description']
        transmission = params['transmission']
        transmission_type = params['transmission_type']
        engine_size_cm3 = params['engine_size_cm3']
        fuel = params['fuel']
        powertrain = params['powertrain']
        power_ps = params['power_ps']
        co2_emissions_gPERkm = params['co2_emissions_gPERkm']
    except Exception as e:
        return "Please provide a JSON dictionary containing values for all fields (except for car_id)"

    length = len(temp_data['vehicle_emissions'])
    last_val = int(float(temp_data['vehicle_emissions'][length-1]['car_id']))

    data_new = {}

    data_new['car_id'] = str(float(last_val + 1))
    data_new['manufacturer'] = manufacturer
    data_new['model'] = model
    data_new['description'] = description
    data_new['transmission'] = transmission
    data_new['transmission_type'] = transmission_type
    data_new['engine_size_cm3'] = engine_size_cm3
    data_new['fuel'] = fuel
    data_new['powertrain'] = powertrain
    data_new['power_ps'] = power_ps
    data_new['co2_emissions_gPERkm'] = co2_emissions_gPERkm

    temp_data['vehicle_emissions'].append(data_new)

    rd.set('vehicle_emissions', json.dumps(temp_data))
    return jsonify(data_new)

@app.route('/delete', methods=['GET'])
def delete_how_to():
    """
    Shows how to use the delete route to get the desired data output.
    Returns:
        string: all of the possible inputs that the server is looking for.
    """
    return '\n\nHow to use /delete\n\nSyntax:\n\n/delete/FIELD?value=VALUE -X POST with FIELD being a user input\n\n\nWhat the inputs can be:\n\nFIELD:\n    car_id\n    manufacturer,\n    model,\n    description,\n    transmission,\n    transmission_type,\n    engine_size_cm3,\n    fuel,\n    powertrain,\n    power_ps,\n    co2_emissions_gPERkm\n\nVALUE:\n    For the VALUE enter the value for the field of which you want every entry containing that pair to be deleted\n\nExample:\nTo delete just the car with car_id = 1234 use:\n    /delete/car_id?value=1234 -X POST\nTo delete all cars manufactured by Mercedes-Benz use:\n    /delete/manufacturer?value=MERCEDES-BENZ -X POST'

@app.route("/delete/<string:field>", methods=['POST'])
def delete(field:str):

    temp_data = json.loads(rd.get('vehicle_emissions'))
    new_data = {}
    new_data['vehicle_emissions'] = []
    value = request.args.get('value')

    for row in temp_data['vehicle_emissions']:
        if row[field] != value:
            new_data['vehicle_emissions'].append(dict(row))

    rd.set('vehicle_emissions', json.dumps(new_data))

    if temp_data == new_data:
        return "no data entries contain the field-value pair entered"

    return "data successfully deleted"

@app.route('/jobs', methods=['GET'])
def jobs_how_to():
    """
    Shows how to use the delete route to get the desired data output.
    Returns:
        string: all of the possible inputs that the server is looking for.
    """
    return 'jobs_test'

@app.route('/jobs/list', methods=['GET'])
def jobs_list():

    key_string = ""

    for key in jd.keys():
        key_string += str(jd.hgetall(key)) + "\n"
    return key_string

@app.route('/jobs/new_job', methods=['POST'])
def jobs_api():
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created.
    """
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job['plot_type'], job['field_1'], job['field_2']))


@app.route('/jobs/download/<jobid>', methods=['GET'])
def download(jobid):
    path = f'/app/{jobid}.png'
    with open(path, 'wb') as f:
        f.write(jd.hget(jobs.generate_job_key(jobid).encode(), b'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = '5005')
