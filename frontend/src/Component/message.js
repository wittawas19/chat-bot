import React from 'react'
import './ComponentCss/message.css' 

 const Message = () => {
  return (
    <div className='chat-message'>
        <div className='chat-avatar'>
            <img src='https://www.howtogeek.com/wp-content/uploads/2021/07/Discord-Logo-Lede.png?height=200p&trim=2,2,2,2'></img> 
        </div>
        <div className='chat-content'>
            <p className=''>hello</p>
        </div>
    </div>
  )
}
export default Message;