from datetime import datetime
import os
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
