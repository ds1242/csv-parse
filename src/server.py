import sqlite3
from flask import Flask, jsonify, request 

app = Flask(__name__)


db_path = './src/batch_jobs.db'

@app.route('/batch_jobs', methods=['GET'])
def get_batch_jobs():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    select_sql = "SELECT * FROM batch_jobs"

    cursor.execute(select_sql)

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
