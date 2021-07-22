from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # becoz of lazy=dynamic self.items -> becomes a query builder, hence we used .all()
        return {'name': self.name, 'items': list(map(lambda item: item.json(), self.items.all()))}

    @classmethod
    def get_all_stores(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_store_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_store_from_db(self):

        db.session.delete(self)
        db.session.commit()
