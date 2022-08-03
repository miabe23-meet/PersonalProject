from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyCS1YDRaYGUaZ3XaL9qGdjWF6aSByVAAaU",
  "authDomain": "bloglobal.firebaseapp.com",
  "projectId": "bloglobal",
  "storageBucket": "bloglobal.appspot.com",
  "messagingSenderId": "417437818626",
  "appId": "1:417437818626:web:f78c14afb53b5e115f6c1b",
  "measurementId": "G-8XV9C5GCDX",
  "databaseURL": "https://bloglobal-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

@app.route('/')
def home():
	if 'user' in login_session:
		if login_session['user'] is None:
		 	name = {"name":"user"}
		 	ok=True
		else:
			name=db.child("users").child(login_session['user']['localId']).get().val()
			ok=False
	return render_template("index.html",name = name, display= ok)


@app.route('/about')
def about():
	if login_session['user'] is None:
	 	name = {"name":"user"}
	 	ok=True
	else:
		name=db.child("users").child(login_session['user']['localId']).get().val()
		ok=False
	return render_template("about.html" , name=name, display=ok)


@app.route('/signUp' , methods=['GET', 'POST'])
def signUp():
	if login_session['user'] is None:
	 	name = {"name":"user"}
	 	ok=True
	else:
		name=db.child("users").child(login_session['user']['localId']).get().val()
		ok=False
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user={
			"name": request.form['name'] ,
			"email": request.form['email'] ,
			"password": request.form['password']
			}
			db.child("users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("signUp.html", name=name , display=ok)



@app.route('/signIn' , methods=['GET', 'POST'])
def signIn():
	if login_session['user'] is None:
	 	name = {"name":"user"}
	 	ok=True
	else:
		name=db.child("users").child(login_session['user']['localId']).get().val()
		ok=False
	error = ""
	if request.method == 'POST':
		print('12345678')

		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] =auth.sign_in_with_email_and_password(email, password)
			print('egfhsvfhs')
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("signin.html", name=name)


@app.route('/post')
def post():
	if login_session['user'] is None:
	 	name = {"name":"user"}
	 	ok=True
	else:
		name=db.child("users").child(login_session['user']['localId']).get().val()
		ok=False
	return render_template("post.html", name = name, display=ok )

@app.route('/signOut')
def signOut():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug = True)
