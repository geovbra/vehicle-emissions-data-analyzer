import jobs
from hotqueue import HotQueue
import redis
import sys

q = HotQueue("queue", host=sys.argv[1], port=6379, db=1)
rd = redis.StrictRedis(host=sys.argv[1], port=6379, db=0)
jd = redis.StrictRedis(host=sys.argv[1], port=6379, db=2)

@q.worker
def execute_job(jid):
    jobs.update_job_status(jid, 'in progress')
    time.sleep(15)
    jobs.update_job_status(jid, 'complete')

execute_job()
