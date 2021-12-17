from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User
from flask_login import login_user, logout_user, login_required
import requests
from requests.structures import CaseInsensitiveDict
import json


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        user = User(username, pwd)
        db.session.add(user)
        db.session.commit()

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    username = request.form['username']
    pwd = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Invalid username or password')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('form'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    if request.method == 'POST':
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        sqft_living = request.form['sqft_living']
        sqft_lot = request.form['sqft_lot']
        floors = request.form['floors']
        waterfront = request.form['waterfront']
        view = request.form['view']
        condition = request.form['condition']
        grade = request.form['grade']
        sqft_above = request.form['sqft_above']
        sqft_basement = request.form['sqft_above']
        yr_built = request.form['yr_built']
        yr_renovated = request.form['yr_renovated']
        sqft_living15 = request.form['sqft_living15']
        sqft_lot15 = request.form['sqft_lot15']

        payload = {
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sqft_living": sqft_living,
            "sqft_lot": sqft_lot,
            "floors": floors,
            "waterfront": waterfront,
            "view": view,
            "condition": condition,
            "grade": grade,
            "sqft_above": sqft_above,
            "sqft_basement": sqft_basement,
            "yr_built": yr_built,
            "yr_renovated": yr_renovated,
            "sqft_living15": sqft_living15,
            "sqft_lot15": sqft_lot15
        }

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        price = requests.post(
            'https://projectpricehouse.herokuapp.com/predict', data=json.dumps(payload), headers=headers)
            

        price = price.json()['Price']

        return '''
            <h1>The house price is R$: {}</h1>'''.format(round(price))

    return render_template('form.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=False)
