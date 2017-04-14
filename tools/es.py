import requests
import logging
import datetime
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

ES_BASE_URL = ''.join(["http://", '127.0.0.1', ":", '9200', "/"])

def dump_at_path(path, data):
  data['timestamp'] = datetime.datetime.now().isoformat()
  log.debug(requests.put(''.join([ES_BASE_URL, path]), data=data).text)