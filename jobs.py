import uuid
from hotqueue import HotQueue
from redis import StrictRedis


 q = HotQueue("queue", host='172.17.0.1', port=6379, db=1)
  rd = redis.StrictRedis(host='172.17.0.1', port=6379, db=0)

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

  def instantiate_job(jid, status, start, end):
      """
      Create the job object description as a python dictionary. Requires the job id, status,
      start and end parameters.
      """
      if type(jid) == str:
          return {'id': jid,
                  'status': status,
                  'start': start,
                  'end': end
          }
      return {'id': jid.decode('utf-8'),
              'status': status.decode('utf-8'),
              'start': start.decode('utf-8'),
              'end': end.decode('utf-8')
      }

  def save_job(job_key, job_dict):
      """Save a job object in the Redis database."""
      rd.hset(.......)

  def queue_job(jid):
      """Add a job to the redis queue."""
      ....

  def add_job(start, end, status="submitted"):
      """Add a job to the redis queue."""
      jid = _generate_jid()
      job_dict = instantiate_job(jid, status, start, end)
      save_job(......)
      queue_job(......)
      return job_dict

  def update_job_status(jid, status):
      """Update the status of job with job id `jid` to status `status`."""
      job = get_job_by_id(jid)
      if job:
          job['status'] = status
          _save_job(_generate_job_key(jid), job)
      else:
          raise Exception()
