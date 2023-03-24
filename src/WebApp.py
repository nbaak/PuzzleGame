from flask import Flask, request, jsonify, render_template
from lib.Session import Session
from Game import Game

app = Flask(__name__)
sessions = {}


def get_peer(request:request):
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.environ:
        ip = request.remote_addr
        
    port = request.environ['REMOTE_PORT']
    
    return ip, port


@app.route("/")
def index():
    return 'Hello Worlds'
    
    
@app.route("/game")
def game(): 
    global sessions
    ip, _ = get_peer(request)
    
    session = Session(ip)
    session.game = Game(5, 4)
    sessions[session.id] = session
    
    return render_template('game.html', session_id=session.id)


@app.route("/initial", methods=["POST"])
def initial_game(): 
    session_id = request.form['session']
    
    session = sessions[session_id]
    field = session.game.field
    gameover = False
            
    return jsonify({'field': field, 'queue': session.game.queue, 'points': session.game.points, 'step': session.game.step, 'gameover': gameover})


@app.route("/update", methods=["POST"])
def update_game():
    row, col, session_id = int(request.form['row']), int(request.form['col']), request.form['session']
    
    session = sessions[session_id]
    if col > -1 and row > -1:
        field, gameover = session.update((col, row))
    else:
        field = session.game.field
        gameover = False
        
    return jsonify({'field': field, 'queue': session.game.queue, 'points': session.game.points, 'step': session.game.step, 'gameover': gameover})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
