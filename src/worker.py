import jobs
from hotqueue import HotQueue
import redis
import sys
import numpy as np
import matplotlib.pyplot as plt       
import json

q = HotQueue("queue", host=sys.argv[1], port=6379, db=1)
rd = redis.StrictRedis(host=sys.argv[1], port=6379, db=0)
jd = redis.StrictRedis(host=sys.argv[1], port=6379, db=2)

@q.worker
def execute_job(jid):
    
    jobs.update_job_status(jid, 'in progress')

    jobid = jobs.generate_job_key(jid).encode()

    job_info = jd.hgetall(jobid)
    
    data = json.loads(rd.get('vehicle_emissions'))

    if job_info['plot_type'.encode()].decode() == "bar":
        field_1 = job_info['field_1'.encode()].decode()
        field_2 = job_info['field_2'.encode()].decode()
        x_axis = []
        y_axis = []
        total = 0
        iters = 0
        for row in data['vehicle_emissions']:
            if row[field_1] not in x_axis:
                x_axis.append(row[field_1])

        for row in x_axis:
            for wor in data['vehicle_emissions']:
                if row == wor[field_1]:
                    iters += 1
                    total += float(wor[field_2])

            average = total/iters
            y_axis.append(average)
            iters = 0
            total = 0

        plt.bar(x_axis, y_axis, width = 0.3)

        plt.title('{} vs {}'.format(field_1, field_2))
        plt.xlabel(field_1)
        plt.ylabel(field_2)
        plt.savefig('bar_plot.png')
        
        with open('bar_plot.png', 'rb') as f:
            img = f.read()

        jd.hset(jobid, 'image', img)
        jd.hset(jobid, 'status', 'finished')

    elif job_info['plot_type'.encode()].decode() == "scatter":

        field_1 = job_info['field_1'.encode()].decode()
        field_2 = job_info['field_2'.encode()].decode()
        x_axis = []
        y_axis = []

        for row in data['vehicle_emissions']:
            x_axis.append(float(row[field_1]))

        for row in data['vehicle_emissions']:
            y_axis.append(float(row[field_2]))

        plt.scatter(x_axis, y_axis, c = "red", marker =".", markersize=1)

        plt.title('{} vs {}'.format(field_1, field_2))
        plt.xlabel(field_1)
        plt.ylabel(field_2)
        plt.savefig('scatter_plot.png')

        with open('scatter_plot.png', 'rb') as f:
            img = f.read()

        jd.hset(jobid, 'image', img)
        jd.hset(jobid, 'status', 'finished')

    else:
        jd.hset(jobid, 'status', 'cancelled (invalid job type)')

execute_job()
