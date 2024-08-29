from flask import Flask, render_template
from dotenv import load_dotenv
from flask import request, url_for, redirect
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
        return redirect(url_for('index'))
    else:
        print(form.errors)
        return render_template('player_form.html', form=form)


if __name__ == '__main__':
    app.run()
