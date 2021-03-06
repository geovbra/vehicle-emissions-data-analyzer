import uuid
from hotqueue import HotQueue
import redis
import sys

q = HotQueue("queue", host=sys.argv[1], port=6379, db=1)
rd = redis.StrictRedis(host=sys.argv[1], port=6379, db=0)
jd = redis.StrictRedis(host=sys.argv[1], port=6379, db=2)

def generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def generate_job_key(jid):
    """
    Generate the redis key from the job id to be used when storing, retrieving or updating
    a job in the database.
    """
    return 'job.{}'.format(jid)

def instantiate_job(jid, status, plot_type, field_1, field_2):
    """
    Create the job object description as a python dictionary. Requires the job id, status,
    start and end parameters.
    """
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'plot_type': plot_type,
                'field_1': field_1,
                'field_2': field_2
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'plot_type': plot_type.decode('utf-8'),
            'field_1': field_1.decode('utf-8'),
            'field_2': field_2.decode('utf-8')
    }

def get_job_by_id(jid):
    
    return jd.hgetall(generate_job_key(jid).encode())

def save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    jd.hset(job_key, mapping=job_dict) 

def queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(plot_type, field_1, field_2, status="submitted"):
    """Add a job to the redis queue."""
    jid = generate_jid()
    job_dict = instantiate_job(jid, status, plot_type, field_1, field_2)
    save_job(generate_job_key(jid), job_dict)
    queue_job(jid)
    return job_dict

def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job = get_job_by_id(jid)
    if job:
        job['status'] = status
        save_job(generate_job_key(jid), job)
    else:
        raise Exception()
