#!/usr/bin/env python3
"""
display statistics from Nginx logs stored in a MongoDB collection.
Database: logs, Collection: nginx. Display matched the example:
- First line: x logs, the total number of documents in the collection.
- Second line: Methods
- Five lines listing the count for each HTTP method 
["GET", "POST", "PUT", "PATCH", "DELETE"]
- One line showing the count for GET requests to the /status path.
"""
from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    """
    Function Prototype: def log_stats(mongo_collection, option=None):
    Display statistics for Nginx logs stored in a MongoDB collection.
    """
    i = {}
    if option:
        value = mongo_collection.count_documents(
            {"method": {"$regex": option}})
        print(f"\tmethod {option}: {value}")
        return

    result = mongo_collection.count_documents(i)
    print(f"{result} logs")
    print("Methods:")
    for method in METHODS:
        log_stats(nginx_collection, method)
    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_stats(nginx_collection)
