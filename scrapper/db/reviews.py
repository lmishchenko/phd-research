from pymongo import MongoClient

from configuration.resolver import configuration

database_name = 'fakes-radar'

if configuration.needs_auth():
    client = MongoClient(host=configuration.mongo_host(),
                         port=configuration.mongo_port(),
                         username=configuration.mongo_user(),
                         password=configuration.mongo_password(),
                         authSource=database_name)
else:
    client = MongoClient(host=configuration.mongo_host(), port=configuration.mongo_port())

database = client[database_name]
reviews_collection = database.reviews
