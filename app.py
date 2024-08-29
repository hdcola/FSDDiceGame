from flask import Flask, render_template
from dotenv import load_dotenv
from flask import request, session
from flask_wtf.csrf import CSRFProtect
from utils import forms
import os

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
            'player2_score': 0
        }
        session['players'] = players
        return render_template('game_form.html', players=players)
    else:
        return render_template('player_form.html', form=form)


@app.route('/game', methods=['GET'])
def game():
    players = session.get('players')
    return render_template('game.html', players=players)


if __name__ == '__main__':
    app.run()
