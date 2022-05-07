import json
from flask import Flask, request
import jobs
import csv

app = Flask(__name__)

emissions_data = {}

@app.route('/read_data', methods=['POST'])
def read_data_from_file_into_dict():
    
    """
    Used to read in the data for later use with other functions. (Updates the list of data dictionaries)
    Returns:
        string: informing the user that the data is now available for use.
    """

    logging.debug('used POST to read in data')

    global emissions_data

    with open('uk_gov_data_dense_preproc.csv' , 'r') as f:
        emissions_data = csv.DictReader(f)

    rd.hset('vehicle_emissions', emissions_data)

    return f'Data has been read from file\n'

# now emissions_data will be accessible to other functions


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
