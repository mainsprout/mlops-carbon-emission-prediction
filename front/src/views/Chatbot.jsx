import React, { useState } from "react";
import axios from "axios";
import "../assets/css/Chatbot.css";  // Chatbot.css 파일을 import

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const apiKey = "";

  const sendMessage = async () => {
    if (input.trim()) {
      // 1) 사용자가 입력한 메시지를 화면에 표시
      const userMessage = { text: input, sender: "user" };
      setMessages((prev) => [...prev, userMessage]);
      setInput("");

      try {
        // 2) FastAPI 서버에 POST 요청
        const response = await axios.post("http://localhost/chat/", {
          message: input,
          api_key: apiKey,
        });
          
          console.log(response)

        // 3) ChatGPT의 응답을 화면에 표시
        const botMessage = { text: response.data.answer, sender: "bot" };
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        // 4) 에러 발생 시 에러 메시지 표시
        const errorMessage = {
          text: "Error: Unable to fetch response.",
          sender: "bot",
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    }
  };

  // 엔터 키로 전송할 수도 있게 추가 구현 (선택사항)
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}       // 엔터키 이벤트
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
