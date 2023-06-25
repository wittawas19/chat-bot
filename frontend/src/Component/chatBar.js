import React, { useEffect, useState } from 'react';
import './ComponentCss/chatBar.css';
import ChatRoom from './chatRoom.js';
import axios from 'axios';

const link = "http://127.0.0.1:5000/getchat";

const ChatBar = () => {
  const [chat, setChat] = useState([]);
  
  const handleSubmit = (e) => {
    console.log(e.target.data)
  }

  useEffect(() => {
    axios.get(link)
      .then(response => {
        const parsedData = JSON.parse(response.data);
        setChat(parsedData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div className="sidebar">
      <div className='appName'>
        <h2>ChatBot simple</h2>
      </div>
      <ul className='history'>
        <form>
          {chat.map(item => (
            <button key={item._id} onSubmit={handleSubmit}>
              <ChatRoom chat={item._id}/>
            </button>
          ))}
        </form>
      </ul>
      <button className='addChat'>+ New Chat</button>
    </div>
  );
};

export default ChatBar;