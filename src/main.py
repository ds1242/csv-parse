import os
from flask import Flask, jsonify, request
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
# from model import Data
import csv


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeytousewithflask'
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///batch_jobs.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'batch_jobs.db')


db.init_app(app)

class Data(db.Model):
    __tablename__ = 'batch_jobs'
    id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.Integer, nullable=True)
    submitted_at = db.Column(db.String(50), nullable=True)
    nodes_used = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Data {self.batch_number}>"
    # Method to generate a dictionary based on table information 
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns }
    
with app.app_context():
    db.drop_all()
    db.create_all()


with app.app_context():
    db.session.query(Data).delete()
    with open("example_batch_records.csv", 'r') as fileName:
        reader = csv.reader(fileName, delimiter=",")
        for row in reader:
            
            batch_number = row[0]
            submitted_at= row[1]
            nodes_used = row[2]
            # print(batch_number, submitted_at, nodes_used)
            db.session.add_all([
                Data(batch_number=batch_number, submitted_at=submitted_at, nodes_used=nodes_used)
            ])
    db.session.commit()

@app.route("/batch_jobs", methods=["GET"])
def batch_jobs():
    data = db.session.execute(db.select(Data).order_by(Data.id))
    all_records = data.scalars().all()
    return jsonify({"links": {
                    "self": request.url},
                    "data": [{
                       "id": row.id,
                       "type": "batch_jobs",
                       "attributes": {
                           "batch_number": row.batch_number,
                           "submitted_at": row.submitted_at,
                           "nodes_used": row.nodes_used
                       }
                   } for row in all_records] })


@app.route('/batch_jobs/', methods=["GET"])
def filter_batch_data():
    pass

if __name__ == '__main__':
    app.run(debug=True)
