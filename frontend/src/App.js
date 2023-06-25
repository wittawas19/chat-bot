import logo from './logo.svg';
import './App.css';
import  ChatBar  from './Component/chatBar';
import MessageBox from './Component/messageBox';

function App() {
  return (
    <div className="App">
       <div>
        <ChatBar/>
        </div>
        <div className='back-ground'>
        <MessageBox/>
        </div>
    </div>
  );
}

export default App;
