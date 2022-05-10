import jobs
from hotqueue import HotQueue
import redis
import sys
import numpy as np
import matplotlib.pyplot as plt       

q = HotQueue("queue", host=sys.argv[1], port=6379, db=1)
rd = redis.StrictRedis(host=sys.argv[1], port=6379, db=0)
jd = redis.StrictRedis(host=sys.argv[1], port=6379, db=2)

@q.worker
def execute_job(jid):
    
    jobs.update_job_status(jid, 'in progress')



    job_info = jd.hget(jobs.generate_job_key(jid))

    if job_info['plot_type'] == bar:

        x_axis = []
        y_axis = []
        total = 0
        iters = 0
        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            if row[job_info['field_1']] not in x_axis:
                x_axis.append(row[job_info['field_1']])

        for row in x_axis:
            for wor in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
                if row == wor[job_info['field_1']]:
                    iters += 1
                    total += float(wor[job_info['field_2']])

            average = total/iters
            y_axis.append(average)
            iters = 0

        plt.bar(x_axis, y_axis, width = 0.3)

        plt.title('{} vs {}'.format(job_info['field_1'], job_info['field_2']))
        plt.xlabel(job_info['field_1'])
        plt.ylabel(job_info['field_2'])
        plt.savefig('bar_plot.png')

        with open('bar_plot.png', 'rb') as f:
            img = f.read()

        jd.hset(jobid, 'image', img)
        jd.hset(jobid, 'status', 'finished')

    if job_info['plot_type'] == scatter:

        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            x_axis.append(float(row[job_info['field_1']]))

        for row in json.loads(rd.get('vehicle_emissions'))['vehicle_emissions']:
            y_axis.append(float(row[job_info['field_2']]))

        plt.scatter(x_axis, y_axis, c = "red")

        plt.title('{} vs {}'.format(job_info['field_1'], job_info['field_2']))
        plt.xlabel(job_info['field_1'])
        plt.ylabel(job_info['field_2'])
        plt.savefig('scatter_plot.png')

        with open('scatter_plot.png', 'rb') as f:
            img = f.read()

        jd.hset(jobid, 'image', img)
        jd.hset(jobid, 'status', 'finished')

    time.sleep(15)
    jobs.update_job_status(jid, 'complete')

execute_job()
