from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    new_game_info = {'gameId': game_id, 'board': game.board}

    return jsonify(new_game_info)


@app.post('/api/score-word')
def score_word():

    game_id = request.json['gameId']
    curr_word = request.json['wordInput']
    game = games[game_id]
    word_list = game.word_list
    result = {'result': "not-word"}
    breakpoint()
    if game.check_word_on_board(curr_word):
        if word_list.check_word(curr_word):
            result['result'] = 'ok'
    else:
        result['result'] = 'not-on-board'

    return jsonify(result)
