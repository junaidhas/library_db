from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
# create the app
app = Flask(__name__)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)

#create new table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book)).scalars().all()
    return render_template("index.html",books = all_books)


@app.route("/delete")
def delete():
    book_id = request.args.get('book_id')
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods =["GET", "POST"])
def add():
    # IF ACCESSED VIA POST THEN THE BOOK HAS BEEN ADDED
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"],
        )
        # Create A New Record
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    # IF ACCESSED VIA GET THEN THE ADD FORM NEEDS TO BE PRESENTED
    return render_template("add.html")


@app.route('/edit', methods=["GET", "POST"])
def edit_rating():
    # IF ACCESSED VIA GET THEN THE EDIT FORM NEEDS TO BE PRESENTED
    book_id = request.args.get('book_id')
    book_to_edit = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()



    # IF ACCESSED VIA POST THEN THE RATING HAS BEEN EDITED      `
    if request.method == "POST":
            book_to_edit.rating =request.form["new_rating"]
            db.session.commit()
            return redirect(url_for('home'))

    return render_template("edit.html", book=book_to_edit)



if __name__ == "__main__":
    app.run(debug=True)

