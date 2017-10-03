from data_scraper.utils import get_elasticsearch_base_url
NEWS = 'NEWS'
STOCK = 'STOCK'
VOLUME_SHOCKERS = 'VOLUME_SHOCKERS'
COMMENTS = 'COMMENTS'

ES_BASE_URL = get_elasticsearch_base_url()
ES_MCINDEX_URL = ''.join([ES_BASE_URL, "moneycontroller/"])