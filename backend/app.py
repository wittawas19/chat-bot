from datetime import datetime
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['db_chatbot']
chats_collection = db['chatRoom']
message_collection = db['message']

app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/addChat', methods=['POST'])
def create_chat():
    data = request.get_json()
    data['date_created'] = datetime.now()  # Set the date_created field with the current date and time
    chat_id = chats_collection.insert_one(data).inserted_id
    return jsonify({'message': 'Chat created successfully', 'chat_id': str(chat_id)}), 201

@app.route('/getchat', methods=['GET'])
def get_chat_list():
    # Retrieve the list of chats from the database
    chat_list = list(chats_collection.find())

    for chat in chat_list:
        chat['_id'] = str(chat['_id'])
    # Return the response as JSON
    return jsonify(chat_list)

@app.route('/getchatbyid/<chat_id>')
def get_chat(chat_id):
    # Retrieve the chat from the database based on the chat_id
    chat = chats_collection.find_one({'_id': ObjectId(chat_id)})

    if chat:
        # Convert ObjectId to string representation
        chat['_id'] = str(chat['_id'])

        # Return the chat as a JSON response
        return jsonify(chat)
    else:
        return jsonify({'error': 'Chat not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
