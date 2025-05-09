from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://expenseuser:nojUYh2c9WJZMYQy@cluster0.fnfoham.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['expense_tracker']
collection = db['expenses']

@app.route('/')
def home():
    return "Welcome to Expense Tracker Backend!"

@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.json
    data['timestamp'] = datetime.utcnow()
    data['category'] = data.get('category', 'Uncategorized')
    collection.insert_one(data)
    return jsonify({"message": "Expense added!"}), 201

@app.route('/expenses', methods=['GET'])
def list_expenses():
    category = request.args.get('category')
    query = {}
    if category:
        query['category'] = category
    expenses = list(collection.find(query, {"_id": 0}))
    return jsonify(expenses)

@app.route('/expense/<name>', methods=['DELETE'])
def delete_expense(name):
    result = collection.delete_one({'name': name})
    if result.deleted_count == 1:
        return jsonify({'message': 'Expense deleted!'}), 200
    else:
        return jsonify({'message': 'Expense not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
