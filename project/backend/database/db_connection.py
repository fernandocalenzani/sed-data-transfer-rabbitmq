from infra.config.env import ENV
from pymongo import MongoClient


class Database:

    def connect():
        client = MongoClient(ENV['MONGO_HOST'])

        try:
            client.admin.command('ping')
            db = client.get_database(ENV['MONGO_DB'])
            print(f"|  DATABASE  : OK")
            return [client, db]
        except Exception as e:
            print(e)
