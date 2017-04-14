from scrapy.conf import settings

def get_elasticsearch_base_url():
  return ''.join(["http://", settings['ELASTICSEARCH_SERVER'], ":", settings['ELASTICSEARCH_PORT'], "/"])

