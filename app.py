from flask import Flask, render_template
from dotenv import load_dotenv
from flask import request, session
from flask_wtf.csrf import CSRFProtect
from utils import forms
import os
import random

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
csrf = CSRFProtect(app)


@app.route('/')
def index():
    form = forms.StartForm()
    return render_template('index.html', form=form)


@app.route('/start', methods=['POST'])
def start():
    form = forms.StartForm(request.form)
    if form.validate_on_submit():
        players = {
            'player1': form.player1.data,
            'player1_score': 0,
            'player2': form.player2.data,
            'player2_score': 0,
            'current_player': 'player1',
            'current_score': 0,
            'round_scores': '',
            'dice': 5
        }
        session['players'] = players
        return render_template('game_form.html', players=players)
    else:
        return render_template('player_form.html', form=form)


@app.route('/game', methods=['GET'])
def game():
    players = session.get('players')
    return render_template('game.html', players=players)


@app.route('/winner', methods=['GET'])
def winner():
    players = session.get('players')
    return render_template('winner.html', players=players)


@app.route('/roll', methods=['GET'])
def roll():
    players = session.get('players')
    #  randomize the dice
    players['dice'] = random.randint(1, 6)
    players['current_score'] += players['dice']
    players['round_scores'] += ' ['+str(players['dice']) + ']'

    if players['dice'] == 1:
        players['current_score'] = 0
        players['round_scores'] = ''
        players['current_player'] = 'player2' if players['current_player'] == 'player1' else 'player1'

    session['players'] = players
    if players[players['current_player'] + '_score'] + players['current_score'] >= 20:
        players[players['current_player'] +
                '_score'] += players['current_score']
        return render_template('winner.html', players=players)
    return render_template('game_form.html', players=players)


@app.route('/hold', methods=['GET'])
def hold():
    players = session.get('players')
    if players['current_player'] == 'player1':
        players['current_player'] = 'player2'
    else:
        players['current_player'] = 'player1'
    session['players'] = players
    return render_template('game_form.html', players=players)


@app.route('/exit', methods=['GET'])
def exit():
    session.pop('players', None)
    return render_template('player_form.html', form=forms.StartForm())


if __name__ == '__main__':
    app.run()
