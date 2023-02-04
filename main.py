from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection-app.db'
db = SQLAlchemy(app)

# table
with app.app_context():
    class Books(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        author = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.Float, nullable=False)

        def __repr__(self):
            books = f'{self.id}, {self.title}, {self.author}, {self.rating}'
            return books


    db.create_all()

    @app.route('/')
    def home():
        books = db.session.query(Books).all()
        return render_template('index.html', all_books=books)

    @app.route("/add", methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            data = request.form
            book = Books(title=data['title'], author=data['author'], rating=data['rating'])
            db.session.add(book)
            db.session.commit()
            return render_template('index.html', all_books=db.session.query(Books).all())
        return render_template('add.html')

    @app.route('/edit-rating/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        if request.method == 'POST':
            book_to_update = Books.query.get(id)
            book_to_update.rating = request.form['rating']
            db.session.commit()

            books = db.session.query(Books).all()
            return render_template('index.html', all_books=books)

        selected_book = Books.query.get(id)
        return render_template('edit-rating.html', book=selected_book)

    @app.route('/delete/<int:id>')
    def delete(id):
        book = Books.query.get(id)
        db.session.delete(book)
        db.session.commit()
        books = db.session.query(Books).all()
        return render_template('index.html', all_books=books)

    if __name__ == "__main__":
        app.run(debug=True)

# < h1 > My
# Library < / h1 >
# { %
# if all_books | length > 0: %}
# { %
# if all_books | length == 1: %}
# { % set
# book_info = all_books %}
# < ul >
# < li > {{book_info['title'], book_info['author']}} < a
# href = "{{ url_for('edit_rating', id=book['id']) }}" > Edit
# rating < / a > < / li >
# < / ul >
# { % else: %}
# { %
# for book in all_books: %}
# < !--                { % set
# book_info = book.split(',') %}-->
# < ul >
# < li > {{book_info['title'], book_info['author']}} < a
# href = "{{ url_for('edit_rating', id=book_info['id']) }}" > Edit
# rating < / a > < / li >
# < / ul >
# { % endfor %}
# { % endif %}
# { % else: %}
# < p > Library is empty. < / p >
# { % endif %}
#
# < a
# href = "{{ url_for('add') }}" > Add
# New
# Book < / a >