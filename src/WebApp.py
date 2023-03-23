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
    ip, port = get_peer(request)
        
    print('/game', ip, port)
    session = Session(ip, port)
    session.game = Game(5, 4)
    sessions[session.id] = session
    
    return render_template('game.html', session_id=session.id)


@app.route("/initial", methods=["POST"])
def initial_game():
    ip, port = get_peer(request)
    
    session_id = request.form['session']
    
    session = sessions[session_id]
    field = session.game.field
    
    print('/update', ip, port, session)
    print(field)
     
        
    return jsonify({'field': field, 'queue': session.game.queue, 'points': session.game.points, 'step': session.game.step})


@app.route("/update", methods=["POST", "GET"])
def update_game():
    ip, port = get_peer(request)
    
    if request.method == 'POST':
        row, col, session_id = int(request.form['row']), int(request.form['col']), request.form['session']
        
        session = sessions[session_id]
        if col > -1 and row > -1:
            field = session.update((col, row))
        else:
            field = session.game.field
        
        print('/update', ip, port, session, row, col)
        print(field)
    
    elif request.method == 'GET':
        print('/update', ip, port)
    
    else:
        exit()        
        
    return jsonify({'field': field, 'queue': session.game.queue, 'points': session.game.points, 'step': session.game.step})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
