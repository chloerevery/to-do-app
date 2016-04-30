from flask import Flask, request, render_template
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
def starting_page():

	table = Todo.query.all()
	print(table)

	return render_template('index.html')

@app.route('/', methods = ['POST'])
def insert():
	text = request.form['newtodo']
	toAdd = Todo(text)

	db.session.add(toAdd)
	db.session.commit();

	table = Todo.query.all()
	print(table)
	
	return render_template('index.html')





if __name__ == '__main__':
	app.debug=True          #restarts every time you change code
	app.run()