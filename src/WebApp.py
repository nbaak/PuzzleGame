from flask import Flask, request, jsonify, render_template
from lib.Session import Session
from Game import Game

import settings
import secret_service
import logging

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
    # TODO: settable difficulty
    return render_template('index.html')
    
    
@app.route("/play")
def play(): 
    global sessions
    ip, _ = get_peer(request)
    
    session = Session(ip)
    session.game = Game(5, 4)
    sessions[session.id] = session
    
    return render_template('game.html', session_id=session.id)


@app.route("/api/game/initial", methods=["POST"])
def initial_game(): 
    session_id = request.form['session']
    
    session = sessions[session_id]
    field = session.game.field
    gameover = False
            
    return jsonify({'field': field, 'queue': session.game.queue, 'points': session.game.points, 'step': session.game.step, 'gameover': gameover, 'timeout': False})


@app.route("/api/game/update", methods=["POST"])
def update_game():
    row, col, session_id = int(request.form['row']), int(request.form['col']), request.form['session']
    
    try:
        session = sessions[session_id]
        if col > -1 and row > -1:
            field, gameover = session.update((col, row))
        else:
            field = session.game.field
            gameover = False
            
        if gameover:
            session.close()
            
        return jsonify({'field': field, 'queue': session.game.queue, 'points': session.game.points, 'step': session.game.step, 'gameover': gameover, 'timeout': False})
            
    except KeyError:
        # session got dropped, maybe cleanup
                    
        return jsonify({'field': None, 'queue': None, 'points': 0, 'step': 0, 'gameover': False, 'timeout': True})


@app.route('/cleanup/<string:secret>', methods=['GET'])
def session_cleanup(secret):
    if secret_service.verify(secret, settings.SECRET_FILE):
        sessions_to_remove = []
        for _, session in sessions.items():
            
            if not session.check(max_age=30):
                sessions_to_remove.append(session.id)
                
        if sessions_to_remove:
            for item in sessions_to_remove:
                del sessions[item]
                logging.info(f"removed {item}")
           
        return "SUCCESS", 200

    return "ERROR", 404


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)
    
    app.run(host="0.0.0.0", port=5000, debug=True)