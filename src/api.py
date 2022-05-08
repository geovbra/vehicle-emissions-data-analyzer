import json
from flask import Flask, request
import jobs
import csv

app = Flask(__name__)



@app.route('/', methods=['GET'])
def how_to():

    """
    Shows how to use the app to get the results you want.
    Returns: 
        string: all of the possible inputs that the server is looking for.
    """


    logging.debug('used GET to access "how_to"')

    return 'test'


@app.route('/reset', methods=['POST'])
def read_data_from_file_into_dict():
    
    """
    Used to read in the data for later use with other functions. (Updates the list of data dictionaries)
    Returns:
        string: informing the user that the data is now available for use.
    """

    data = {}
    data['vehicle_emissions'] = []
    
    logging.debug('used POST to read in data')

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


    logging.debug('used GET to access "how_to"')

    return 'test_read_how_to'


@app.route('/read/<string:key>', methods=['GET'])
def read(key:str):
    logging.debug('used GET to access specific data specified by a key')

    temp_data = []

    key = f'{key}'

    if key == "all"
        for row in data:
            temp_data.append(row)
    
    else if key == "car_id"
        start = request.args.get('start')
        if type(start) != int
            return 'please use an integer as your query parameter'
        for row in data:
            if row['car_id'] == start
                temp_data.append(row)

    else if key == "manufacturer"
        start = request.args.get('start')
        if type(start) != str
            return 'please use a string as your query parameter'
        for row in data:
            if row['manufacturer'] == start
                temp_data.append(row)

    else if key == "model"
        start = request.args.get('start')
        if type(start) != str
            return 'please use a string as your query parameter'
        for row in data:
            if row['model'] == start
                temp_data.append(row)


    return jsonify(temp_data)

   


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
    app.run(debug=True, host='0.0.0.0')
