import datetime
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId, ISODate

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['db_chatbot']
chats_collection = db['chatRoom']
message_collection = db['message']


@app.route('/addChat', methods=['POST'])
def create_chat():
    data = request.get_json()
    chat_id = chats_collection.insert_one(data).inserted_id
    return jsonify({'message': 'Chat created successfully', 'chat_id': str(chat_id)}), 201

@app.route('/sendMessage', methods = ['POST'])
def send_message(chatId):
    data = request.get_json()

    message = {
        "id" : ObjectId(),
        "chat_id" : data.get("chat_id"), 
        "order_num":  data.get("order_num"),
        "date_created" : datetime.now(),
        "content":  data.get("content"),
        "has_file": data.get("has_file"), 
        "file_path": data.get("file_path")
    } 

    result = chats_collection.update_one(
        {'_id': ObjectId(chatId)},
        {'$push': {'messages': message}}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Message added successfully'}), 201
    else:
        return jsonify({'message': 'Failed to add message'}), 400



if __name__ == '__main__':
    app.run(debug=True)
