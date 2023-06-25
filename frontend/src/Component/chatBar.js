import React from 'react'
import './ComponentCss/chatBar.css'
import ChatRoom from './chatRoom.js'
const ChatBar = () => {
  
  return (
    <div className="sidebar">
        <div className='appName'> <h2 >ChatBot simple</h2> </div> 
        <ul className='history'>
          <nav>
          <ChatRoom/>
          </nav> 
        </ul>
        <button className='addChat'  >+ New Chat</button>
    </div>
  )
}
export default ChatBar; 

