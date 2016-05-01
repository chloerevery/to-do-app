from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['POSTGRES_DATABASE_URI'] = 'postgres://bobby@localhost:5432/scrape'
db = SQLAlchemy(app)



class Todo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	text = db.Column(db.String(120))
	checked = db.Column(db.Boolean)

	def __init__(self,text):
		self.text = text
		self.checked = False

	def __repr__(self):
		return '<Todo %r %r %r>' % (self.id,self.text,self.checked)


db.create_all()




@app.route('/')
def starting_page(): #this is called when the user has not yet entered any todos, including the first time they visit the page

	table = Todo.query.all()
	print("here")
	print(table)
	todos = Todo.query.all()
	print("todos contents:")
	print(todos)

	return render_template('index.html',
							todos=todos)



@app.route('/', methods = ['POST'])
def insert():
	print("got here")
	text = request.form['newtodo']
	if len(text)>0: # a teeny bit of validation
		print("text = " + text)
		toAdd = Todo(text)

		db.session.add(toAdd)
		db.session.commit();
		return redirect('/') # a redirect clears the form input

	todos = Todo.query.all()
	print("todos query results:")
	print(todos)
	
	return render_template('index.html',
							todos=todos)
	





if __name__ == '__main__':
	app.debug=True          #restarts every time you change code
	app.run()