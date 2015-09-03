from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/<username>')
def show_user_profile(username):
	return 'Hello ' + username

@app.route('/<username>/<list>')
def show_user_list(username, list):
	return 'Show list ' + username + '/' + list 

@app.route('/about')
def show_about():
	return 'Insert about page here'

if __name__ == '__main__':
	app.run('0.0.0.0')