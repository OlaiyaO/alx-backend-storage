#!/usr/bin/env python3
"""
Code to list all documents in Python
"""
import pymongo


def list_all(mongo_collection):
    """
    list_all function lists all doc in a collection
    """
    if not mongo_collection:
        return []
    documents = mongo_collection.find()
    return [post for post in documents]
