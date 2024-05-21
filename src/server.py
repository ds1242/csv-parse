import sqlite3
from flask import Flask, jsonify, request 

app = Flask(__name__)


db_path = './src/batch_jobs.db'

@app.route('/batch_jobs', methods=['GET'])
def get_batch_jobs():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    select_sql = "SELECT * FROM batch_jobs WHERE 1=1"
    # print(request.args.get('[min_nodes]'))
    min_nodes = request.args.get('filter[min_nodes]')
    max_nodes = request.args.get('filter[max_nodes]')
    submitted_before = request.args.get('filter[submitted_before]')
    submitted_after = request.args.get('filter[submitted_after]')


    query_params = []

    if min_nodes:
        select_sql += 'AND nodes_used >= ?'
        query_params.append(min_nodes)

    if max_nodes:
        select_sql += 'AND nodes_used <= ?'
        query_params.append(max_nodes)

    if submitted_before:
        select_sql += 'AND submitted_at <= ?'
        query_params.append(submitted_before)

    if submitted_after:
        select_sql += 'AND submitted_at >= ?'
        query_params.append(submitted_after)

    cursor.execute(select_sql, query_params)

    rows = cursor.fetchall()

    results = []
    for row in rows:
        record = {
            "batch number": row[0],
            "submitted_at": row[1],
            "nodes_used": row[2]
        }
        results.append(row)

    connection.close()
    return jsonify({"links": {
        "self": request.url},
        "data": [{
            "id": row[0],
            "type": "batch_jobs",
            "attributes": {
                "batch_number": row[0],
                "submitted_at": row[1],
                "nodes_used": row[2]
                }
            } for row in results]})

if __name__ == "__main__":
    app.run(debug=True)
