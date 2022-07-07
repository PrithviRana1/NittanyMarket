from flask import Flask, render_template, request

import mysql.connector

connection = mysql.connector.connect(host= 'localhost', port = '3306', database = 'NittanyMarket', user='root', password='admin', auth_plugin='mysql_native_password')

cursor = connection.cursor()

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'




@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        pass_word = request.form['password']
        cursor.execute('SELECT * FROM Users WHERE email = %s AND pass_word = %s', (email, pass_word))
        query = cursor.fetchall()
        if query:
            return render_template('Home.html', error=error);

        else:
            error = 'Incorrect login credentials'

    return render_template('Failure.html', error=error)








if __name__ == "__main__":
    app.run()


