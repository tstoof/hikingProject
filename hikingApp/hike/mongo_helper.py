# mongo_helper.py (no models.py needed)
import pymongo
from django.conf import settings

class MongoDBHelper:
    def __init__(self):
        # Connect to MongoDB using the URI from settings
        self.client = pymongo.MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]

    def get_collection(self, collection_name):
        """Return a specific collection"""
        return self.db[collection_name]

    def insert_document(self, collection_name, document):
        """Insert a document into a collection"""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id

    def find_documents(self, collection_name, query):
        """Find documents that match a query"""
        collection = self.get_collection(collection_name)
        return collection.find(query)

    def update_document(self, collection_name, query, update):
        """Update a document in a collection"""
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {"$set": update})
        return result.modified_count
