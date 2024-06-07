// Chessboard.js
import React from 'react';
import Chessboard from 'chessboardjsx';

const ChessboardComponent = ({ position, onDrop }) => {
  return (
    <Chessboard
      position={position}
      width={400}
      draggable={true}
      onDrop={onDrop}
    />
  );
};

export default ChessboardComponent;
