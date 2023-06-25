import React, { useEffect, useState } from 'react';
import './ComponentCss/chatBar.css';
import ChatRoom from './chatRoom.js';
import axios from 'axios';

const link = "http://127.0.0.1:5000/getchat";
const linkAdd = "http://127.0.0.1:5000/addChat"

const ChatBar = () => {
  const [chat, setChat] = useState([]);
  
  const handleClick = (e) => {
    console.log(e.target)
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
            <button key={item._id} onClick={handleClick}>
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