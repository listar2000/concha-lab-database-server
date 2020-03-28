import sqlite3
import re
import os
from flask import g
from concha import create_app

app = create_app()

DATABASE = os.getcwd() + '/data/concha-lab.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

### The below are sql operations ###

"""
due to sqlite naming rule, we have flipped some column names when constructing
the database
"""
translate_dict = {
    "k1" : "1k", "k2" : "2k", "k3" : "3k", "k4" : "4k", "k6" : "6k",
    "k8" : "8k", "k500": "500k"
}

"""
queries with the following key need to have quotation marks around their value
"""
str_list = ["test_date", "gender", "region", "NAICS_descr"]

numeric_regex = r"^(([0-9]*)|(([0-9]*)\.([0-9]*)))$"

def parse_filter(key, condition: str):
    if condition.startswith(('>=', '<=')):
        sign, body = condition[:2], condition[2:]
    elif condition.startswith(('>', '<', '=')):
        sign, body = condition[:1], condition[1:]
    else:
        return None
    
    if key in str_list:
        query = f'{key}{sign}"{body}"'
    elif not re.match(numeric_regex, body):
        return None
    else:
        query = f'{key}{condition}'
    
    return query