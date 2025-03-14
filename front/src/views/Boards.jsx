import React, { useState } from "react";
import "../assets/css/Boards.css";
import DetailBoard from "./DetailBoard"; // DetailBoard 컴포넌트 가져오기

function Boards({ boards }) {
  const [selectedBoard, setSelectedBoard] = useState(null); // 선택된 보드 상태

  const handleCloseModal = () => {
    setSelectedBoard(null); // 모달 닫기
  };

  return (
    <>
      <h1 className="boards-title">카풀 게시판</h1>
      <div className="boards-container">
        {boards.length > 0 ? (
          <ul className="boards-list">
            {boards.map((board, index) => (
              <li
                key={index}
                className="board-item"
                onClick={() => setSelectedBoard(board)} // 보드 클릭 시 상태 업데이트
              >
                <h3 className="board-title">{board.title}</h3>
                <p className="board-description">{board.description}</p>
                <div className="board-details">
                  <p>
                    <strong>도로 구간:</strong> {board.roadSection}
                  </p>
                  <p className="board-date">
                    등록일: {new Date(board.createdAt).toLocaleString()}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-boards">등록된 게시판이 없습니다.</p>
        )}
      </div>

      {/* DetailBoard 모달 */}
      <DetailBoard board={selectedBoard} onClose={handleCloseModal} />
    </>
  );
}

export default Boards;
