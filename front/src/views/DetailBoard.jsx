import React from "react";
import ReactDOM from "react-dom";
import "../assets/css/DetailBoard.css";

function DetailBoard({ board, onClose }) {
  if (!board) return null;

  return ReactDOM.createPortal(
    <div className="detail-board">
      {/* 모달 배경 */}
      <div className="detail-board-overlay" onClick={onClose}></div>

      {/* 모달 컨텐츠 */}
      <div className="detail-board-content">
        <button className="close-button" onClick={onClose}>X</button>
        <h2 className="detail-board-title">{board.title}</h2>
        <p className="detail-board-description">{board.description}</p>
        <div className="detail-board-details">
          <p><strong>제목:</strong> {board.title}</p>
          <p><strong>내용:</strong> {board.description}</p>
          <p><strong>도로 구간:</strong> {board.roadSection}</p>
          <p><strong>전화번호:</strong> {board.phoneNumber}</p>
          <p><strong>이메일:</strong> {board.email}</p>
          <p className="detail-board-date">등록일: {new Date(board.createdAt).toLocaleString()}</p>
        </div>
      </div>
    </div>,
    document.body // React Portal을 사용하여 body에 렌더링
  );
}

export default DetailBoard;
