#!/usr/bin/env python3
"""
Code that changes all topics of a school document based on name
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    update_topic changess all topics of a document with a specific attr: value
    """
    return mongo_collection.update_many({
            "name": name
        },
        {
            "$set": {
                "topics": topics
            }
        })
