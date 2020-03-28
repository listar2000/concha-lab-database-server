from concha import create_app
from concha.database import get_db, parse_filter
from flask import request
import json

app = create_app()

@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"

get_data_template = "SELECT * FROM cdc_NAL {} LIMIT {};"

@app.route('/api/summary', methods=['GET'])
def get_data_summary():
    cursor = get_db().cursor()
    limit = request.args.get('limit', 10)
    queries = []
    for key in request.args:
        if key != "limit":
            val = request.args.get(key)
            queries.append(parse_filter(key, val))
    
    if len(queries) > 0:
        conditions = "WHERE " + ' AND '.join(queries)
    else:
        conditions = ""
    
    print(conditions)
        
    filter_query = get_data_template.format(conditions, limit)
    cursor.execute(filter_query)
    results = cursor.fetchall()

    cursor.close()
    return json.dumps(results)
