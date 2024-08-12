#!/usr/bin/env python3
"""
Code to insert a new document in a collection with Python
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    insert_school function inserts a documents into a collection
    """
    data = mongo_collection.insert_one(kwargs)
    return data.inserted_id
