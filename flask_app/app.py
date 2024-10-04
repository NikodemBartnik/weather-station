from flask import Flask, request, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# Set up MongoDB client
mongo_uri = f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@mongodb:27017/project"
client = MongoClient(mongo_uri)
db = client.project

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.get('data')
    if data:
        db.data_collection.insert_one({'data': data})
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
