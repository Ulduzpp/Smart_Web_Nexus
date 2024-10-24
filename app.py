from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import secrets
from form import InputForm  
from model import predict_disease

app = Flask(__name__)

# Configuring app
app.config['SECRET_KEY'] = secrets.token_hex(16)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('login'))

@app.route('/input', methods=['GET', 'POST'])
@login_required
def input_data():
    return render_template('input.html')

@app.route('/result')
@login_required
def result():
    return render_template('result.html')

@app.route('/history')
@login_required
def history():
     return render_template('history.html')

@app.errorhandler(401)
def invalid_credentials(error):
    return render_template('error_401.html'), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('error_403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error_500.html'), 500

if __name__ == '__main__':
        app.run(debug=True)