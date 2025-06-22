from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required')
        if Author.query.filter(Author.name == name).first():
            raise ValueError('Name must be unique')
        return name
    @validates('phone_number')
    def validate_phone(self, key, number):
        if number and (len(number) != 10 or not number.isdigit()):
            raise ValueError("Phone number must be 10 digits.")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content')
    def validate_content(self, _, content):
        if len(content) < 250:
            raise ValueError("Content must be ≥ 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, _, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be ≤ 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, _, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction/Non-Fiction.")
        return category

    @validates('title')
    def validate_title(self, _, title):
        phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in phrases):
            raise ValueError("Title must include a clickbait phrase.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'