from flask import Flask, render_template, request, redirect, url_for, session
from chess_engine import *
from flask_session import Session

from routes.users import users
import services.userService as userService
import services.dbService as dbService

app = Flask(__name__)

@app.route("/play")
def index():
    return render_template("play.html")


@app.route('/')
def d():
    return render_template("main-home.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user'] = None
    return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form_data = None
        return render_template('index.html', form_data=form_data)
    else:
        form_data = request.form
        if userService.isEmailExists(form_data['email']):
            error_message = 'User with this email already exists.'
            return render_template('index.html', error_message=error_message, form_data=form_data)
        
        user = userService.insert({
            'name': form_data['name'],
            'email': form_data['email'],
            'password': form_data['password']
        })
        session['user'] = user

        return redirect(url_for('chat'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form_data = None
        return render_template('login.html', form_data=form_data)
    else:
        form_data = request.form
        user = userService.getUser(form_data['email'])

        if user is None:
            error_message = 'User with this email not found.'
            return render_template('index.html', error_message=error_message, form_data=form_data)
        
        if str(user[3]) != str(form_data['password']):
            error_message = 'Invalid Password.'
            return render_template('index.html', error_message=error_message, form_data=form_data)
        
        
        session['user'] = user

        return redirect(url_for('chat'))



@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    print(depth)
    print("Calculating...")
    engine = Engine(fen)
    move = engine.iterative_deepening(depth - 1)
    print("Move found!", move)
    print()
    return move


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


if __name__ == '__main__':
    app.run(debug=True)