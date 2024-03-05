from typing import Any
from sqlalchemy.exc import IntegrityError

from ...exceptions import NotFoundException, CreationFailedException
from ...models import db


# Assuming db and ma are initialized in your main Flask application

class CRUDService:
    """
    A CRUD service for a Flask RESTx project, using Flask-Marshmallow for
    serialization and deserialization
    """

    def __init__(self, model, schema, db=db):
        self.model = model
        self.schema = schema
        self.db = db

    def create(self, data)->Any:
        """takes json data and returns the created item if successful"""
        try:
            item = self.schema.load(data, session=self.db.session)
            self.db.session.add(item)
            self.db.session.commit()
            return item
        except IntegrityError as e:
            self.db.session.rollback()
            raise CreationFailedException(f"Creation failed: {e.orig}")

    def get(self, id)->Any:
        """takes id, returns item if successful, raises NotFound if not"""
        item = self.model.query.get(id)
        if not item:
            raise NotFoundException(f"Item with ID {id} does not exist")
        return item


    def get_all(self)->Any:
        items = self.model.query.all()
        return items

    def update(self, id, data)->Any:
        """
        input: id, json data
        patch the item with the given id with the given data
        returns item if successful, raises NotFound if not
        """
        item = self.model.query.get(id)
        if not item:
            raise NotFoundException(f"Item with ID {id} does not exist")
        try:
            self.schema.load(data, instance=item, session=self.db.session)
            self.db.session.commit()
            return item
        except IntegrityError as e:
            self.db.session.rollback()
            raise CreationFailedException(f"Creation failed: {e.orig}")


    def delete(self, id)->Any:
        """Returns item if successful, raises ValidationError if not"""
        item = self.model.query.get(id)
        if not item:
            raise NotFoundException(f"Item with ID {id} does not exist")
        self.db.session.delete(item)
        self.db.session.commit()
        return item
