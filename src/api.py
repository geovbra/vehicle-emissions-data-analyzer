import json
from flask import Flask, request
import jobs
import csv

app = Flask(__name__)


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
