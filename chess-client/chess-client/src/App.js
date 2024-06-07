// App.js
import React, { useState, useEffect } from 'react';
import socketIOClient from 'socket.io-client';
import axios from 'axios';
import Chessboard from 'chessboardjsx';
const ENDPOINT = "http://localhost:5000";


function App() {
  const [username, setUsername] = useState("");
  const [playerId, setPlayerId] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const socket = socketIOClient(ENDPOINT);

  useEffect(() => {
    socket.on("game_state", data => {
      if (data.game_id === gameId) {
        setGameState(data.state);
      }
    });
  }, [gameId]);

  useEffect(() => {
    socket.on("game_state", data => {
      if (data.game_id === gameId) {
        setGameState(data.state);
      }
    });
  }, [socket, gameId]); 
  
  const login = async () => {
    const response = await axios.post(`${ENDPOINT}/login`, { username });
    setPlayerId(response.data.id);
  };

  const startGame = async () => {
    const response = await axios.post(`${ENDPOINT}/start_game`, {
      player1_id: playerId,
      player2_id: playerId,  // For testing, I use the same player
    });
    setGameId(response.data.game_id);
    setGameState(response.data.state);
  };

  const handleMove = (move) => {
    socket.emit("move", { game_id: gameId, move });
  };

  return (
    <div>
      <input value={username} onChange={(e) => setUsername(e.target.value)} />
      <button onClick={login}>Login</button>
      <button onClick={startGame}>Start Game</button>
      {gameState && (
        <Chessboard
          position={gameState}
          onDrop={handleMove}
        />
      )}
    </div>
  );
}

export default App;
