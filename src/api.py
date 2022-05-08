import json
from flask import Flask, request, jsonify
import jobs
import csv
import redis
import sys
app = Flask(__name__)


rd = redis.StrictRedis(host=sys.argv[1], port=6379, db=0)



data = {}


@app.route('/', methods=['GET'])
def how_to():

    """
    Shows how to use the app to get the results you want.
    Returns: 
        string: all of the possible inputs that the server is looking for.
    """




    return 'test'


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




    return 'test_read_how_to'


@app.route('/read/<string:key>', methods=['GET'])
def read(key:str):

    temp_data = []

    key = f'{key}'

    if key == "all":
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            temp_data.append(row)
    
    elif key == "car_id":
        start = request.args.get('start')
	
        #if type(start) != int:
        #    return 'please use an integer as your query parameter'

        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['car_id'] == start:
                temp_data.append(row)

    elif key == "manufacturer":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['manufacturer'] == start:
                temp_data.append(row)

    elif key == "model":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['model'] == start:
                temp_data.append(row)

    elif key == "description":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['description'] == start:
                temp_data.append(row)
  
    elif key == "transmission":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['transmission'] == start:
                temp_data.append(row)

    elif key == "transmission_type":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['transmission_type'] == start:
                temp_data.append(row)

    elif key == "engine_size_cm3":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['engine_size_cm3'] == start:
                temp_data.append(row)

    elif key == "fuel":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['fuel'] == start:
                temp_data.append(row)

    elif key == "powertrain":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['powertrain'] == start:
                temp_data.append(row)

    elif key == "power_ps":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['power_ps'] == start:
                temp_data.append(row)

    elif key == "co2_emissions_gPERkm":
        start = request.args.get('start')
        if type(start) != str:
            return 'please use a string as your query parameter'
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row['co2_emissions_gPERkm'] == start:
                temp_data.append(row)

    return jsonify(temp_data)


@app.route('/update/<string:ID>', methods=['POST'])
def update_data(ID:str):

    ID = int(float(ID))

    temp_data = json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']

    field = request.args.get('field')
    value = request.args.get('value')

    if field == 'car_id':
        return 'You cannot alter the car_id!'
    if field != 'manufacturer' or field != 'model' or field != 'description' or field != 'transmission' or field != 'trasnmission_type' or field != 'engine_size_cm3' or field != 'fuel' or field != 'powertrain' or field != 'power_ps' or field != 'co2_emissions_gPERkm':
        return 'please enter a valid string for field.'

    temp_data[ID][field] = value

    rd.set('vehicle_emissions', json.dumps(temp_data))

    return jsonify(temp_data)

@app.route('/create/new_entry', methods=['POST'])
def create_data():
    
    temp_data = json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']

    manufacturer = request.args.get('manufacturer')
    model = request.args.get('model')
    description = request.args.get('description')
    transmission = request.args.get('transmission')
    transmission_type = request.args.get('transmission_type')
    engine_size_cm3 = request.args.get('engine_size_cm3')
    fuel = request.args.get('fuel')
    powertrain = request.args.get('powertrain')
    power_ps = request.args.get('power_ps')
    co2_emissions_gPERkm = request.args.get('co2_emissions_gPERkm')

    length = len(temp_data)

    data_new = {}

    data_new['car_id'] = str(float(length + 1))
    data_new['manufacturer'] = manufacturer
    data_new['model'] = model
    data_new['description'] = description
    data_new['transmission'] = transmission
    data_new['transmission_type'] = transmission_type
    data_new['engine_size_cm3'] = engine_size_cm3
    data_new['fuel'] = fuel
    data_new['powertrain'] = powertrain
    data_new['power_ps'] = power_ps
    data_new['co2_emissions_gPERkm'] = co2_emsissions_gPERkm

    temp_data.append(data_new)

    rd.set('vehicle_emissions', json.dumps(temp_data))

@app.route('/delete', methods=['GET'])
def delete_how_to():
    """
    Shows how to use the delete route to get the desired data output.
    Returns:
        string: all of the possible inputs that the server is looking for.
    """

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


@app.route('/jobs', methods=['POST'])
def jobs_api():
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created.
    """
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job['start'], job['end']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = '5005')
