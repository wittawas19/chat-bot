import React, { useEffect } from 'react';
import './ComponentCss/messageBox.css';
import Message from './message.js';
import axios from 'axios';

const MessageBox = () => {
  useEffect(() => {
    fetchData();
  }, []);

  const link = "http://localhost:5000/"

  const fetchData = async () => {
    try {
      const response = await axios.get( link + '');
      const data = response.data;
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };
  const handleSubmit = (e) => {
    e.preventDefault()
    console.log(e.target[1].value)
  }

  return (
    <div className="message">
      <div className='chat-title'>
        <h2 className='chat-name-text'> Chat Room 1 </h2>
      </div>
      <div className='bot-res'>
        <Message />
      </div>
      <form className='text-input' onSubmit={handleSubmit}>

        <button className='upload'> + </button>
        <input className='text-box' type="text" placeholder='text'>
        </input>
        <button className='send' placeholder=''> {'>'} </button>

      </form>
    </div>
  )
}

export default MessageBox