from flask import Flask, render_template, request, session, redirect

import mysql.connector

connection = mysql.connector.connect(host= 'localhost', port = '3306', database = 'NittanyMarket', user='root', password='admin', auth_plugin='mysql_native_password')

cursor = connection.cursor()

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'


app.secret_key = 'xyz'

@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/home')
def home():
    cursor.execute('SELECT * FROM Categories WHERE parent_category=%s ORDER BY category_name Limit 6', ('Root',))
    categs = cursor.fetchall()
    print(categs)
    return render_template('Home.html', categs=categs)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['pass_word'] = request.form['pass_word']
        email = session['email']
        pass_word = session['pass_word']
        cursor.execute('SELECT * FROM Users WHERE email = %s AND pass_word = %s', (email, pass_word))
        query = cursor.fetchall()
        if query:
            #return render_template('Home.html', error=error);
            return redirect('/home')

        else:
            error = 'Incorrect login credentials'

    return render_template('Failure.html', error=error)

@app.route('/account_info')
def account_info():
    email = session['email']
    cursor.execute('SELECT * FROM BUYERS WHERE email=%s', (email,))
    user = cursor.fetchall()
    home_address_id = user[0][5]
    billing_address_id = user[0][6]
    cursor.execute('SELECT * FROM Address WHERE address_id=%s', (home_address_id,))
    home_address = cursor.fetchall()
    zip_code_home = home_address[0][1]
    cursor.execute('SELECT * FROM Zipcode_Info WHERE zipcode=%s', (zip_code_home,))
    zip_code_home = cursor.fetchall()

    cursor.execute('SELECT * FROM Address WHERE address_id=%s', (billing_address_id,))
    bill_address = cursor.fetchall()

    zip_code_bill = bill_address[0][1]
    cursor.execute('SELECT * FROM Zipcode_Info WHERE zipcode=%s', (zip_code_bill,))
    zip_code_bill = cursor.fetchall()

    cursor.execute('SELECT * FROM Credit_Cards WHERE Owner_email=%s', (email,))
    credit_cards = cursor.fetchall()
    if credit_cards:
        print('success')
        print(credit_cards)
    else:
        print('failure')
        print(email)
        print(type(email))

    return render_template('AccountInfo.html', zip_code_home=zip_code_home,zip_code_bill=zip_code_bill,user=user, credit_cards=credit_cards, home_address=home_address, bill_address=bill_address)

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    email = session['email']
    if request.method == 'POST':
        new_password = request.form['new_password']
        cursor.execute('UPDATE Users SET pass_word = %s WHERE email = %s', (new_password, email ))
        connection.commit()

    return redirect('/account_info')



@app.route('/home/categories/<category>', methods=['GET'])
def categories(category):
    cursor.execute('SELECT * FROM Categories WHERE parent_category=%s', (category,))
    categs = cursor.fetchall()

    return render_template('Categories.html', categs=categs)










if __name__ == "__main__":
    app.run(debug=True)


