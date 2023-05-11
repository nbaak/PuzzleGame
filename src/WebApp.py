from flask import Flask, request, jsonify, render_template, send_file
from lib.Session import Session
from lib.Leaderboard import Leaderboard
from Game import Game

import settings
import secret_service
import logging
from draw import safe_replay
import os

app = Flask(__name__)

sessions = {}
leaderboards = {}


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


@app.route("/leaderboard/<int:width>/<int:height>/<int:level>")
@app.route("/leaderboard/<int:width>/<int:height>", defaults={'level':0})
@app.route("/leaderboard", defaults={'width': 5, 'height': 4, 'level':0})
def ladder(width, height, level):
    
    try:
        board = f"{width}-{height}-{level}"
        leaderboard = leaderboards[board].get()
        
    except KeyError:
        leaderboard = None
    
    return render_template('leaderboard.html', leaderboard=leaderboard)
    

@app.route("/play/<int:width>/<int:height>/<int:level>")
@app.route("/play/<int:width>/<int:height>", defaults={'level':0})
@app.route("/play", defaults={'width': 5, 'height': 4, 'level':0})
def play(width, height, level):
    global sessions
    
    ip, _ = get_peer(request)
    
    width, height = int(width), int(height)
    
    session = Session(ip)
    session.game = Game(width, height, level)
    sessions[session.id] = session
    
    return render_template('game.html', session_id=session.id, game_width=width, game_height=height, game_level=level)


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
            print(len(session.game.replay_field), session.game.step)
            session.close()
            
        return jsonify({'field': field, 'queue': session.game.queue, 'points': session.game.points, 'step': session.game.step, 'gameover': gameover, 'timeout': False})
            
    except KeyError:
        # session got dropped, maybe cleanup
                    
        return jsonify({'field': None, 'queue': None, 'points': 0, 'step': 0, 'gameover': False, 'timeout': True})

    
@app.route("/api/leaderboard", methods=["POST"])
def api_leaderboard():
    global leaderboards
    try:
        session_id = request.form['session']
        username = request.form['username']
        
        session = sessions[session_id]
        if session.closed:
            
            safe_replay(session.game, session.id)
            
            board = f"{session.game.width}-{session.game.height}-{session.game.level}"
            leaderboard = Leaderboard(session.game.width, session.game.height, session.game.level, file_location='./saves')
            leaderboard.add_user(username, session.id, session.points)
            
            leaderboards[board] = leaderboard
        
        return 'SUCCESS', 200
        
    except Exception as e:
        logging.error(str(e))
        return 'ERROR', 404


@app.route('/cleanup/<string:secret>', methods=['GET'])
def session_cleanup(secret:str):
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

@app.route('/api/replay/<string:session_id>', methods=['GET'])
def get_image(session_id:str):
    
    image_path = f"./screenshots/{session_id}/anim.gif"
    
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/gif')


@app.route('/debug/sessions')
def debug_sessions():

    def stamp_to_datetime(ts:float) -> str:
        from time import strftime, localtime
        return strftime("%Y-%m-%-d %H:%M:%S", localtime(ts))
    
    content = ""
    for session in sessions.values():
        content += f"{session.id} - {stamp_to_datetime(session.started)} - {stamp_to_datetime(session.updated)} - {session.game.points}\n"
    
    response = app.response_class(
        response=content,
        status=200,
        mimetype="text/plain"
    )
    
    return response


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s',
                        encoding='utf-8',
                        level=logging.INFO)
    
    # TODO: try to reconnect leaderboards, if some exist
    
    app.run(host="0.0.0.0", port=5000, debug=True)
