from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy


# Setting up the Database. Here we use Postgres hosting on localhost 5432
app = Flask(__name__)
app.config['POSTGRES_DATABASE_URI'] = 'postgres://bobby@localhost:5432/scrape'
db = SQLAlchemy(app)

# Here we define the schema of what will be the Todo Relation. We create an id as a primary
# key and create two additional attributes.
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	text = db.Column(db.String(120))
	checked = db.Column(db.Boolean)

	def __init__(self,text):
		# Constructor. Note that id automatically assigns itself and we predefined every
		# newly created tuple (here, a todo element) to be unchecked until modified
		self.text = text
		self.checked = False

	def __repr__(self):
		# Defines how each tuple appears when printed to the console. Useful for debugging.
		return '<Todo %r %r %r>' % (self.id,self.text,self.checked)


# Creates Relations to be filled
db.create_all()


# Here we define three routes to handle interactions between the database and the front-end
#app

@app.route('/')
def starting_page(): # This is called when the user has not yet entered any todos, 
# including the first time they visit the page. It simply pulls all todo elements from the 
# Todo Relation and populates the app with them

	todos = Todo.query.all()

	#Debugging code that prints the entire Relation to the console. This does not 
	#actually populate the app with the todo elements
	print("todos contents:")
	print(todos)

	return render_template('index.html',
							todos=todos)



@app.route('/', methods = ['POST'])
def insert(): # This is called whenever the 'newtodo' form is submitted, creating a new todo
# element. We create the new tuple, add it to the relation, then commit.
	
	text = request.form['newtodo'] # Retrieves the relevant text from the submitted form
	if len(text)>0: # A teeny bit of validation, useful so that refreshing the page does not
	# resubmit the same tuple, resulting in duplicate entries in the relation
		print("text = " + text)
		toAdd = Todo(text)

		db.session.add(toAdd)
		db.session.commit();
		return redirect('/') # A redirect clears the form input

	return redirect('/') # We return to the starting_page() method so that the app can be
	# populated with the new tuple included

@app.route('/delete/<int:todo_id>', methods = ['POST'])
def delete(todo_id): # This is called whenever the Delete button next to a todo element is
# clicked, signifiying that the user intends to delete the corresponding element. We 
# temporarily jump to a different route to do the work of deleting, then redirect back to
# the index page

	# When the Delete button is clicked, we direct to a route that contains the id of the 
	# tuple toDelete in the route itself. It is then easy to retrieve this id and use it to
	# select for the unique tuple toDelete in the relation (since id is a primary key)
	toDelete = Todo.query.get(todo_id)
	db.session.delete(toDelete)
	db.session.commit()
	return redirect('/') # Again we return to the starting_page() so that the app can be
	# displayed with the previous tuple deleted


if __name__ == '__main__':
	app.debug=True          #restarts every time you change code
	app.run()