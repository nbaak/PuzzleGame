from flask import Flask, request, jsonify, render_template
import requests, json

app = Flask(__name__)

# TODO: Session storage
sessions = {}

rows = 4
cols = 5
field = [[i+r for i in range(cols)] for r in range(rows)]
queue = [i for i in range(10)]

@app.route("/")
def index():
    return 'Hello Worlds'
    
    
@app.route("/game")
def game():
    return render_template('game.html')

@app.route("/update", methods=["POST", "GET"])
def update_game():
    global field
    
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.environ:
        ip = request.remote_addr
        
    print(ip)
    
    if request.method == 'POST':
        row, col = int(request.form['row']), int(request.form['col'])
        field[row][col] += 1
    
        
    return jsonify({'field': field, 'queue': queue})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
