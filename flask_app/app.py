from flask import Flask, request, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# Set up MongoDB client
mongo_uri = f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@mongodb:27017/project?authSource=admin"
client = MongoClient(mongo_uri)
db = client.project

@app.route('/')
def index():
    # Get data from MongoDB and print in a table
    data = db.data_collection.find()
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.get('data')
    temp = request.form.get('temperature')
    if data:
        db.data_collection.insert_one({'data': data, 'temperature': temp})
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
