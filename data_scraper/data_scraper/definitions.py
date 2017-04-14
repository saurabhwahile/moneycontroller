from data_scraper.utils import get_elasticsearch_base_url
NEWS = 'NEWS'
STOCK = 'STOCK'
VOLUME_SHOCKERS = 'VOLUME_SHOCKERS'


ES_BASE_URL = get_elasticsearch_base_url()
ES_MCINDEX_URL = ''.join([ES_BASE_URL, "moneycontroller/"])
ES_MCSTOCK_INDEX_URL = ''.join([ES_MCINDEX_URL, "stocks/"])
ES_MCVOLUMESHOCKER_URL = ''.join([ES_MCINDEX_URL, "volume_shockers/"])
ES_MCNEWS_URL = ''.join([ES_MCINDEX_URL, 'news/'])