import React, { useState } from "react";
import "../assets/css/RegisterBoard.css";

function RegisterBoard({ addBoard }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [roadSection, setRoadSection] = useState("");
  const [carbonEmission, setCarbonEmission] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!title || !description || !roadSection || !phoneNumber || !email) {
      alert("모든 필드를 채워주세요.");
      return;
    }

    const newBoard = {
      title,
      description,
      roadSection,
      phoneNumber,
      email,
      createdAt: new Date().toISOString(),
    };

    addBoard(newBoard);
    
    alert("게시판이 성공적으로 등록되었습니다!");

    // 초기화
    setTitle("");
    setDescription("");
    setRoadSection("");
    setPhoneNumber("");
    setEmail("");
  };

  return (
    <div className="register-board">
      <h2 className="form-title">게시판 등록</h2>
      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-group">
          <label htmlFor="title">제목</label>
          <input
            type="text"
            id="title"
            className="form-input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="게시판 제목을 입력하세요"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">설명</label>
          <textarea
            id="description"
            className="form-textarea"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="게시판 내용을 입력하세요"
          />
        </div>

        <div className="form-group">
          <label htmlFor="roadSection">도로 구간</label>
          <input
            type="text"
            id="roadSection"
            className="form-input"
            value={roadSection}
            onChange={(e) => setRoadSection(e.target.value)}
            placeholder="예: 서울 강남대로"
          />
        </div>

        <div className="form-group">
          <label htmlFor="phoneNumber">전화번호</label>
          <input
            type="text"
            id="phoneNumber"
            className="form-input"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="전화번호를 입력하세요"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">이메일</label>
          <input
            type="email"
            id="email"
            className="form-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="이메일을 입력하세요"
          />
        </div>

        <button type="submit" className="form-button">게시판 등록</button>
      </form>
    </div>
  );
}

export default RegisterBoard;
