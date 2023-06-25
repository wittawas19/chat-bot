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
def send_message(chatId, order):
    data = request.get_json()

    message = {
        "id" : ObjectId(),
        "chat_id" : chatId, 
        "order_num":  order,
        "date_created" : ISODate(),
    } 

    id = message_collection.insert_one(data)
    


if __name__ == '__main__':
    app.run(debug=True)
