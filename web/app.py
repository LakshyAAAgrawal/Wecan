from flask import Flask, render_template, request, redirect
from tables import MyTable, Person

app = Flask(__name__)

@app.route('/')
def login():
	return render_template('login.html', invalid="hidden")

@app.route('/retry')
def retry():
	return render_template('login.html', invalid="visible")

@app.route('/authenticate', methods=['POST'])
def authenticate():
	print(request.form['my_email'])
	print(request.form['my_password'])
	return redirect('/retry')

@app.route('/main')
def main():
	items = [Person('Mark','Otto','@twitter', False), Person('Jacob','Thornton','@fat', True), Person('Larry the Bird','','@twitter', False)]
	my_table = MyTable(items)
	return render_template('main.html', table=my_table, title="Cards", organisation_name="Pied Piper", name="Richard Hendricks", lists="active")

if __name__=="__main__":
	app.run(debug=True);