from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess.db'
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
app.app_context().push()
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String, nullable=False)  # This will hold the board state in FEN notation
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    player = Player.query.filter_by(username=username).first()
    if not player:
        player = Player(username=username)
        db.session.add(player)
        db.session.commit()
    return jsonify({'id': player.id, 'username': player.username})


@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    player1_id = data.get('player1_id')
    player2_id = data.get('player2_id')
    
    if player1_id is None or player2_id is None:
        return jsonify({'error': 'Player IDs are required.'}), 400

    
    initial_state = "startpos"
    
    game = Game(state=initial_state, player1_id=player1_id, player2_id=player2_id)
    db.session.add(game)
    db.session.commit()
    
    return jsonify({'game_id': game.id, 'state': game.state})

@socketio.on('move')
def handle_move(data):
    game_id = data['game_id']
    move = data['move']
    game = Game.query.get(game_id)
    # Update the game state with the new move
    new_state = update_game_state(game.state, move)  # This function needs to be implemented
    game.state = new_state
    db.session.commit()
    emit('move', {'game_id': game_id, 'state': new_state}, broadcast=True)

def update_game_state(current_state, move):
    # This function should update the game state according to the rules of chess
    # Implementing the chess logic is complex and would require a chess engine
    pass

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)
