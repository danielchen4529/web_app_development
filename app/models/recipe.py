from datetime import datetime
from . import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def create(cls, title, ingredients, instructions, image_url=None, category_id=None):
        recipe = cls(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            image_url=image_url,
            category_id=category_id
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, title=None, ingredients=None, instructions=None, image_url=None, category_id=None):
        if title is not None:
            self.title = title
        if ingredients is not None:
            self.ingredients = ingredients
        if instructions is not None:
            self.instructions = instructions
        if image_url is not None:
            self.image_url = image_url
        if category_id is not None:
            self.category_id = category_id
            
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
