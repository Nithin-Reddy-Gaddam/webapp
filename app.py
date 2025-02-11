from flask import Flask, request, render_template, redirect, url_for
import csv

app = Flask(__name__)


def validate_data(username, email, password):
    if 3 > len(username) < 10:
        return "Username must be 3 to 10 letters"
    if "@" not in email or "." not in email:
        return "Enter a valid email address"
    if len(password) < 8:
        return "password should be minimum of 8 characters"
    return None


def save_to_csv(username, email, password):
    with open('user.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, password])


@app.route('/thankyou')
def thank_you():
    return "<h1> Thank you for signing up!</h1>" \
           "<a href='/login'>Login here</a>"


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        error_message = validate_data(username, email, password)
        if error_message:
            return render_template('signup.html', error=error_message)
        save_to_csv(username, email, password)
        print("data saved to csv")

        return redirect('/thankyou')
    return render_template('signup.html')


def validate_login(username, password):
    with open('user.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                stored_username, stored_email, stored_password = row
                if username == stored_username and password == stored_password:
                    return True
    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if validate_login(username, password):
            return redirect(url_for('welcome', username=username))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/welcome/<username>')
def welcome(username):
    return f"<h1> Welcome {username}!</h1><br> <a href='/logout'>Logout account</a>"


@app.route('/logout')
def logout():
    return render_template('logout.html')


# if __name__ == '__main__':
app.run(debug=True)
