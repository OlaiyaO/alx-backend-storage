#!/usr/bin/env python3
"""
Code to return the list of schools having a specific topic in Python?
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    schools_by_topic function finds schools having a specific value
    """
    return mongo_collection.find({"topics":  {"$in": [topic]}})
