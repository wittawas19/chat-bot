from datetime import datetime
import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json
from flask_cors import CORS

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['db_chatbot']
chats_collection = db['chatRoom']
message_collection = db['message']

app = Flask(__name__)
CORS(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        
        elif isinstance(self,datetime): 
            return str(o)

        return json.JSONEncoder.default(self, o)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/addChat', methods=['POST'])
def create_chat():
    data = request.get_json()
    data['date_created'] = str(datetime.now())
    chat_id = chats_collection.insert_one(data).inserted_id
    return jsonify({'message': 'Chat created successfully', '_id': str(chat_id)}), 201

@app.route('/sendMessage/<chatId>', methods = ['POST'])
def send_message(chatId):
    data = request.get_json()

    message = {
        "id" : ObjectId(),
        "chat_id" : data.get("chat_id"), 
        "is_user":  data.get("is_user"),
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
    
    
@app.route('/getchat',methods=['GET'])
def get_chat_list():
    # Retrieve the list of chats from the database
    chat_list = list(chats_collection.find())
    
    chat = JSONEncoder().encode(chat_list)

    # Return the response as JSON
    return jsonify(chat)

@app.route('/getchatbyid/<chat_id>' ,methods=['GET'])
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
     
    
@app.route('/change_icon/<chat_id>', methods=['POST'])
def change_chat_icon(chat_id):
    # Check if the chat exists
    chat = chats_collection.find_one({'_id': ObjectId(chat_id)})
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404

    # Retrieve the uploaded image file
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Perform any necessary validations on the file, such as checking the file extension or size

    # Get the file extension from the original filename
    _, file_extension = os.path.splitext(file.filename)

    save_directory = f'image'
    os.makedirs(save_directory, exist_ok=True)

    # Save the image file with the original file extension
    file_path = f'{save_directory}/{chat_id}{file_extension}'
    file.save(file_path)

    # Update the chat document with the new icon_path
    chats_collection.update_one({'_id': ObjectId(chat_id)}, {'$set': {'icon_path': file_path}})

    return jsonify({'message': 'Chat icon updated successfully'})
    
if __name__ == '__main__':
    app.run(debug=True)
